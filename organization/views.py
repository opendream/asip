import os
import re
import shutil
from subprocess import CalledProcessError
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import QuerySet, Q
from django import forms
from django.forms import formset_factory
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from wkhtmltopdf import wkhtmltopdf
from wkhtmltopdf.views import PDFTemplateResponse

from account.forms import PasswordResetForm
from account.functions import user_can_edit_check

from common.constants import STATUS_PUBLISHED, STATUS_CHOICES_DISPLAY, STATUS_PENDING, STATUS_DRAFT, TYPE_PROGRAM, TYPE_INVESTOR
from common.decorators import statistic
from common.forms import RequiredFormSet, RequiredFirstFormSet
from common.functions import process_status, get_success_message, camelcase_to_underscore, instance_set_permalink, \
    get_point
from common.templatetags.common_tags import render_form_field_errors
from organization.constants import TAB_LIST_CONFIG, PROMOTE_LIST_CONFIG
from organization.forms import OrganizationEditForm, OrganizationEditInlineForm, \
    TeamInformationForm, OrganizationSection1EditForm, OrganizationSection2EditForm, \
    OrganizationSection3EditForm, OrganizationSection4EditForm, OrganizationSection5EditForm, \
    PhoneNumberOfOrganizationsHeadquartersForm, LocationOfOrganizationsOperatingFacilitiesForm, \
    MeasurementYearValuesForm, Top3MajorInvestorsYearAndAmountForm, Top3MajorDonorsYearAndAmountForm, JobEditForm, \
    ProgramEditForm, BatchSection1Form, BatchSection2Form, OrganizationInformationForm, \
    ContactPersonInformationForm, StaffInviteForm, OrganizationAssistantshipForm, OrganizationFundingRoundForm, \
    OrganizationExtraForm, OrganizationParticipantForm, ProgramInlineEditForm, ContactInformationForm, JobApplyForm, \
    ParticipantOrganizationForm, OrganizationAttachmentForm, InTheNewsEditForm
from organization.functions import organization_render_reference, job_render_reference, program_render_reference, \
    in_the_news_render_reference
from organization.models import Organization, Job, Program, ProgramBatch, OrganizationStaff, \
    OrganizationAssistance, OrganizationFundingRound, InTheNews

import json
from party.functions import portfolio_render_reference
from party.models import Party
from relation.models import OrganizationHasPeople, PartyPartnerParty, PartySupportParty, PartyReceivedFundingParty, \
    PartyInvestParty, PartyReceivedInvestingParty, OrganizationParticipate, UserApplyJob
from special.models import Special
from taxonomy.models import OrganizationRole, TypeOfAssistantship, OrganizationType


def instance_save_formset(instance, field_name, formset, formset_field_list):
    pass


@login_required
def organization_create(request, type_of_organization, instance=None, build_point_from_initial=False, get_context=False):
    return _organization_create(request, type_of_organization, instance, build_point_from_initial, get_context)

