# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
import tagging_autocomplete_tagit.models
import ckeditor.fields
import django.utils.timezone
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
        ('auth', '0001_initial'),
        ('party', '0003_auto_20150429_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('party_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='party.Party')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('image', files_widget.fields.ImageField(max_length=200, null=True, blank=True)),
                ('first_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True, blank=True)),
                ('occupation', models.CharField(max_length=255, null=True, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('description', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('skills', tagging_autocomplete_tagit.models.TagAutocompleteTagItField(max_length=255, null=True, blank=True)),
                ('facebook_url', models.URLField(max_length=255, null=True, blank=True)),
                ('twitter_url', models.URLField(max_length=255, null=True, blank=True)),
                ('linkedin_url', models.URLField(max_length=255, null=True, blank=True)),
                ('homepage_url', models.URLField(max_length=255, null=True, blank=True)),
                ('username', models.CharField(help_text='Required 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.@+-]+$'), 'Enter a valid username.', b'invalid')])),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('notification_allow_email_send_organizationhaspeople', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_partysupportparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_partyfollowparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_partycontactparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_partytestifyparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_partylove', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_partyinvitetestifyparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_organization_partypartnerparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_organization_userexperienceorganization', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_organization_partysupportparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_organization_partyfollowparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_organization_partycontactparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_organization_partytestifyparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_organization_partylove', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_organization_partyinvitetestifyparty', models.NullBooleanField(default=True)),
                ('notification_allow_email_send_from_follow', models.NullBooleanField(default=True)),
                ('user_email_notification', models.NullBooleanField()),
                ('organization_email_notification', models.NullBooleanField()),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('interests', models.ManyToManyField(related_name='interests', null=True, to='taxonomy.Topic', blank=True)),
                ('party_activated', models.ForeignKey(related_name='party_activated', blank=True, to='party.Party', null=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
                ('user_roles', models.ManyToManyField(related_name='user_roles', null=True, to='taxonomy.UserRole', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('party.party', models.Model),
        ),
    ]
