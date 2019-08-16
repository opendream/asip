import traceback
from django.db import models
from haystack.exceptions import NotHandled
from haystack.signals import RealtimeSignalProcessor
from organization.models import Job


class SearchRealtimeSignalProcessor(RealtimeSignalProcessor):

    def handle_save(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        update should be sent to & update the object on those backends.
        """
        using_backends = self.connection_router.for_write(instance=instance)

        related_instance = None
        related_sender = None
        if instance._meta.app_label == 'relation' and hasattr(instance, 'dst') and instance.dst_id:
            related_instance = instance
            related_sender = instance.__class__

            instance = instance.dst
            sender = instance.__class__

        from party.models import Party

        if instance.__class__ is Party:
            if hasattr(instance, 'organization'):
                instance = instance.organization
            elif hasattr(instance, 'user'):
                instance = instance.user

            sender = instance.__class__

        if instance.__class__ is Job and instance.organization_jobs.first():
            instance = instance.organization_jobs.first()
            sender = instance.__class__

        for using in using_backends:

            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                index.update_object(instance, using=using)

                if related_instance and related_sender:
                    related_index = self.connections[using].get_unified_index().get_index(related_sender)
                    related_index.update_object(related_instance, using=using)
            except (NotHandled, KeyError, AttributeError) as e:
                # TODO: Maybe log it or let the exception bubble?
                pass

    def handle_delete(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        delete should be sent to & delete the object on those backends.
        """
        using_backends = self.connection_router.for_write(instance=instance)

        related_instance = None
        related_sender = None

        if instance._meta.app_label == 'relation' and hasattr(instance, 'dst') and instance.dst_id:
            related_instance = instance
            related_sender = instance.__class__

            instance = instance.dst
            sender = instance.__class__

        from party.models import Party

        if instance.__class__ is Party:
            if hasattr(instance, 'organization'):
                instance = instance.organization
            elif hasattr(instance, 'user'):
                instance = instance.user

            sender = instance.__class__

        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                index.remove_object(instance, using=using)

                if related_instance and related_sender:
                    related_index = self.connections[using].get_unified_index().get_index(related_sender)
                    related_index.remove_object(related_instance, using=using)

            except NotHandled:
                # TODO: Maybe log it or let the exception bubble?
                pass

    def handle_m2m_changed(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        update should be sent to & update the object on those backends.
        """
        using_backends = self.connection_router.for_write(instance=instance)

        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().get_index(type(instance))
                index.update_object(instance, using=using)
            except NotHandled:
                # TODO: Maybe log it or let the exception bubble?
                pass

    def setup(self):
        models.signals.m2m_changed.connect(self.handle_m2m_changed)
        super(SearchRealtimeSignalProcessor, self).setup()

    def teardown(self):
        models.signals.m2m_changed.disconnect(self.handle_m2m_changed)
        super(SearchRealtimeSignalProcessor, self).teardown()