def _organization_create(request, type_of_organization, instance=None, build_point_from_initial=False, get_context=False):

    if type_of_organization == TYPE_PROGRAM:
        if instance:
            return redirect('program_create', instance.id)
        return redirect('program_create_instance')

    # Extra
    if (instance and not instance.id) and type_of_organization not in dict(Organization.TYPE_CHOICES).keys():
        raise Http404
    elif type_of_organization not in dict(Organization.TYPE_CHOICES).keys():
        type_of_organization = settings.DEFAULT_TYPE_RECEIVER

    type_of_organization_name = dict(Organization.TYPE_CHOICES)[type_of_organization]

    informal_status = STATUS_DRAFT
    if request.method == 'POST':
        informal_status = int(request.POST.get('status', STATUS_DRAFT))
    elif instance:
        informal_status = instance.status

    formset_extra = 1
    if informal_status == STATUS_PUBLISHED:
        formset_extra = 1


    # Config for reuse
    ModelClass = Organization
    instance = instance or ModelClass(type_of_organization=type_of_organization)

    # Formset
    TeamInformationFormSet = formset_factory(TeamInformationForm, extra=formset_extra, can_delete=True)
    PhoneNumberOfOrganizationsHeadquartersFormSet = formset_factory(PhoneNumberOfOrganizationsHeadquartersForm, formset=RequiredFormSet, extra=formset_extra, can_delete=True)
    LocationOfOrganizationsOperatingFacilitiesFormSet = formset_factory(LocationOfOrganizationsOperatingFacilitiesForm, extra=formset_extra, can_delete=True)
    MeasurementYearValuesFormSet = formset_factory(MeasurementYearValuesForm, extra=1, can_delete=True)

    Top3MajorInvestorsYearAndAmountFormSet = formset_factory(Top3MajorInvestorsYearAndAmountForm, extra=3, can_delete=True, max_num=3)
    Top3MajorDonorsYearAndAmountFormSet = formset_factory(Top3MajorDonorsYearAndAmountForm, extra=3, can_delete=True, max_num=3)

    OrganizationAssistantshipFormSet = formset_factory(OrganizationAssistantshipForm, extra=0, can_delete=True)
    OrganizationFundingRoundFormSet = formset_factory(OrganizationFundingRoundForm, extra=formset_extra, can_delete=True)

    OrganizationParticipantFormSet = formset_factory(OrganizationParticipantForm, extra=formset_extra, can_delete=True)

    if request.method == 'POST':

        instance.type_of_organization = type_of_organization

        form = OrganizationEditForm(instance, ModelClass, request.user, request.POST)
        extra_form = OrganizationExtraForm(request.POST, prefix='extra_form')

        # Extra form
        organization_section1_form = OrganizationSection1EditForm(request.POST, instance=instance)
        organization_section2_form = OrganizationSection2EditForm(request.POST, instance=instance)
        organization_section3_form = OrganizationSection3EditForm(request.POST, instance=instance)
        organization_section4_form = OrganizationSection4EditForm(request.POST, instance=instance)
        organization_section5_form = OrganizationSection5EditForm(request.POST, instance=instance)
        organization_attachment_form = OrganizationAttachmentForm(request.POST, instance=instance)

        # Formset
        team_information_formset = TeamInformationFormSet(request.POST, prefix='team_information')
        phone_number_of_organizations_headquarters_formset = PhoneNumberOfOrganizationsHeadquartersFormSet(request.POST, prefix='phone_number_of_organizations_headquarters')
        location_of_organizations_operating_facilities_formset = LocationOfOrganizationsOperatingFacilitiesFormSet(request.POST,
                                                                                                                   prefix='location_of_organizations_operating_facilities')
        measurement_year_values_formset = MeasurementYearValuesFormSet(request.POST, prefix='measurement_year_values')
        top_3_major_investors_year_and_amount_formset = Top3MajorInvestorsYearAndAmountFormSet(request.POST, prefix='top_3_major_investors_year_and_amount')
        top_3_major_donors_year_and_amount_formset = Top3MajorDonorsYearAndAmountFormSet(request.POST, prefix='top_3_major_donors_year_and_amount')

        organization_assistantship_formset = OrganizationAssistantshipFormSet(request.POST, prefix='organization_assistantship')
        organization_funding_round_formset = OrganizationFundingRoundFormSet(request.POST, prefix='organization_funding_round')

        organization_participant_formset = OrganizationParticipantFormSet(request.POST,
                                                                             prefix='organization_participant')

        is_new = form.is_new()



        # Formset
        if form.is_valid() and \
           extra_form.is_valid() and \
           organization_section1_form.is_valid() and organization_section2_form.is_valid() and \
           organization_section3_form.is_valid() and organization_section4_form.is_valid() and \
           organization_section5_form.is_valid() and \
           organization_attachment_form.is_valid() and \
           team_information_formset.is_valid() and \
           organization_assistantship_formset.is_valid() and \
           organization_funding_round_formset.is_valid() and \
           organization_participant_formset.is_valid() and \
           phone_number_of_organizations_headquarters_formset.is_valid() and \
           location_of_organizations_operating_facilities_formset.is_valid() and \
           measurement_year_values_formset.is_valid() and \
           top_3_major_investors_year_and_amount_formset.is_valid() and \
           top_3_major_donors_year_and_amount_formset.is_valid():

            if instance.id and form.cleaned_data.get('changed') != instance.changed_raw:
                messages.error(request, _('Someone or another browser tab has updated and added additional relationship information (funding, program, etc.) with your organization. <br/>Your relationship information is protected but your update information is lost. Please try again.'))
                return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)


            # Before save m2m
            organization_section1_form.save(commit=False)
            organization_section2_form.save(commit=False)
            organization_section3_form.save(commit=False)
            organization_section4_form.save(commit=False)
            organization_section5_form.save(commit=False)
            organization_attachment_form.save(commit=False)


            # Calculate point of this organization
            form_list = [
                form,
                organization_section1_form,
                organization_section2_form,
                organization_section3_form,
                organization_section4_form,
                organization_section5_form,
            ]

            if hasattr(settings, 'POINT'):
                instance.point = get_point(form_list, settings.POINT, [r.id for r in form.cleaned_data.get('organization_roles')], update=True)
            else:
                instance.point = 0

            # Relation
            if not instance.created_by_id:
                instance.created_by = request.user

            # Internal
            instance.permalink = form.cleaned_data.get('permalink')
            instance.name = form.cleaned_data.get('name')
            instance.preferred_name = form.cleaned_data.get('preferred_name')
            instance.summary = form.cleaned_data.get('summary')
            instance.kind = form.cleaned_data.get('kind')
            instance.description = form.cleaned_data.get('description')
            instance.date_of_establishment = form.cleaned_data.get('date_of_establishment')
            instance.company_registration_number = form.cleaned_data.get('company_registration_number')

            instance_image = instance._meta.get_field('image')
            if instance_image:
                instance_image.save_form_data(instance, form.cleaned_data.get('image'))

            instance_cover_image = instance._meta.get_field('cover_image')
            if instance_cover_image:
                instance_cover_image.save_form_data(instance, form.cleaned_data.get('cover_image'))

            instance_images = instance._meta.get_field('images')
            if instance_images:
                instance_images.save_form_data(instance, form.cleaned_data.get('images'))

            if type_of_organization == Organization.TYPE_STARTUP:
                instance.is_register_to_nia = form.cleaned_data.get('is_register_to_nia')

                instance.company_vision = form.cleaned_data.get('company_vision')
                instance.company_mission = form.cleaned_data.get('company_mission')
                instance.business_model = form.cleaned_data.get('business_model')
                instance.growth_strategy = form.cleaned_data.get('growth_strategy')

                instance.has_participate_in_program = form.cleaned_data.get('has_participate_in_program')
                instance.has_taken_equity_in_startup = form.cleaned_data.get('has_taken_equity_in_startup')
                instance.taken_equity_amount = form.cleaned_data.get('taken_equity_amount')
                instance.has_received_investment = form.cleaned_data.get('has_received_investment')
                instance.other_financial_source = form.cleaned_data.get('other_financial_source')

            if type_of_organization == Organization.TYPE_INVESTOR:
                instance.is_register_to_nia = form.cleaned_data.get('is_register_to_nia')
                instance.is_lead_investor = form.cleaned_data.get('is_lead_investor')

                instance.money_amount_of_money_invested = form.cleaned_data.get('money_amount_of_money_invested')
                instance.has_taken_equity_in_fund_organization = form.cleaned_data.get('has_taken_equity_in_fund_organization')

                instance.money_money_raise = form.cleaned_data.get('money_money_raise')
                instance.money_target_funding = form.cleaned_data.get('money_target_funding')
                instance.money_pre_money_valuation = form.cleaned_data.get('money_pre_money_valuation')

            # External
            instance.facebook_url = form.cleaned_data.get('facebook_url')
            instance.twitter_url = form.cleaned_data.get('twitter_url')
            instance.linkedin_url = form.cleaned_data.get('linkedin_url')
            instance.homepage_url = form.cleaned_data.get('homepage_url')
            instance.instagram_url = form.cleaned_data.get('instagram_url')
            instance.other_channel = form.cleaned_data.get('other_channel')

            instance.other_office_type = form.cleaned_data.get('other_office_type')
            instance.other_focus_sector = form.cleaned_data.get('other_focus_sector')
            instance.other_focus_industry = form.cleaned_data.get('other_focus_industry')

            instance.specialty = form.cleaned_data.get('specialty')
            instance.extra_information = json.dumps(extra_form.cleaned_data, cls=DjangoJSONEncoder)

            # Meta
            update_status = int(form.cleaned_data.get('status'))
            if request.user.is_staff or settings.ALLOWED_CREATE_ORGANIZATION_WITHOUT_APPROVAL:
                instance.status = update_status
            elif update_status == STATUS_PUBLISHED and not instance.published:
                pass
                # TODO: alert something
            else:
                instance.status = update_status


            if not instance.published and instance.status == STATUS_PUBLISHED:
                instance.published = timezone.now()
                instance.published_by = request.user

            instance.country = form.cleaned_data.get('country')
            instance.organization_primary_role = form.cleaned_data.get('organization_primary_role')

            # instance.product_launch = form.cleaned_data.get('product_launch')
            # instance.funding = form.cleaned_data.get('funding')
            # instance.request_funding = form.cleaned_data.get('request_funding')

            instance.money_deal_size_start = form.cleaned_data.get('money_deal_size_start')
            instance.money_deal_size_end = form.cleaned_data.get('money_deal_size_end')

            instance_attachments = instance._meta.get_field('attachments')
            if instance_attachments:
                instance_attachments.save_form_data(instance, form.cleaned_data.get('attachments'))

            instance.investor_type = form.cleaned_data.get('investor_type')
            instance.other_attachments_types = form.cleaned_data.get('other_attachments_types')

            # Formset
            team_information = []
            for team_information_form in team_information_formset:

                if team_information_form.cleaned_data and not team_information_form.cleaned_data.get('DELETE'):
                    team_information.append({
                        'name': team_information_form.cleaned_data.get('name'),
                        'title': team_information_form.cleaned_data.get('title')
                    })
            instance.team_information = team_information

            phone_number_of_organizations_headquarters = []
            for phone_number_of_organizations_headquarters_form in phone_number_of_organizations_headquarters_formset:

                if phone_number_of_organizations_headquarters_form.cleaned_data and not phone_number_of_organizations_headquarters_form.cleaned_data.get('DELETE'):
                    phone_number_of_organizations_headquarters.append({
                        'phone_number': phone_number_of_organizations_headquarters_form.cleaned_data.get('phone_number'),
                    })
            instance.phone_number_of_organizations_headquarters = phone_number_of_organizations_headquarters

            location_of_organizations_operating_facilities = []
            for location_of_organizations_operating_facilities_form in location_of_organizations_operating_facilities_formset:

                if location_of_organizations_operating_facilities_form.cleaned_data and not location_of_organizations_operating_facilities_form.cleaned_data.get(
                        'DELETE'):
                    location_of_organizations_operating_facilities.append({
                        'address': location_of_organizations_operating_facilities_form.cleaned_data.get('address'),
                    })
            instance.location_of_organizations_operating_facilities = location_of_organizations_operating_facilities

            measurement_year_values = []
            for measurement_year_values_form in measurement_year_values_formset:

                if measurement_year_values_form.cleaned_data and not measurement_year_values_form.cleaned_data.get(
                        'DELETE'):
                    measurement_year_values.append({
                        'year_of_datapoint': measurement_year_values_form.cleaned_data.get('year_of_datapoint'),
                        'value_of_impact_1': measurement_year_values_form.cleaned_data.get('value_of_impact_1'),
                        'value_of_impact_2': measurement_year_values_form.cleaned_data.get('value_of_impact_2'),
                        'value_of_impact_3': measurement_year_values_form.cleaned_data.get('value_of_impact_3'),
                    })
            instance.measurement_year_values = measurement_year_values

            top_3_major_investors_year_and_amount = []
            for top_3_major_investors_year_and_amount_form in top_3_major_investors_year_and_amount_formset:

                if top_3_major_investors_year_and_amount_form.cleaned_data and not top_3_major_investors_year_and_amount_form.cleaned_data.get(
                        'DELETE'):
                    top_3_major_investors_year_and_amount.append({
                        'title': top_3_major_investors_year_and_amount_form.cleaned_data.get('title')
                    })
            instance.top_3_major_investors_year_and_amount = top_3_major_investors_year_and_amount

            top_3_major_donors_year_and_amount = []
            for top_3_major_donors_year_and_amount_form in top_3_major_donors_year_and_amount_formset:

                if top_3_major_donors_year_and_amount_form.cleaned_data and not top_3_major_donors_year_and_amount_form.cleaned_data.get('DELETE'):
                    top_3_major_donors_year_and_amount.append({
                        'title': top_3_major_donors_year_and_amount_form.cleaned_data.get('title')
                    })
            instance.top_3_major_donors_year_and_amount = top_3_major_donors_year_and_amount

            instance.save()

            organization_section1_form.save_m2m()
            organization_section2_form.save_m2m()
            organization_section3_form.save_m2m()
            organization_section4_form.save_m2m()
            organization_section5_form.save_m2m()
            organization_attachment_form.save_m2m()

            # Taxonomy
            # instance.type_of_needs.clear()
            # for type_of_need in form.cleaned_data.get('type_of_needs'):
            #     instance.type_of_needs.add(type_of_need)
            #
            # instance.type_of_supports.clear()
            # for type_of_support in form.cleaned_data.get('type_of_supports'):
            #     instance.type_of_supports.add(type_of_support)
            #
            # instance.topics.clear()
            # for topic in form.cleaned_data.get('topics'):
            #     instance.topics.add(topic)

            instance.organization_roles.clear()
            for organization_role in form.cleaned_data.get('organization_roles'):
                instance.organization_roles.add(organization_role)
            #
            # instance.type_of_supports.clear()
            # for type_of_support in form.cleaned_data.get('type_of_supports'):
            #     instance.type_of_supports.add(type_of_support)

            instance.organization_types.clear()
            for organization_type in form.cleaned_data.get('organization_types'):
                instance.organization_types.add(organization_type)

            # instance.investor_types.clear()
            # for investor_type in form.cleaned_data.get('investor_types'):
            #     instance.investor_types.add(investor_type)

            # instance.growth_stage.clear()
            #
            # try:
            #     for growth_stage in form.cleaned_data.get('growth_stage'):
            #         instance.growth_stage.add(growth_stage)
            # except TypeError:
            #     if form.cleaned_data.get('growth_stage'):
            #         instance.growth_stage.add(form.cleaned_data.get('growth_stage'))


            # Specail

            if request.user.is_staff:
                specials = [special.id for special in form.cleaned_data.get('specials')]
                for special in instance.specials.exclude(id__in=specials):
                    instance.specials.remove(special)

                specials = [special.id for special in instance.specials.all()]
                for special in form.cleaned_data.get('specials').exclude(id__in=specials):
                    instance.specials.add(special)
            else:
                special = request.session.get('special', '')
                if special:
                    special = Special.objects.get(permalink=special)
                    instance.specials.add(special)



            # Relate

            admins = [admin.id for admin in form.cleaned_data['admins']]
            for admin in instance.admins.exclude(id__in=admins):
                instance.admins.remove(admin)

                for program in instance.program_organization.all():
                    program.admins.remove(admin)

            admins = [admin.id for admin in instance.admins.all()]
            for admin in form.cleaned_data['admins'].exclude(id__in=admins):
                instance.admins.add(admin)

                for program in instance.program_organization.all():
                    program.admins.add(admin)


            # Add default admin when created first
            if is_new and not instance.created_by.is_staff and not instance.admins.all().count():
                instance.admins.add(instance.created_by)

            portfolios = [portfolio.id for portfolio in form.cleaned_data.get('portfolios')]
            instance.portfolios.exclude(id__in=portfolios).delete()

            portfolios = [portfolio.id for portfolio in instance.portfolios.all()]
            for portfolio in form.cleaned_data.get('portfolios').exclude(id__in=portfolios):
                instance.portfolios.add(portfolio)

            jobs = [job.id for job in form.cleaned_data.get('jobs')]
            instance.jobs.exclude(id__in=jobs).delete()

            jobs = [job.id for job in instance.jobs.all()]
            for job in form.cleaned_data.get('jobs').exclude(id__in=jobs):
                instance.jobs.add(job)


            in_the_news = [item.id for item in form.cleaned_data.get('in_the_news')]
            instance.in_the_news.exclude(id__in=in_the_news).delete()

            in_the_news = [item.id for item in instance.in_the_news.all()]
            for item in form.cleaned_data.get('in_the_news').exclude(id__in=jobs):
                instance.in_the_news.add(item)


            programs = [program.id for program in form.cleaned_data.get('programs')]
            instance.program_organization.exclude(id__in=programs).delete()

            programs = [portfolio.id for portfolio in instance.program_organization.all()]
            for program in form.cleaned_data.get('programs').exclude(id__in=programs):
                instance.program_organization.add(program)


            OrganizationStaff.objects.filter(organization=instance).delete()
            for people in form.cleaned_data.get('key_person'):
                people.organization = instance
                people.staff_status = OrganizationStaff.STATUS_KEY_PERSON
                people.save()

            for people in form.cleaned_data.get('staff'):
                people.organization = instance
                people.staff_status = OrganizationStaff.STATUS_STAFF
                people.save()


            partners = set(form.cleaned_data['government_partners']) | set(form.cleaned_data['media_partners']) | set(form.cleaned_data['association_partners']) | set(form.cleaned_data['partners'])
            partners = Organization.objects.filter(id__in=[partner.id for partner in partners])

            PartyPartnerParty.objects.filter(src=instance).exclude(dst=partners).delete()
            PartyPartnerParty.objects.filter(dst=instance).exclude(src=partners).delete()
            for partner in partners:
                if instance.id == partner.id:
                    continue
                if not PartyPartnerParty.objects.filter(Q(src=instance, dst=partner) | Q(src=partner, dst=instance)).count():
                    PartyPartnerParty.objects.create(src=instance, dst=partner)


            PartySupportParty.objects.filter(dst=instance).exclude(src=form.cleaned_data.get('supporters')).delete()
            for supporter in form.cleaned_data.get('supporters'):
                if instance.id == supporter.id:
                    continue
                PartySupportParty.objects.get_or_create(src=supporter, dst=instance, defaults={
                    'src': supporter,
                    'dst': instance,
                    'swap': True
                })

            PartySupportParty.objects.filter(src=instance).exclude(dst=form.cleaned_data.get('recipients')).delete()
            for recipient in form.cleaned_data.get('recipients'):
                if instance.id == recipient.id:
                    continue
                PartySupportParty.objects.get_or_create(src=instance, dst=recipient)

            PartyInvestParty.objects.filter(dst=instance).exclude(src=form.cleaned_data.get('investors')).delete()
            for investor in form.cleaned_data.get('investors'):
                if instance.id == investor.id:
                    continue
                PartyInvestParty.objects.get_or_create(src=investor, dst=instance, defaults={
                    'src': investor,
                    'dst': instance,
                    'swap': True
                })

            PartyInvestParty.objects.filter(src=instance).exclude(dst=form.cleaned_data.get('invest_recipients')).delete()
            for invest_recipient in form.cleaned_data.get('invest_recipients'):
                if instance.id == invest_recipient.id:
                    continue
                PartyInvestParty.objects.get_or_create(src=instance, dst=invest_recipient)

            received_fundings = [received_funding.id for received_funding in form.cleaned_data.get('received_fundings')]
            PartyReceivedFundingParty.objects.filter(src__id=instance.id).exclude(id__in=received_fundings).delete()
            for received_funding in form.cleaned_data.get('received_fundings'):
                if not received_funding.src:
                    received_funding.src = instance.party_ptr
                    received_funding.save()

            gived_fundings = [gived_funding.id for gived_funding in form.cleaned_data.get('gived_fundings')]
            PartyReceivedFundingParty.objects.filter(dst__id=instance.id).exclude(id__in=gived_fundings).delete()
            for gived_funding in form.cleaned_data.get('gived_fundings'):
                if not gived_funding.dst:
                    gived_funding.dst = instance.party_ptr
                    gived_funding.swap = True
                    gived_funding.save()

            received_investings = [received_investing.id for received_investing in form.cleaned_data.get('received_investings')]
            PartyReceivedInvestingParty.objects.filter(src__id=instance.id).exclude(id__in=received_investings).delete()
            for received_investing in form.cleaned_data.get('received_investings'):
                if not received_investing.src:
                    received_investing.src = instance.party_ptr
                    received_investing.save()

            gived_investings = [gived_investing.id for gived_investing in form.cleaned_data.get('gived_investings')]
            PartyReceivedInvestingParty.objects.filter(dst__id=instance.id).exclude(id__in=gived_investings).delete()
            for gived_investing in form.cleaned_data.get('gived_investings'):
                if not gived_investing.dst:
                    gived_investing.dst = instance.party_ptr
                    gived_investing.swap = True
                    gived_investing.save()

            instance.office_type.clear()
            for office_type in form.cleaned_data.get('office_type'):
                instance.office_type.add(office_type)

            instance.focus_sector.clear()
            for focus_sector in form.cleaned_data.get('focus_sector'):
                instance.focus_sector.add(focus_sector)

            instance.focus_industry.clear()
            for focus_industry in form.cleaned_data.get('focus_industry'):
                instance.focus_industry.add(focus_industry)

            instance.stage_of_participants.clear()
            for stage_of_participants in form.cleaned_data.get('stage_of_participants'):
                instance.stage_of_participants.add(stage_of_participants)

            instance.financial_source.clear()
            for financial_source in form.cleaned_data.get('financial_source'):
                instance.financial_source.add(financial_source)

            instance.growth_stage.clear()
            try:
                for growth_stage in form.cleaned_data.get('growth_stage'):
                    instance.growth_stage.add(growth_stage)
            except TypeError:
                if form.cleaned_data.get('growth_stage'):
                    instance.growth_stage.add(form.cleaned_data.get('growth_stage'))

            instance.attachments_types.clear()
            for attachments_types in form.cleaned_data.get('attachments_types'):
                instance.attachments_types.add(attachments_types)

            if type_of_organization == Organization.TYPE_INVESTOR:
                instance.funding_type.clear()
                for funding_type in form.cleaned_data.get('funding_type'):
                    instance.funding_type.add(funding_type)

            instance.assistance_organization.filter(organization=instance).delete()
            for assistantship_form in organization_assistantship_formset:
                if assistantship_form.cleaned_data and assistantship_form.cleaned_data.get('type_of_assistantship'):
                    assistant = OrganizationAssistance()
                    assistant.description = assistantship_form.cleaned_data.get('description')
                    assistant.assistance = assistantship_form.cleaned_data.get('type_of_assistantship')
                    assistant.is_required = assistantship_form.cleaned_data.get('is_required')
                    assistant.organization = instance
                    assistant.save()

            instance.funding_round_organization.filter(organization=instance).delete()
            for funding_round_form in organization_funding_round_formset:
                if funding_round_form.cleaned_data and funding_round_form.cleaned_data.get('announced_date') and not funding_round_form.cleaned_data.get('DELETE'):
                    funding_round = OrganizationFundingRound()
                    funding_round.announced_date = funding_round_form.cleaned_data.get('announced_date')
                    funding_round.closed_date = funding_round_form.cleaned_data.get('closed_date')
                    funding_round.organization = instance
                    funding_round.save()

            for participant_form in organization_participant_formset:
                if participant_form.cleaned_data and participant_form.cleaned_data.get('program'):

                    if not participant_form.cleaned_data.get('program'):
                        continue

                    if participant_form.cleaned_data['id']:
                        participant = OrganizationParticipate.objects.get(id=participant_form.cleaned_data['id'])
                    else:
                        participant = OrganizationParticipate()

                    if participant_form.cleaned_data.get('DELETE'):
                        if participant:
                            participant.delete()
                    else:
                        participant.src = instance
                        participant.dst = participant_form.cleaned_data.get('program')
                        participant.month = participant_form.cleaned_data.get('month')
                        participant.save()


            instance.build_claim()


            message_success = get_success_message(instance, is_new, [type_of_organization])

            if settings.THANK_AFTER_CREATE and is_new:
                message_success = '%s<script type="text/javascript">$(\'#thankyou-modal\').modal(\'show\')</script>' % message_success

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, organization_render_reference(instance).replace("'", "\\'"))

            messages.success(request, message_success)
            if instance.status is not STATUS_PUBLISHED:
                #messages.warning(request, '%s is not publish organization.' % instance.name)
                messages.warning(request, _('%s is %s.') % (instance.name, dict(STATUS_CHOICES_DISPLAY)[instance.status].lower()))

            return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:

            error_message = _('Your submission error. Please, check in tab has the icon') + '%s' % (
                '&nbsp;<span class="glyphicon glyphicon-exclamation-sign"></span>',
                # render_form_field_errors(form)
            )

            messages.error(request, error_message)
            print form.errors


    else:

        organization_primary_role = request.GET.get('organization_primary_role', None)
        initial = {
            # Internal
            'changed': instance.changed_raw,
            'kind': instance.kind if instance.id else None,
            'permalink': instance.permalink,
            'name': instance.name or request.GET.get('name', ''),
            'summary': instance.summary,
            'description': instance.description,
            'image': instance.image,
            'cover_image': instance.cover_image,
            'images': instance.images,

            # External
            'facebook_url': instance.facebook_url,
            'twitter_url': instance.twitter_url,
            'linkedin_url': instance.linkedin_url,
            'homepage_url': instance.homepage_url,

            # Meta
            'status': instance.status,

            'country': instance.country,
            'organization_primary_role': instance.organization_primary_role or (organization_primary_role and OrganizationRole.objects.get(permalink=organization_primary_role)),

            'money_deal_size_start': instance.money_deal_size_start,
            'money_deal_size_end': instance.money_deal_size_end,

            #2018
            'preferred_name': instance.preferred_name,
            'company_registration_number': instance.company_registration_number,
            'date_of_establishment': instance.date_of_establishment,

            'instagram_url': instance.instagram_url,
            'other_channel': instance.other_channel,

            'specialty': instance.specialty,

            'office_type': instance.office_type.all() if instance.id else None,
            'other_office_type': instance.other_office_type,

            'focus_sector': instance.focus_sector.all() if instance.id else None,
            'other_focus_sector': instance.other_focus_sector,

            'focus_industry': instance.focus_industry.all() if instance.id else None,
            'other_focus_industry': instance.other_focus_industry,

            'stage_of_participants': instance.stage_of_participants.all() if instance.id else None,
            'growth_stage': instance.growth_stage.all() if instance.id else None,

            'financial_source': instance.financial_source.all() if instance.id else None,

            'attachments_types': instance.attachments_types.all() if instance.id else None,
            'attachments': instance.attachments if instance.attachments else None,

            'investor_type': instance.investor_type,
            'other_attachments_types': instance.other_attachments_types,
        }

        if type_of_organization == Organization.TYPE_STARTUP:
            initial['company_registration_number'] = instance.company_registration_number
            initial['is_register_to_nia'] = instance.is_register_to_nia

            initial['company_vision'] = instance.company_vision
            initial['company_mission'] = instance.company_mission
            initial['business_model'] = instance.business_model
            initial['growth_strategy'] = instance.growth_strategy

            initial['has_participate_in_program'] = instance.has_participate_in_program
            initial['has_taken_equity_in_startup'] = instance.has_taken_equity_in_startup
            initial['taken_equity_amount'] = instance.taken_equity_amount

            initial['has_received_investment'] = instance.has_received_investment
            initial['other_financial_source'] = instance.other_financial_source

        if type_of_organization == Organization.TYPE_INVESTOR:
            initial['kind'] = Organization.KIND_ORGANIZATION
            initial['is_register_to_nia'] = instance.is_register_to_nia

            initial['funding_type'] = instance.funding_type.all() if instance.id else None

            initial['is_lead_investor'] = instance.is_lead_investor
            initial['money_amount_of_money_invested'] = instance.money_amount_of_money_invested
            initial['has_taken_equity_in_fund_organization'] = instance.has_taken_equity_in_fund_organization

            initial['money_money_raise'] = instance.money_money_raise
            initial['money_target_funding'] = instance.money_target_funding
            initial['money_pre_money_valuation'] = instance.money_pre_money_valuation

        if instance.id:
            # Taxonomy
            initial['type_of_needs'] = instance.type_of_needs.all()
            initial['type_of_supports'] = instance.type_of_supports.all()
            initial['topics'] = instance.topics.all()
            initial['organization_roles'] = instance.organization_roles.all()
            initial['organization_types'] = instance.organization_types.all()
            initial['investor_types'] = instance.investor_types.all()

            initial['product_launch'] = instance.product_launch
            initial['funding'] = instance.funding
            initial['request_funding'] = instance.request_funding

            # if instance.type_of_organization in [Organization.TYPE_SUPPORTING_ORGANIZATION]:
            #     initial['growth_stage'] = instance.growth_stage.all()
            # else:
            #     try:
            #         initial['growth_stage'] = instance.growth_stage.all()[0]
            #     except IndexError:
            #         pass
            #

            UserModel = get_user_model()

            # Relate (Holy query)
            initial['admins'] = instance.admins.all().distinct()
            initial['portfolios'] = instance.portfolios.all().distinct()
            initial['jobs'] = instance.jobs.all().distinct()
            initial['in_the_news'] = instance.in_the_news.all().distinct()

            initial['programs'] = instance.program_organization.all()

            initial['key_person'] = OrganizationStaff.objects.filter(organization=instance, staff_status=OrganizationStaff.STATUS_KEY_PERSON)
            initial['staff'] = OrganizationStaff.objects.filter(organization=instance, staff_status=OrganizationStaff.STATUS_STAFF)

            if instance.type_of_organization == Organization.TYPE_STARTUP:
                initial['government_partners'] = Party.objects.filter((Q(partner_dst__src=instance) & Q(partner_dst__dst__organization__organization_types__permalink='government')) | (Q(partner_src__dst=instance) & Q(partner_src__src__organization__organization_types__permalink='government'))).distinct()
                initial['media_partners'] = Party.objects.filter((Q(partner_dst__src=instance) & Q(partner_dst__dst__organization__organization_types__permalink='media')) | (Q(partner_src__dst=instance) & Q(partner_src__src__organization__organization_types__permalink='media'))).distinct()
                initial['association_partners'] = Party.objects.filter((Q(partner_dst__src=instance) & Q(partner_dst__dst__organization__organization_types__permalink='association')) | (Q(partner_src__dst=instance) & Q(partner_src__src__organization__organization_types__permalink='association'))).distinct()
                # Party.objects.filter(
                initial['partners'] = Party.objects.filter((Q(partner_dst__src=instance) & ~Q(partner_dst__dst__organization__organization_types__permalink__in=['government', 'media', 'association'])) | (Q(partner_src__dst=instance) & ~Q(partner_src__src__organization__organization_types__permalink__in=['government', 'media', 'association']))).distinct()
            else:
                initial['partners'] = Party.objects.filter(Q(partner_dst__src=instance) | Q(partner_src__dst=instance)).distinct()

            initial['supporters'] = Party.objects.filter(support_src__dst=instance).distinct()
            initial['recipients'] = Party.objects.filter(support_dst__src=instance).distinct()
            initial['investors'] = Party.objects.filter(invest_src__dst=instance).distinct()
            initial['invest_recipients'] = Party.objects.filter(invest_dst__src=instance).distinct()

            initial['received_fundings'] = PartyReceivedFundingParty.objects.filter(src__id=instance.id).distinct()
            initial['gived_fundings'] = PartyReceivedFundingParty.objects.filter(dst__id=instance.id).distinct()

            initial['received_investings'] = PartyReceivedInvestingParty.objects.filter(src__id=instance.id).distinct()
            initial['gived_investings'] = PartyReceivedInvestingParty.objects.filter(dst__id=instance.id).distinct()

            if request.user.is_staff:
                initial['specials'] = instance.specials.all()

            extra_information = json.loads(instance.extra_information or '{}')

        else:
            initial['status'] = process_status(request.user, initial['status'], True)
            extra_information = {}

        form = OrganizationEditForm(instance, ModelClass, request.user, initial=initial)
        extra_form = OrganizationExtraForm(initial=extra_information, prefix='extra_form')

        # Extra form
        organization_section1_form = OrganizationSection1EditForm(instance=instance)
        organization_section2_form = OrganizationSection2EditForm(instance=instance)
        organization_section3_form = OrganizationSection3EditForm(instance=instance)
        organization_section4_form = OrganizationSection4EditForm(instance=instance)
        organization_section5_form = OrganizationSection5EditForm(instance=instance)
        organization_attachment_form = OrganizationAttachmentForm(instance=instance)

        organization_section3_form.fields['financial_statement_review'].widget = forms.CheckboxInput()

        user = False
        if request.user.is_authenticated():
            user = request.user

        if user and hasattr(user, 'is_staff') and user.is_staff is False:
            organization_section3_form.fields['financial_statement_review'].widget = forms.CheckboxInput(attrs={'readonly':'readonly', 'disabled': 'disabled'})
        # Formset
        team_information_formset = TeamInformationFormSet(
            initial=instance.team_information,
            prefix='team_information'
        )
        phone_number_of_organizations_headquarters_formset = PhoneNumberOfOrganizationsHeadquartersFormSet(
            initial=instance.phone_number_of_organizations_headquarters,
            prefix='phone_number_of_organizations_headquarters'
        )
        location_of_organizations_operating_facilities_formset = LocationOfOrganizationsOperatingFacilitiesFormSet(
            initial=instance.location_of_organizations_operating_facilities,
            prefix='location_of_organizations_operating_facilities'
        )
        measurement_year_values_formset = MeasurementYearValuesFormSet(
            initial=instance.measurement_year_values,
            prefix='measurement_year_values'
        )
        top_3_major_investors_year_and_amount_formset = Top3MajorInvestorsYearAndAmountFormSet(
            initial=instance.top_3_major_investors_year_and_amount,
            prefix='top_3_major_investors_year_and_amount'
        )
        top_3_major_donors_year_and_amount_formset = Top3MajorDonorsYearAndAmountFormSet(
            initial=instance.top_3_major_donors_year_and_amount,
            prefix='top_3_major_donors_year_and_amount'
        )

        organization_assistantship_initial = []

        for assistance in TypeOfAssistantship.objects.all():
            description = ''
            is_required = None

            try:
                exist = instance.assistance_organization.get(organization=instance, assistance=assistance)
                description = exist.description
                is_required = exist.is_required

            except OrganizationAssistance.DoesNotExist:
                pass

            organization_assistantship_initial.append({
                'type_of_assistantship': assistance,
                'type_of_assistantship_text': assistance.title,
                'description': description,
                'is_required': is_required
            })

        organization_assistantship_formset = OrganizationAssistantshipFormSet(initial=organization_assistantship_initial,
                                                                              prefix='organization_assistantship')

        organization_participant_initial = []
        if instance.participate_src.filter(src=instance).count():
            for participant in instance.participate_src.filter(src=instance):
                organization_participant_initial.append({
                    'id': participant.id,
                    'program': participant.dst,
                    'month': participant.month,
                    'status': participant.status,
                })
        else:
            pass

        organization_participant_formset = OrganizationParticipantFormSet(initial=organization_participant_initial,
                                                                          prefix='organization_participant')

        organization_funding_round_initial = []
        for funding_round in instance.funding_round_organization.filter(organization=instance).order_by('id'):
            organization_funding_round_initial.append({
                'announced_date': funding_round.announced_date,
                'closed_date': funding_round.closed_date
            })

        organization_funding_round_formset = OrganizationFundingRoundFormSet(initial=organization_funding_round_initial,
                                                                             prefix='organization_funding_round')

        if build_point_from_initial:
            form_list = [
                form,
                organization_section1_form,
                organization_section2_form,
                organization_section3_form,
                organization_section4_form,
                organization_section5_form,
            ]
            if hasattr(settings, 'POINT'):
                instance.point = get_point(form_list, settings.POINT, instance.organization_roles.all().values_list('id', flat=True), update=False)
            else:
                instance.point = 0

            instance.save()

            return True

    context = {
        'form': form,
        'extra_form': extra_form,
        'type_of_organization': type_of_organization,
        'type_of_organization_name': type_of_organization_name,
        # Section
        'organization_section1_form': organization_section1_form,
        'organization_section2_form': organization_section2_form,
        'organization_section3_form': organization_section3_form,
        'organization_section4_form': organization_section4_form,
        'organization_section5_form': organization_section5_form,
        'organization_attachment_form': organization_attachment_form,
        # Formset
        'team_information_formset': team_information_formset,
        'phone_number_of_organizations_headquarters_formset': phone_number_of_organizations_headquarters_formset,
        'location_of_organizations_operating_facilities_formset': location_of_organizations_operating_facilities_formset,
        'measurement_year_values_formset': measurement_year_values_formset,
        'top_3_major_investors_year_and_amount_formset': top_3_major_investors_year_and_amount_formset,
        'top_3_major_donors_year_and_amount_formset': top_3_major_donors_year_and_amount_formset,

        'organization_assistantship_formset': organization_assistantship_formset,
        'organization_funding_round_formset': organization_funding_round_formset,
        'organization_participant_formset': organization_participant_formset
    }

    if get_context:
        return context

    return render(request, 'organization/form.html', context)

