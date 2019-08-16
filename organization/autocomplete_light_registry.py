import autocomplete_light

from account.models import User
from common.constants import STATUS_PUBLISHED, STATUS_PENDING
from organization.functions import job_render_reference, program_render_reference, user_render_reference, \
    staff_render_reference, in_the_news_render_reference
from organization.models import Job, Program, OrganizationStaff, InTheNews


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

class InTheNewsAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = InTheNews.objects.filter().order_by('-date', '-created')
    search_fields = ['title']

    display_edit_link = True
    field_name = 'in_the_news'

    def choice_label(self, choice):

        return in_the_news_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))


class ProgramAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = Program.objects.all().extra(select={'is_published': 'status = %d' % STATUS_PUBLISHED, 'is_pending': 'status = %d' % STATUS_PENDING}).order_by('-is_published', '-is_pending', '-status', '-ordering')
    search_fields = ['name']

    display_edit_link = True
    field_name = 'programs'

    def choice_label(self, choice):
        return program_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))

class ProgramInlineAutocomplete(ProgramAutocomplete):
    display_edit_link = False


class UserProgramAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = User.objects.filter().order_by('first_name', 'last_name')
    search_fields = ['email']

    display_edit_link = False
    field_name = 'users'

    def choice_label(self, choice):
        return user_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))


class StaffAutocomplete(autocomplete_light.AutocompleteModelBase):
    choices = OrganizationStaff.objects.filter().order_by('email')
    search_fields = ['name', 'email']

    display_edit_link = False
    field_name = 'staff'

    def choice_label(self, choice):
        return staff_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):
        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))


autocomplete_light.register(Job, JobAutocomplete)
autocomplete_light.register(Program, ProgramAutocomplete)
autocomplete_light.register(Program, ProgramInlineAutocomplete)
autocomplete_light.register(User, UserProgramAutocomplete)
autocomplete_light.register(OrganizationStaff, StaffAutocomplete)


