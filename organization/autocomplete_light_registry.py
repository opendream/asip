import autocomplete_light
from organization.functions import job_render_reference
from organization.models import Job


class JobAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = Job.objects.filter().order_by('-ordering')
    search_fields = ['title']

    display_edit_link = True
    field_name = 'jobs'

    def choice_label(self, choice):

        return job_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))

autocomplete_light.register(Job, JobAutocomplete)