@login_required
def organization_edit(request, organization_id=None):

    organization = get_object_or_404(Organization, id=organization_id)
    if hasattr(organization, 'program'):
        return redirect('program_edit', organization.program.id)

    # Check permission
    user_can_edit_check(request, organization)

    return _organization_create(request, organization.type_of_organization, organization)

def organization_generate_pdf(request, organization_id, bypass_key):
    organization = get_object_or_404(Organization, id=organization_id)
    if bypass_key == settings.BYPASS_KEY:
        if organization.type_of_organization == TYPE_PROGRAM:
            return _program_create(request, instance=organization.program)

        return _organization_create(request, organization.type_of_organization, organization)
    return Http404

@login_required
def organization_pdf(request, organization_id):

    organization = get_object_or_404(Organization, id=organization_id)

    # Check permission
    user_can_edit_check(request, organization)

    container = '%s/media/pdf' % settings.BASE_DIR
    if not os.path.exists(container):
        os.makedirs(container)

    dir_path = '%s/organization-%s' % (container, organization.permalink)

    changed = organization.changed_raw or organization.changed or organization.created or organization.created_raw
    file_name = 'organization-%s-%s.pdf' % (organization.permalink, changed.strftime("%s"))
    dest = '%s/%s' % (dir_path, file_name)

    # case has old version pdf or generate new pdf
    if not os.path.exists(dest):

        # case has old version pdf
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path) # clear

        os.makedirs(dir_path)

        try:
            pdf_url = '%s://%s%s' % (request.scheme, request.get_host(), reverse('organization_generate_pdf', args=[organization.id, settings.BYPASS_KEY])) + '?vary_print=true'
            print 'generate pdf from %s' % pdf_url
            print 'save to %s' % dest
            wkhtmltopdf(pdf_url, dest,
                quiet=None, javascript_delay='2000', print_media_type=True, dpi=72, lowquality=True,
            )
        except CalledProcessError:
            pass

    if os.path.exists(dest):
        f = open(dest, 'r')
        content_file = f.read()
        f.close()

        response = HttpResponse(content_file)
        response['Content-Disposition'] = 'attachment; filename=organization-%s.pdf' % (organization.permalink)
        response['Content-Type'] = 'application/pdf'

        return response

    return HttpResponse('OK')


@login_required
def organization_inline_create(request, instance=None):

    # Config for reuse
    ModelClass = Organization
    instance = instance or ModelClass()

    win_name = request.GET.get('_win_name') or request.POST.get('_win_name') or 'id_dst'
    no_script = request.GET.get('no_script') or request.POST.get('no_script') or 0
    return_display_name = request.GET.get('return_display_name') or request.POST.get('return_display_name') or 0

    type_of_organization = request.GET.get('type_of_organization')
    force_type_of_organization = request.GET.get('force_type_of_organization') or request.POST.get('force_type_of_organization') or 0
    organization_type__permalink = request.GET.get('organization_type__permalink')

    required_address = request.GET.get('required_address') or request.POST.get('required_address') or 0
    required_contact = request.GET.get('required_contact') or request.POST.get('required_contact') or 0
    is_mockup = request.GET.get('is_mockup') or request.POST.get('is_mockup') or 0

    PhoneNumberOfOrganizationsHeadquartersFormSet = formset_factory(PhoneNumberOfOrganizationsHeadquartersForm, extra=1, can_delete=True)

    if request.method == 'POST':


        form = OrganizationEditInlineForm(instance, ModelClass, request.user, request.POST)
        phone_number_of_organizations_headquarters_formset = PhoneNumberOfOrganizationsHeadquartersFormSet(request.POST, prefix='phone_number_of_organizations_headquarters')

        is_new = form.is_new()

        if form.is_valid() and (not required_contact or phone_number_of_organizations_headquarters_formset.is_valid()):

            # Relation
            if not instance.created_by_id:
                instance.created_by = request.user

            instance.name = form.cleaned_data.get('name')

            primary_role = form.cleaned_data.get('type_of_organization')
            organization_type__permalink = form.cleaned_data.get('organization_type__permalink')

            instance.type_of_organization = primary_role

            primary_role = OrganizationRole.objects.get(permalink=primary_role)
            organization_type = None
            if organization_type__permalink:
                organization_type = OrganizationType.objects.get(permalink=organization_type__permalink)
            instance.organization_primary_role = primary_role

            if required_address:
                instance.location_of_organizations_headquarters = form.cleaned_data.get('location_of_organizations_headquarters')

            if required_contact:
                instance.store_email_of_organizations_headquarters = form.cleaned_data.get('store_email_of_organizations_headquarters')

                phone_number_of_organizations_headquarters = []
                for phone_number_of_organizations_headquarters_form in phone_number_of_organizations_headquarters_formset:

                    if phone_number_of_organizations_headquarters_form.cleaned_data and not phone_number_of_organizations_headquarters_form.cleaned_data.get('DELETE'):
                        phone_number_of_organizations_headquarters.append({
                            'phone_number': phone_number_of_organizations_headquarters_form.cleaned_data.get('phone_number'),
                        })
                instance.phone_number_of_organizations_headquarters = phone_number_of_organizations_headquarters


            instance_set_permalink(instance, instance.name, prefix='inline')

            instance_image = instance._meta.get_field('image')
            if instance_image:
                instance_image.save_form_data(instance, form.cleaned_data.get('image'))

            instance.status = STATUS_DRAFT
            instance.is_mockup = is_mockup
            instance.save()

            instance.organization_roles.add(primary_role)
            if organization_type:
                instance.organization_types.add(organization_type)

            # Add default admin when created first
            if is_new and not instance.created_by.is_staff and not instance.admins.all().count():
                instance.admins.add(instance.created_by)

            special = request.session.get('special', '')
            if not instance.id and special:
                special = Special.objects.get(permalink=special)
                instance.specials.add(special)

            message_success = get_success_message(instance, is_new, [instance.type_of_organization])

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, organization_render_reference(instance).replace("'", "\\'"))


            if request.GET.get('_inline') or request.POST.get('_inline'):
                form.inst = instance
            else:
                messages.success(request, message_success)
                return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:
            print 'vvvvvvv'
    else:
        initial = {
            # Internal
            'name': instance.name,
            'image': instance.image,
            'status': instance.status,
            'type_of_organization': type_of_organization,
            'organization_type__permalink': organization_type__permalink,
        }

        if instance.id:
            pass
        else:
            initial['status'] = process_status(request.user, initial['status'], True)


        form = OrganizationEditInlineForm(instance, ModelClass, request.user, initial=initial)
        phone_number_of_organizations_headquarters_formset = PhoneNumberOfOrganizationsHeadquartersFormSet(
            initial=instance.phone_number_of_organizations_headquarters,
            prefix='phone_number_of_organizations_headquarters'
        )

    return render(request, 'organization/inline_form.html', {
        'form': form,
        'win_name': win_name,
        'no_script': no_script,
        'return_display_name': return_display_name,
        'force_type_of_organization': force_type_of_organization,
        'required_address': required_address,
        'required_contact': required_contact,
        'phone_number_of_organizations_headquarters_formset': phone_number_of_organizations_headquarters_formset,
        'is_mockup': is_mockup,
    })


@statistic
def organization_detail(request, organization_permalink):

    # For user type name from url
    organization = get_object_or_404(Organization, permalink=organization_permalink)
    #if not organization_id:
    #    return redirect('organization_detail', type_of_organization, organization_permalink, organization.id)

    return render(request, 'organization/detail.html', {
        'party_list_type': organization.type_of_organization,
        'organization_permalink': organization_permalink,
        'organization_id': organization.id,
        'instance': organization
    })

def organization_role_detail(request, organization_role_permalink, organization_permalink):

    # For user type name from url
    organization = get_object_or_404(Organization, permalink=organization_permalink)

    return render(request, 'organization/detail.html', {
        'party_list_type': organization_role_permalink,
        'organization_permalink': organization_permalink,
        'organization_id': organization.id,
        'instance': organization

    })


def organization_type_list(request, type_of_organization):

    # Extra
    if type_of_organization not in dict(Organization.TYPE_CHOICES).keys():
        raise Http404

    try:
        type_of_organization_name = dict(Organization.TYPE_CHOICES)[type_of_organization]

        tab_list_config = json.dumps(TAB_LIST_CONFIG[type_of_organization])
        promote_list_config = json.dumps(PROMOTE_LIST_CONFIG[type_of_organization])

        return render(request, 'party/list.html', {
            'party_list_type': type_of_organization,
            'party_list_title': type_of_organization_name,
            'tab_list_config': tab_list_config,
            'promote_list_config': promote_list_config
        })

    except:
        raise Http404


def organization_role_list(request, organization_role_permalink, organization_type_permalink=None):

    # Extra
    organization_role = get_object_or_404(OrganizationRole, permalink=organization_role_permalink)

    return render(request, 'party/list.html', {
        'party_list_type': organization_role,
        'party_list_title': organization_role.title,
        'tab_list_config': json.dumps(TAB_LIST_CONFIG[organization_role.permalink]),
        'promote_list_config': json.dumps(PROMOTE_LIST_CONFIG[organization_role.permalink]),
        'role_permalink': organization_role_permalink
    })


def organization_list(request):
    try:
        return render(request, 'party/list.html')
    except:
        raise Http404


@login_required
def job_create(request, organization_id=None, instance=None, standalone=False):

    # Config for reuse
    ModelClass = Job
    instance = instance or ModelClass()

    organization = None

    if instance.id and instance.organization_jobs.count():
        organization = instance.organization_jobs.all()[0]

    elif organization_id and int(organization_id):
        organization = get_object_or_404(Organization, id=organization_id)


    if request.method == 'POST':

        if request.POST.get('organization'):
            request.POST['organization'] = int(float(request.POST['organization']))


        required_organization = not request.GET.get('_popup') and not instance.id

        form = JobEditForm(instance, ModelClass, request.user, request.POST, user=request.user, required_organization=required_organization)

        is_new = form.is_new()

        is_valid = form.is_valid()
        if is_valid:

            if not instance.id:
                instance.created_by = request.user

            instance.title = form.cleaned_data['title']
            instance.contact_information = form.cleaned_data['contact_information']
            instance.description = form.cleaned_data['description']
            instance.role = form.cleaned_data['role']
            instance.job_primary_role = form.cleaned_data['job_primary_role']
            instance.position = form.cleaned_data['position']
            instance.money_salary_min = form.cleaned_data['money_salary_min']
            instance.money_salary_max = form.cleaned_data['money_salary_max']
            instance.equity_min = form.cleaned_data['equity_min']
            instance.equity_max = form.cleaned_data['equity_max']
            instance.remote = form.cleaned_data['remote'] == 'True'
            instance.years_of_experience = form.cleaned_data['years_of_experience']
            instance.country = form.cleaned_data['country']
            instance.location = form.cleaned_data['location']
            instance.skills = form.cleaned_data['skills']
            instance.status = int(form.cleaned_data['status'])

            form_organization = form.cleaned_data.get('organization')
            final_organization = organization or form_organization
            if final_organization and not instance.contact_information.strip():
                instance.contact_information = 'Tel: %s<br/>Email: %s<br/>Address: %s' % (
                    ', '.join([item.get('phone_number') for item in final_organization.phone_number_of_organizations_headquarters]),
                    final_organization.store_email_of_organizations_headquarters,
                    final_organization.location_of_organizations_headquarters,
                )

            instance.save()

            instance.job_roles.clear()
            for item in form.cleaned_data['job_roles']:
                if instance.job_primary_role and instance.job_primary_role.id != item.id:
                    instance.job_roles.add(item)

            instance.locations.clear()
            instance.locations.add(*form.cleaned_data['locations'])



            message_success = get_success_message(instance, is_new, [])


            sure_non_organization = False
            if organization:
                sure_non_organization = bool(organization.jobs.filter(id=instance.id).count() == 0)


            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, job_render_reference(instance).replace("'", "\\'"))
            elif organization and sure_non_organization:
                organization.jobs.add(instance)
            elif not organization and form_organization:
                form_organization.jobs.add(instance)



            messages.success(request, message_success)

            return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')


    else:

        initial = {
            'title': instance.title,
            'contact_information': instance.contact_information,
            'description': instance.description,
            'role': instance.role,
            'job_primary_role': instance.job_primary_role,
            'position': instance.position,
            'money_salary_min': instance.money_salary_min,
            'money_salary_max': instance.money_salary_max,
            'equity_min': instance.equity_min,
            'equity_max': instance.equity_max,
            'remote': bool(instance.remote),
            'years_of_experience': instance.years_of_experience,
            'country': instance.country or (organization and organization.country),
            'location': instance.location,
            'skills': instance.skills,
            'status': instance.status,
        }

        if instance.id:
            initial['job_roles'] = instance.job_roles.all()
            initial['locations'] = instance.locations.all()


        form = JobEditForm(instance, ModelClass, request.user, initial=initial, user=request.user)


    return render(request, 'organization/job/form.html', {
        'form': form,
        'standalone': standalone,
        'organization': organization,
    })

@login_required
def job_create_standalone(request):
    return job_create(request, standalone=True)


@login_required
def job_edit(request, job_id):

    instance = get_object_or_404(Job, id=job_id)

    # Check permission
    # user_can_edit_check(request.user, instance)

    return job_create(request, instance=instance)


def job_detail(request, job_id):
    instance = get_object_or_404(Job, id=job_id)
    return render(request, 'organization/job/detail.html', {'job_id': job_id, 'instance': instance})

@login_required(login_url='%s?advance=1&required_job=1' % settings.LOGIN_URL)
def job_list(request):
    user = request.user
    if not (user.job_status and user.job_public_status is not None and user.job_position and user.money_salary and user.job_locations and user.job_criteria):
        return redirect('%s?advance=1&required_job=1&next=%s' % (reverse('account_edit'), urllib.quote_plus(reverse('job_list'))))

    try:
        request.GET['f']
    except KeyError:

        params = []

        for item in user.job_roles.all():
            params.append('jobs_job_primary_role__permalink=%s' % item.permalink)

        for item in user.job_locations.all():
            params.append('jobs_locations__permalink=%s' % item.permalink)

        if user.job_position:
            params.append('jobs_position=%s' % user.job_position)

        return redirect(reverse('job_list') + ('?f#?%s' % '&'.join(params)))

    return render(request, 'organization/job/list.html')


@login_required(login_url='%s?advance=1&required_job=1' % settings.LOGIN_URL)
def job_apply(request):

    user = request.user

    if request.method == 'POST':
        form = JobApplyForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data['job']

            if not (user.job_status and user.job_public_status is not None and user.job_position and user.money_salary and user.job_locations and user.job_criteria):
                return redirect('%s?advance=1&required_job=1&next=%s' % (reverse('account_edit'), urllib.quote_plus(reverse('job_detail', args=[job.id]))))


            organization = job.organization_jobs.all().first()
            if not organization:
                raise Http404

            UserApplyJob.objects.get_or_create(src=user, dst=organization, job=job, defaults={
                'src': user, 'dst': organization, 'job': job, 'message': form.cleaned_data['message']
            })
            messages.success(request, u'Your application has been sent to %s' % organization.get_display_name())
            return redirect('job_detail', job.id)

        else:
            messages.error(request, u'Your submission error. %s' % form.errors)
            return redirect('job_detail', request.POST.get('job'))
    else:
        raise Http404

@login_required
def job_applying_list(request):
    return render(request, 'organization/job/applying_list.html')

@login_required
def job_applying_detail(request, apply_id):
    instance = get_object_or_404(UserApplyJob, id=apply_id)
    return render(request, 'organization/job/applying_detail.html', {'apply_id': apply_id, 'instance': instance})



def job_landing(request):
    return render(request, 'organization/job/landing.html', {'total_job': Job.objects.filter(status=STATUS_PUBLISHED).count()})


@login_required
def program_create(request, organization_id=None, instance=None):
    return _program_create(request, organization_id=organization_id, instance=instance)


def _program_create(request, organization_id=None, instance=None):

    # Config for reuse
    ModelClass = Program
    instance = instance or ModelClass()

    is_from_reference = bool(organization_id)
    informal_status = STATUS_DRAFT
    informal_is_register_to_nia = False
    if request.method == 'POST':
        informal_status = int(request.POST.get('status', STATUS_DRAFT))
        informal_is_register_to_nia = request.POST.get('is_register_to_nia', '') == 'True'
    elif instance:
        informal_status = instance.status
        informal_is_register_to_nia = instance.is_register_to_nia

    BatchSection1Formset = formset_factory(BatchSection1Form, min_num=2, max_num=6, extra=0, can_delete=True)
    if informal_status == STATUS_DRAFT or not informal_is_register_to_nia:
        BatchSection2Formset = formset_factory(BatchSection2Form, min_num=1, extra=0, can_delete=True)
    else:
        BatchSection2Formset = formset_factory(BatchSection2Form, formset=RequiredFirstFormSet, min_num=1, extra=0, can_delete=True)

    TeamInformationFormSet = formset_factory(TeamInformationForm, extra=1, can_delete=True)
    PhoneNumberOfOrganizationsHeadquartersFormSet = formset_factory(PhoneNumberOfOrganizationsHeadquartersForm,
                                                                    extra=1, can_delete=True)
    LocationOfOrganizationsOperatingFacilitiesFormSet = formset_factory(LocationOfOrganizationsOperatingFacilitiesForm, extra=1, can_delete=True)

    ParticipantOrganizationFormSet = formset_factory(ParticipantOrganizationForm, extra=1, can_delete=True)

    organization = None

    if instance.id and instance.organization:
        organization = instance.organization

    elif organization_id and int(organization_id):
        organization = get_object_or_404(Organization, id=organization_id)

    if request.method == 'POST':

        if request.POST.get('organization'):
            organization_id = int(float(request.POST['organization']))
            request.POST['organization'] = organization_id
            organization = get_object_or_404(Organization, id=organization_id)

        form = ProgramEditForm(instance, ModelClass, request.user, request.POST)

        organization_section1_form = OrganizationSection1EditForm(request.POST, instance=instance)
        organization_attachment_form = OrganizationAttachmentForm(request.POST, instance=instance)

        batch_section1_formset = BatchSection1Formset(request.POST, prefix='batch_section1_formset')
        batch_section2_formset = BatchSection2Formset(request.POST, prefix='batch_section2_formset')

        contact_form = ContactPersonInformationForm(request.POST, prefix='contact_form')
        working_form = ContactInformationForm(request.POST, prefix='working_form')

        participant_organization_formset = ParticipantOrganizationFormSet(request.POST,
                                                                             prefix='participant_organization')

        is_new = form.is_new()

        if form.is_valid() and \
            organization_section1_form.is_valid() and \
            organization_attachment_form.is_valid() and \
            contact_form.is_valid() and \
            working_form.is_valid() and \
            batch_section1_formset.is_valid() and \
            batch_section2_formset.is_valid() and \
            participant_organization_formset.is_valid():

            if not instance.id:
                instance.created_by = request.user

            organization_section1_form.save(commit=False)
            organization_attachment_form.save(commit=False)

            instance.name = form.cleaned_data['name']
            instance.type_of_organization = TYPE_PROGRAM

            if not form.cleaned_data['permalink']:
                instance_set_permalink(instance, instance.name)
            else:
                instance.permalink = form.cleaned_data['permalink']

            instance.date_of_establishment = form.cleaned_data['date_of_establishment']

            instance.contact_person = json.dumps(contact_form.cleaned_data)

            instance.other_focus_sector = form.cleaned_data['other_focus_sector']
            instance.other_focus_industry = form.cleaned_data['other_focus_industry']

            instance.is_acting_as_an_investor = form.cleaned_data['is_acting_as_an_investor']
            instance.has_invited_in_participants_team = form.cleaned_data['has_invited_in_participants_team']

            instance.specific_stage = form.cleaned_data['specific_stage']
            instance.has_taken_equity_in_participating_team = form.cleaned_data['has_taken_equity_in_participating_team']
            instance.does_provide_financial_supports = form.cleaned_data['does_provide_financial_supports']

            instance.amount_of_financial_supports = form.cleaned_data['amount_of_financial_supports']
            instance.period_of_engagement = form.cleaned_data['period_of_engagement']

            instance.does_provide_working_spaces = form.cleaned_data['does_provide_working_spaces']
            instance.is_own_working_space = form.cleaned_data['is_own_working_space']
            instance.does_provide_service_and_facility = form.cleaned_data['does_provide_service_and_facility']
            instance.service_and_facility_information = form.cleaned_data['specify_service']
            instance.working_spaces_information = json.dumps(working_form.cleaned_data)

            instance.attachments = form.cleaned_data['attachments']
            instance.status = form.cleaned_data['status']
            if instance.status == STATUS_PENDING and organization and organization.status == STATUS_PUBLISHED:
                instance.status = STATUS_PUBLISHED

            instance.facebook_url = form.cleaned_data['facebook_url']
            instance.twitter_url = form.cleaned_data['twitter_url']
            instance.linkedin_url = form.cleaned_data['linkedin_url']
            instance.homepage_url = form.cleaned_data['homepage_url']
            instance.instagram_url = form.cleaned_data['instagram_url']
            instance.other_channel = form.cleaned_data['other_channel']
            instance.description = form.cleaned_data['description']

            instance.is_register_to_nia = form.cleaned_data['is_register_to_nia']
            instance.is_partner = form.cleaned_data['is_partner']

            instance_image = instance._meta.get_field('image')
            if instance_image:
                instance_image.save_form_data(instance, form.cleaned_data['image'])

            instance_cover_image = instance._meta.get_field('cover_image')
            if instance_cover_image:
                instance_cover_image.save_form_data(instance, form.cleaned_data['cover_image'])

            instance.organization = organization
            instance.other_attachments_types = form.cleaned_data.get('other_attachments_types')
            instance.save()


            organization_section1_form.save_m2m()
            organization_attachment_form.save_m2m()

            instance.program_type.clear()
            for program_type in form.cleaned_data['program_type']:
                instance.program_type.add(program_type)

            instance.focus_sector.clear()
            for focus_sector in form.cleaned_data['focus_sector']:
                instance.focus_sector.add(focus_sector)

            instance.focus_industry.clear()
            for focus_industry in form.cleaned_data['focus_industry']:
                instance.focus_industry.add(focus_industry)

            instance.stage_of_participants.clear()
            for stage_of_participants in form.cleaned_data['stage_of_participants']:
                instance.stage_of_participants.add(stage_of_participants)

            instance.investment_type.clear()
            for investment_type in form.cleaned_data['investment_type']:
                instance.investment_type.add(investment_type)

            instance.investment_stage_type.clear()
            for investment_stage_type in form.cleaned_data['investment_stage_type']:
                instance.investment_stage_type.add(investment_stage_type)

            instance.attachments_types.clear()
            for attachments_types in form.cleaned_data['attachments_types']:
                instance.attachments_types.add(attachments_types)

            OrganizationStaff.objects.filter(organization=instance).delete()
            for people in form.cleaned_data['mentor']:
                people.organization = instance
                people.staff_status = OrganizationStaff.STATUS_MENTOR
                people.save()

            for people in form.cleaned_data['staff']:
                people.organization = instance
                people.staff_status = OrganizationStaff.STATUS_STAFF
                people.save()

            instance.batch_program.all().delete()
            for batch_form in batch_section1_formset:
                if batch_form.cleaned_data:

                    if not (batch_form.cleaned_data['amount_pre_seed_stage'] or batch_form.cleaned_data['amount_seed_stage'] or batch_form.cleaned_data['amount_pre_series_a_stage'] or batch_form.cleaned_data['amount_series_b_stage'] or batch_form.cleaned_data['amount_series_c_stage'] or batch_form.cleaned_data['amount_specific_stage'] or batch_form.cleaned_data['amount_total_stage']):
                        continue

                    batch = ProgramBatch()
                    batch.title = batch_form.cleaned_data['title']
                    batch.amount_pre_seed_stage = batch_form.cleaned_data['amount_pre_seed_stage'] if batch_form.cleaned_data['amount_pre_seed_stage'] else None
                    batch.amount_seed_stage = batch_form.cleaned_data['amount_seed_stage'] if batch_form.cleaned_data['amount_seed_stage'] else None
                    batch.amount_pre_series_a_stage = batch_form.cleaned_data['amount_pre_series_a_stage'] if batch_form.cleaned_data['amount_pre_series_a_stage'] else None
                    batch.amount_series_a_stage = batch_form.cleaned_data['amount_series_a_stage'] if batch_form.cleaned_data['amount_series_a_stage'] else None
                    batch.amount_series_b_stage = batch_form.cleaned_data['amount_series_b_stage'] if batch_form.cleaned_data['amount_series_b_stage'] else None
                    batch.amount_series_c_stage = batch_form.cleaned_data['amount_series_c_stage'] if batch_form.cleaned_data['amount_series_c_stage'] else None
                    batch.amount_specific_stage = batch_form.cleaned_data['amount_specific_stage'] if batch_form.cleaned_data['amount_specific_stage'] else None
                    batch.amount_total_stage = batch_form.cleaned_data['amount_total_stage'] if batch_form.cleaned_data['amount_total_stage'] else None
                    batch.program = instance
                    batch.save()

            for batch_form in batch_section2_formset:
                if batch_form.cleaned_data and batch_form.cleaned_data['title'] != '':
                    batch, created = ProgramBatch.objects.get_or_create(title=batch_form.cleaned_data['title'], program=instance)
                    batch.total_teams_applying = batch_form.cleaned_data['total_teams_applying'] if batch_form.cleaned_data['total_teams_applying'] else None
                    batch.total_teams_accepted = batch_form.cleaned_data['total_teams_accepted'] if batch_form.cleaned_data['total_teams_accepted'] else None
                    batch.total_participants_accepted = batch_form.cleaned_data['total_participants_accepted'] if batch_form.cleaned_data['total_participants_accepted'] else None
                    batch.total_graduated_teams_accepted = batch_form.cleaned_data['total_graduated_teams_accepted'] if batch_form.cleaned_data['total_graduated_teams_accepted'] else None
                    batch.total_training_program = batch_form.cleaned_data['total_training_program'] if batch_form.cleaned_data['total_training_program'] else None
                    batch.total_organized_event = batch_form.cleaned_data['total_organized_event'] if batch_form.cleaned_data['total_organized_event'] else None
                    batch.total_coached_staff = batch_form.cleaned_data['total_coached_staff'] if batch_form.cleaned_data['total_coached_staff'] else None
                    batch.total_assisting_staff = batch_form.cleaned_data['total_assisting_staff'] if batch_form.cleaned_data['total_assisting_staff'] else None
                    batch.total_approximated_products = batch_form.cleaned_data['total_approximated_products'] if batch_form.cleaned_data['total_approximated_products'] else None
                    batch.save()

            PartyPartnerParty.objects.filter(src=instance).exclude(dst=form.cleaned_data['partners']).delete()
            PartyPartnerParty.objects.filter(dst=instance).exclude(src=form.cleaned_data['partners']).delete()
            for partner in form.cleaned_data['partners']:
                if instance.id == partner.id:
                    continue
                if not PartyPartnerParty.objects.filter(
                        Q(src=instance, dst=partner) | Q(src=partner, dst=instance)).count():
                    PartyPartnerParty.objects.create(src=instance, dst=partner)

            admins = [admin.id for admin in form.cleaned_data['admins']]
            for admin in instance.admins.exclude(id__in=admins):
                instance.admins.remove(admin)

            admins = [admin.id for admin in instance.admins.all()]
            for admin in form.cleaned_data['admins'].exclude(id__in=admins):
                instance.admins.add(admin)


            # Add default admin when created first
            if is_new and not instance.created_by.is_staff and not instance.admins.all().count():
                instance.admins.add(instance.created_by)



            for participant_form in participant_organization_formset:
                if participant_form.cleaned_data and participant_form.cleaned_data.get('organization'):

                    if not participant_form.cleaned_data.get('organization'):
                        continue

                    if participant_form.cleaned_data['id']:
                        participant = OrganizationParticipate.objects.get(id=participant_form.cleaned_data['id'])
                    else:
                        participant = OrganizationParticipate()

                    if participant_form.cleaned_data.get('DELETE'):
                        if participant:
                            participant.delete()
                    else:
                        participant.src = participant_form.cleaned_data.get('organization')
                        participant.dst = instance
                        participant.month = participant_form.cleaned_data.get('month')
                        participant.swap = True
                        participant.save()


            message_success = get_success_message(instance, is_new, [])

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, program_render_reference(instance).replace("'", "\\'"))

            messages.success(request, message_success)

            if instance.status is not STATUS_PUBLISHED:
                #messages.warning(request, '%s is not publish organization.' % instance.name)
                messages.warning(request, _('%s is %s.') % (instance.name, dict(STATUS_CHOICES_DISPLAY)[int(instance.status)].lower()))

            return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:
            error_message = _('Your submission error. Please, check in tab has the icon') + '%s' % (
                '&nbsp;<span class="glyphicon glyphicon-exclamation-sign"></span>',
                # render_form_field_errors(form)
            )
            messages.error(request, error_message)

    else:

        initial = {
            'name': instance.name,
            'permalink': instance.permalink,
            'program_type': instance.program_type.all() if instance.id else None,
            'date_of_establishment': instance.date_of_establishment if instance.date_of_establishment else None,

            'organization': organization or instance.organization,

            'image': instance.image,
            'cover_image': instance.cover_image,
            'description': instance.description,

            'focus_sector': instance.focus_sector.all() if instance.id else None,
            'other_focus_sector': instance.other_focus_sector,

            'focus_industry': instance.focus_industry.all() if instance.id else None,
            'other_focus_industry': instance.other_focus_industry,

            'stage_of_participants': instance.stage_of_participants.all() if instance.id else None,

            'is_acting_as_an_investor': instance.is_acting_as_an_investor,
            'has_invited_in_participants_team': instance.has_invited_in_participants_team,

            'investment_type': instance.investment_type.all() if instance.id else None,
            'investment_stage_type': instance.investment_stage_type.all() if instance.id else None,

            'specific_stage': instance.specific_stage if instance.specific_stage else None,
            'has_taken_equity_in_participating_team': instance.has_taken_equity_in_participating_team,
            'does_provide_financial_supports': instance.does_provide_financial_supports,

            'amount_of_financial_supports': instance.amount_of_financial_supports if instance.amount_of_financial_supports else None,
            'period_of_engagement': instance.period_of_engagement if instance.period_of_engagement else None,

            'does_provide_working_spaces': instance.does_provide_working_spaces,
            'is_own_working_space': instance.is_own_working_space,

            'does_provide_service_and_facility': instance.does_provide_service_and_facility,
            'specify_service': instance.service_and_facility_information if instance.service_and_facility_information else None,

            'attachments_types': instance.attachments_types.all() if instance.id else None,
            'attachments': instance.attachments if instance.attachments else None,

            'status': instance.status,

            # External
            'facebook_url': instance.facebook_url,
            'twitter_url': instance.twitter_url,
            'linkedin_url': instance.linkedin_url,
            'homepage_url': instance.homepage_url,
            'instagram_url': instance.instagram_url,
            'other_channel': instance.other_channel,

            'admins': instance.admins.all().distinct() if instance.id else None,
            'partners': Party.objects.filter(Q(partner_dst__src=instance) | Q(partner_src__dst=instance)).distinct() if instance.id else None,

            'is_register_to_nia': instance.is_register_to_nia,
            'is_partner': instance.is_partner,
            'other_attachments_types': instance.other_attachments_types,

        }

        form = ProgramEditForm(instance, ModelClass, request.user, initial=initial)

        if instance.id:
            organization_section1_form = OrganizationSection1EditForm(instance=instance)
            organization_attachment_form = OrganizationAttachmentForm(instance=instance)

            batch_section1_initial = []
            batch_section2_initial = []
            for batch in instance.batch_program.filter(program=instance).order_by('title'):
                batch_section1_initial.append({
                    'title': batch.title,
                    'amount_pre_seed_stage': batch.amount_pre_seed_stage,
                    'amount_seed_stage': batch.amount_seed_stage,
                    'amount_pre_series_a_stage': batch.amount_pre_series_a_stage,
                    'amount_series_a_stage': batch.amount_series_a_stage,
                    'amount_series_b_stage': batch.amount_series_b_stage,
                    'amount_series_c_stage': batch.amount_series_c_stage,
                    'amount_specific_stage': batch.amount_specific_stage,
                    'amount_total_stage': batch.amount_total_stage,
                })

                batch_section2_initial.append({
                    'title': batch.title,
                    'total_teams_applying': batch.total_teams_applying,
                    'total_teams_accepted': batch.total_teams_accepted,
                    'total_participants_accepted': batch.total_participants_accepted,
                    'total_graduated_teams_accepted': batch.total_graduated_teams_accepted,
                    'total_training_program': batch.total_training_program,
                    'total_organized_event': batch.total_organized_event,
                    'total_coached_staff': batch.total_coached_staff,
                    'total_assisting_staff': batch.total_assisting_staff,
                    'total_approximated_products': batch.total_approximated_products
                })

            batch_section1_formset = BatchSection1Formset(initial=batch_section1_initial, prefix='batch_section1_formset')
            batch_section2_formset = BatchSection2Formset(initial=batch_section2_initial, prefix='batch_section2_formset')

            contact_person = json.loads(instance.contact_person or '{}')
            working_information = json.loads(instance.working_spaces_information or '{}')

            # initial = {}
            # if organization:
            #     phone_numbers = [phone_number['phone_number'] for phone_number in
            #                  organization.phone_number_of_organizations_headquarters]
            #
            #     initial={
            #         'name': organization.name,
            #         'register_number': organization.company_registration_number,
            #         'address': organization.location_of_organizations_headquarters,
            #         'tel': ','.join(phone_numbers),
            #         'mobile': ','.join(phone_numbers),
            #         'email': organization.email_of_contact_person,
            #         'website': organization.homepage_url,
            #         'sns': organization.social_networks
            #     }

            contact_form = ContactPersonInformationForm(initial=contact_person, prefix='contact_form')
            working_form = OrganizationInformationForm(initial=working_information, prefix='working_form')

            initial['mentor'] = OrganizationStaff.objects.filter(organization=instance, staff_status=OrganizationStaff.STATUS_MENTOR)
            initial['staff'] = OrganizationStaff.objects.filter(organization=instance, staff_status=OrganizationStaff.STATUS_STAFF)

            participant_organization_initial = []
            if instance.participate_dst.filter(dst=instance).count():
                for participant in instance.participate_dst.filter(dst=instance):
                    participant_organization_initial.append({
                        'id': participant.id,
                        'organization': participant.src,
                        'month': participant.month,
                        'status': participant.status,
                    })
            else:
                pass

            participant_organization_formset = ParticipantOrganizationFormSet(initial=participant_organization_initial,
                                                                              prefix='participant_organization')

        else:
            organization_section1_form = OrganizationSection1EditForm(instance=instance)
            organization_attachment_form = OrganizationAttachmentForm(instance=instance)

            batch_section1_formset = BatchSection1Formset(prefix='batch_section1_formset')
            batch_section2_formset = BatchSection2Formset(prefix='batch_section2_formset')


            if organization:
                phone_numbers = [phone_number['phone_number'] for phone_number in organization.phone_number_of_organizations_headquarters]

                contact_form = ContactPersonInformationForm(initial={
                    'name': organization.name_of_representative,
                    'tel': ','.join(phone_numbers),
                    'mobile': ','.join(phone_numbers),
                    'email': organization.email_of_contact_person
                }, prefix='contact_form')
                working_form = OrganizationInformationForm(prefix='working_form')
            else:
                contact_form = ContactPersonInformationForm(initial={}, prefix='contact_form')
                working_form = OrganizationInformationForm(initial={}, prefix='working_form')

            participant_organization_formset = ParticipantOrganizationFormSet(initial=[], prefix='participant_organization')

    template = 'organization/program/form.html'
    # if request.GET.get('_popup'):
    #     template = 'organization/program/inline_form.html'

    return render(request, template, {
        'form': form,
        'type_of_organization': TYPE_PROGRAM,
        'type_of_organization_name': _('Program'),
        'organization_section1_form': organization_section1_form,
        'organization_attachment_form': organization_attachment_form,
        'contact_form': contact_form,
        'working_form': working_form,
        'batch_section1_formset': batch_section1_formset,
        'batch_section2_formset': batch_section2_formset,
        'organization': organization,
        'is_from_reference': is_from_reference,
        'participant_organization_formset': participant_organization_formset,
    })


@login_required
def program_create_instance(request):
    return _program_create(request, instance=None)


@login_required
def program_edit(request, program_id):

    instance = get_object_or_404(Program, id=program_id)

    # Check permission
    user_can_edit_check(request.user, instance)

    return _program_create(request, instance=instance)

@login_required
def program_inline_create(request, instance=None):
        # Config for reuse
    ModelClass = Program
    instance = instance or ModelClass()
    type_of_organization = TYPE_PROGRAM

    win_name = request.GET.get('_win_name') or request.POST.get('_win_name') or 'id_dst'
    no_script = request.GET.get('no_script') or request.POST.get('no_script') or 0
    return_display_name = request.GET.get('return_display_name') or request.POST.get('return_display_name') or 0
    is_mockup = request.GET.get('is_mockup') or request.POST.get('is_mockup') or 0

    if request.method == 'POST':
        form = ProgramInlineEditForm(instance, ModelClass, request.user, request.POST)

        is_new = form.is_new()

        if form.is_valid():
            if not instance.id:
                instance.created_by = request.user

            instance.name = form.cleaned_data['name']
            instance.type_of_organization = type_of_organization

            instance_set_permalink(instance, instance.name, prefix='inline')
            instance.status = STATUS_DRAFT
            instance.is_mockup = is_mockup
            instance.save()

            # Add default admin when created first
            if is_new and not instance.created_by.is_staff and not instance.admins.all().count():
                instance.admins.add(instance.created_by)

            message_success = get_success_message(instance, is_new, [instance.type_of_organization])

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, organization_render_reference(instance).replace("'", "\\'"))


            if request.GET.get('_inline') or request.POST.get('_inline'):
                form.inst = instance
            else:
                messages.success(request, message_success)
                return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:
            print 'dddddd'
    else:
        initial = {
            # Internal
            'name': instance.name,
            'status': instance.status,
            'type_of_organization': type_of_organization
        }

        if instance.id:
            pass
        else:
            initial['status'] = process_status(request.user, initial['status'], True)


        form = ProgramInlineEditForm(instance, ModelClass, request.user, initial=initial)

    return render(request, 'organization/program/inline_form.html', {
        'form': form,
        'win_name': win_name,
        'no_script': no_script,
        'return_display_name': return_display_name,
        'is_mockup': is_mockup,
    })


@csrf_protect
def inline_password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_context': extra_context
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)

            field_id = request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins'

            staff = form.staff
            return HttpResponseRedirect('%s&staff_id=%s&field_id=%s' % (post_reset_redirect, staff.id, field_id))
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def staff_inline_invite(request, staff_id=None):

    post_reset_redirect = '%s?success=1' % reverse('staff_inline_invitation')
    if request.GET.get('next'):
        post_reset_redirect = '%s&next=%s' % (post_reset_redirect, urllib.quote_plus(request.GET.get('next')))

    if request.GET.get('success'):

        messages.success(request, _('The email invitation has been send.'))
        return render(request, 'organization/staff/inline_invite_form.html', {
            'form': StaffInviteForm(),
            'success': True,
            'staff_id': request.GET.get('staff_id'),
            'field_id': request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins',
            'create': request.POST.get('create') or request.GET.get('create') or False,
            'title': request.POST.get('title') or request.GET.get('title') or '',
            'manage': request.POST.get('manage') or request.GET.get('manage') or ''
        })

    return inline_password_reset(request,
        template_name='organization/staff/inline_invite_form.html',
        email_template_name='account/email/invite_email.html',
        subject_template_name='account/email/invite_email_subject.txt',
        password_reset_form=StaffInviteForm,
        post_reset_redirect=post_reset_redirect,
        extra_context={
            'field_id': request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins',
            'create': request.POST.get('create') or request.GET.get('create') or False,
            'title': request.POST.get('title') or request.GET.get('title') or '',
            'manage': request.POST.get('manage') or request.GET.get('manage') or ''
        }
    )

def staff_edit(request, staff_id):
    # TODO: render form with 'organization/staff/inline_invite_form.html' and StaffInviteForm
    return staff_inline_invite(request, staff_id)




@login_required
def in_the_news_create(request, organization_id=None, instance=None):
    # Config for reuse
    ModelClass = InTheNews
    instance = instance or ModelClass()

    if request.method == 'POST':

        form = InTheNewsEditForm(instance, ModelClass, request.user, request.POST)

        is_new = form.is_new()

        if form.is_valid():

            instance.title = form.cleaned_data['title']
            instance.description = form.cleaned_data['description']
            instance.url = form.cleaned_data['url']
            instance.date = form.cleaned_data['date']

            print instance.date

            instance_image = instance._meta.get_field('image')
            if instance_image:
                instance_image.save_form_data(instance, form.cleaned_data['image'])


            instance.save()


            message_success = get_success_message(instance, is_new, [])

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, in_the_news_render_reference(instance).replace("'", "\\'"))

            messages.success(request, message_success)

            return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')


    else:
        initial = {
            'title': instance.title,
            'description': instance.description,
            'image': instance.image,
            'url': instance.url,
            'date': instance.date,
        }


        form = InTheNewsEditForm(instance, ModelClass, request.user, initial=initial)


    return render(request, 'organization/in_the_news/form.html', {
        'form': form,
    })


@login_required
def in_the_news_edit(request, in_the_news_id):

    instance = get_object_or_404(InTheNews, id=in_the_news_id)
    return in_the_news_create(request, instance=instance)