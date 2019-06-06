from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import QuerySet, Q
from django import forms
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from account.functions import user_can_edit_check

from common.constants import STATUS_PUBLISHED, STATUS_CHOICES_DISPLAY
from common.decorators import statistic
from common.functions import process_status, get_success_message, camelcase_to_underscore, instance_set_permalink, \
    get_point
from common.templatetags.common_tags import render_form_field_errors
from organization.constants import TAB_LIST_CONFIG, PROMOTE_LIST_CONFIG
from organization.forms import OrganizationEditForm, OrganizationEditInlineForm, \
    TeamInformationForm, OrganizationSection1EditForm, OrganizationSection2EditForm, \
    OrganizationSection3EditForm, OrganizationSection4EditForm, OrganizationSection5EditForm, \
    PhoneNumberOfOrganizationsHeadquartersForm, LocationOfOrganizationsOperatingFacilitiesForm, \
    MeasurementYearValuesForm, Top3MajorInvestorsYearAndAmountForm, Top3MajorDonorsYearAndAmountForm, JobEditForm
from organization.functions import organization_render_reference, job_render_reference
from organization.models import Organization, Job

import json
from party.models import Party
from relation.models import OrganizationHasPeople, PartyPartnerParty, PartySupportParty, PartyReceivedFundingParty, \
    PartyInvestParty, PartyReceivedInvestingParty
from special.models import Special
from taxonomy.models import OrganizationRole


def instance_save_formset(instance, field_name, formset, formset_field_list):
    pass


@login_required
def organization_create(request, type_of_organization, instance=None, build_point_from_initial=False):

    # Extra
    if (instance and not instance.id) and type_of_organization not in dict(Organization.TYPE_CHOICES).keys():
        raise Http404
    elif type_of_organization not in dict(Organization.TYPE_CHOICES).keys():
        type_of_organization = settings.DEFAULT_TYPE_RECEIVER

    type_of_organization_name = dict(Organization.TYPE_CHOICES)[type_of_organization]


    # Config for reuse
    ModelClass = Organization
    instance = instance or ModelClass(type_of_organization=type_of_organization)

    # Formset
    TeamInformationFormSet = formset_factory(TeamInformationForm, extra=1, can_delete=True)
    PhoneNumberOfOrganizationsHeadquartersFormSet = formset_factory(PhoneNumberOfOrganizationsHeadquartersForm, extra=1, can_delete=True)
    LocationOfOrganizationsOperatingFacilitiesFormSet = formset_factory(LocationOfOrganizationsOperatingFacilitiesForm, extra=1, can_delete=True)
    MeasurementYearValuesFormSet = formset_factory(MeasurementYearValuesForm, extra=1, can_delete=True)

    Top3MajorInvestorsYearAndAmountFormSet = formset_factory(Top3MajorInvestorsYearAndAmountForm, extra=3, can_delete=True, max_num=3)
    Top3MajorDonorsYearAndAmountFormSet = formset_factory(Top3MajorDonorsYearAndAmountForm, extra=3, can_delete=True, max_num=3)


    if request.method == 'POST':

        instance.type_of_organization = type_of_organization

        form = OrganizationEditForm(instance, ModelClass, request.user, request.POST)
        # Extra form
        organization_section1_form = OrganizationSection1EditForm(request.POST, instance=instance)
        organization_section2_form = OrganizationSection2EditForm(request.POST, instance=instance)
        organization_section3_form = OrganizationSection3EditForm(request.POST, instance=instance)
        organization_section4_form = OrganizationSection4EditForm(request.POST, instance=instance)
        organization_section5_form = OrganizationSection5EditForm(request.POST, instance=instance)

        # Formset
        team_information_formset = TeamInformationFormSet(request.POST, prefix='team_information')
        phone_number_of_organizations_headquarters_formset = PhoneNumberOfOrganizationsHeadquartersFormSet(request.POST, prefix='phone_number_of_organizations_headquarters')
        location_of_organizations_operating_facilities_formset = LocationOfOrganizationsOperatingFacilitiesFormSet(request.POST,
                                                                                                                   prefix='location_of_organizations_operating_facilities')
        measurement_year_values_formset = MeasurementYearValuesFormSet(request.POST, prefix='measurement_year_values')
        top_3_major_investors_year_and_amount_formset = Top3MajorInvestorsYearAndAmountFormSet(request.POST, prefix='top_3_major_investors_year_and_amount')
        top_3_major_donors_year_and_amount_formset = Top3MajorDonorsYearAndAmountFormSet(request.POST, prefix='top_3_major_donors_year_and_amount')

        is_new = form.is_new()



        # Formset
        if form.is_valid() and \
           organization_section1_form.is_valid() and organization_section2_form.is_valid() and \
           organization_section3_form.is_valid() and organization_section4_form.is_valid() and \
           organization_section5_form.is_valid() and \
           team_information_formset.is_valid() and \
           phone_number_of_organizations_headquarters_formset.is_valid() and \
           location_of_organizations_operating_facilities_formset.is_valid() and \
           measurement_year_values_formset.is_valid() and \
           top_3_major_investors_year_and_amount_formset.is_valid() and \
           top_3_major_donors_year_and_amount_formset.is_valid():

            # Before save m2m
            organization_section1_form.save(commit=False)
            organization_section2_form.save(commit=False)
            organization_section3_form.save(commit=False)
            organization_section4_form.save(commit=False)
            organization_section5_form.save(commit=False)


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
                instance.point = get_point(form_list, settings.POINT, [r.id for r in form.cleaned_data['organization_roles']], update=True)
            else:
                instance.point = 0

            # Relation
            if not instance.created_by_id:
                instance.created_by = request.user

            # Internal
            instance.permalink = form.cleaned_data['permalink']
            instance.name = form.cleaned_data['name']
            instance.summary = form.cleaned_data['summary']
            instance.kind = form.cleaned_data['kind']
            instance.description = form.cleaned_data['description']

            instance_image = instance._meta.get_field('image')
            if instance_image:
                instance_image.save_form_data(instance, form.cleaned_data['image'])

            instance_images = instance._meta.get_field('images')
            if instance_images:
                instance_images.save_form_data(instance, form.cleaned_data['images'])

            # External
            instance.facebook_url = form.cleaned_data['facebook_url']
            instance.twitter_url = form.cleaned_data['twitter_url']
            instance.linkedin_url = form.cleaned_data['linkedin_url']
            instance.homepage_url = form.cleaned_data['homepage_url']

            # Meta
            instance.status = int(form.cleaned_data['status'])

            if not instance.published and instance.status == STATUS_PUBLISHED:
                instance.published = timezone.now()
                instance.published_by = request.user

            instance.country = form.cleaned_data['country']
            instance.organization_primary_role = form.cleaned_data['organization_primary_role']

            instance.product_launch = form.cleaned_data['product_launch']
            instance.funding = form.cleaned_data['funding']
            instance.request_funding = form.cleaned_data['request_funding']

            instance.deal_size_start = form.cleaned_data['deal_size_start']
            instance.deal_size_end = form.cleaned_data['deal_size_end']


            # Formset
            team_information = []
            for team_information_form in team_information_formset:

                if team_information_form.cleaned_data and not team_information_form.cleaned_data.get('DELETE'):
                    team_information.append({
                        'name': team_information_form.cleaned_data['name'],
                        'title': team_information_form.cleaned_data['title']
                    })
            instance.team_information = team_information

            phone_number_of_organizations_headquarters = []
            for phone_number_of_organizations_headquarters_form in phone_number_of_organizations_headquarters_formset:

                if phone_number_of_organizations_headquarters_form.cleaned_data and not phone_number_of_organizations_headquarters_form.cleaned_data.get('DELETE'):
                    phone_number_of_organizations_headquarters.append({
                        'phone_number': phone_number_of_organizations_headquarters_form.cleaned_data['phone_number'],
                    })
            instance.phone_number_of_organizations_headquarters = phone_number_of_organizations_headquarters

            location_of_organizations_operating_facilities = []
            for location_of_organizations_operating_facilities_form in location_of_organizations_operating_facilities_formset:

                if location_of_organizations_operating_facilities_form.cleaned_data and not location_of_organizations_operating_facilities_form.cleaned_data.get(
                        'DELETE'):
                    location_of_organizations_operating_facilities.append({
                        'address': location_of_organizations_operating_facilities_form.cleaned_data['address'],
                    })
            instance.location_of_organizations_operating_facilities = location_of_organizations_operating_facilities

            measurement_year_values = []
            for measurement_year_values_form in measurement_year_values_formset:

                if measurement_year_values_form.cleaned_data and not measurement_year_values_form.cleaned_data.get(
                        'DELETE'):
                    measurement_year_values.append({
                        'year_of_datapoint': measurement_year_values_form.cleaned_data['year_of_datapoint'],
                        'value_of_impact_1': measurement_year_values_form.cleaned_data['value_of_impact_1'],
                        'value_of_impact_2': measurement_year_values_form.cleaned_data['value_of_impact_2'],
                        'value_of_impact_3': measurement_year_values_form.cleaned_data['value_of_impact_3'],
                    })
            instance.measurement_year_values = measurement_year_values

            top_3_major_investors_year_and_amount = []
            for top_3_major_investors_year_and_amount_form in top_3_major_investors_year_and_amount_formset:

                if top_3_major_investors_year_and_amount_form.cleaned_data and not top_3_major_investors_year_and_amount_form.cleaned_data.get(
                        'DELETE'):
                    top_3_major_investors_year_and_amount.append({
                        'title': top_3_major_investors_year_and_amount_form.cleaned_data['title']
                    })
            instance.top_3_major_investors_year_and_amount = top_3_major_investors_year_and_amount

            top_3_major_donors_year_and_amount = []
            for top_3_major_donors_year_and_amount_form in top_3_major_donors_year_and_amount_formset:

                if top_3_major_donors_year_and_amount_form.cleaned_data and not top_3_major_donors_year_and_amount_form.cleaned_data.get('DELETE'):
                    top_3_major_donors_year_and_amount.append({
                        'title': top_3_major_donors_year_and_amount_form.cleaned_data['title']
                    })
            instance.top_3_major_donors_year_and_amount = top_3_major_donors_year_and_amount


            instance.save()

            organization_section1_form.save_m2m()
            organization_section2_form.save_m2m()
            organization_section3_form.save_m2m()
            organization_section4_form.save_m2m()
            organization_section5_form.save_m2m()

            # Taxonomy
            instance.type_of_needs.clear()
            for type_of_need in form.cleaned_data['type_of_needs']:
                instance.type_of_needs.add(type_of_need)

            instance.type_of_supports.clear()
            for type_of_support in form.cleaned_data['type_of_supports']:
                instance.type_of_supports.add(type_of_support)

            instance.topics.clear()
            for topic in form.cleaned_data['topics']:
                instance.topics.add(topic)

            instance.organization_roles.clear()
            for organization_role in form.cleaned_data['organization_roles']:
                instance.organization_roles.add(organization_role)

            instance.type_of_supports.clear()
            for type_of_support in form.cleaned_data['type_of_supports']:
                instance.type_of_supports.add(type_of_support)

            instance.organization_types.clear()
            for organization_type in form.cleaned_data['organization_types']:
                instance.organization_types.add(organization_type)

            instance.investor_types.clear()
            for investor_type in form.cleaned_data['investor_types']:
                instance.investor_types.add(investor_type)

            instance.growth_stage.clear()

            try:
                for growth_stage in form.cleaned_data['growth_stage']:
                    instance.growth_stage.add(growth_stage)
            except TypeError:
                if form.cleaned_data['growth_stage']:
                    instance.growth_stage.add(form.cleaned_data['growth_stage'])


            # Specail

            if request.user.is_staff:
                specials = [special.id for special in form.cleaned_data['specials']]
                for special in instance.specials.exclude(id__in=specials):
                    instance.specials.remove(special)

                specials = [special.id for special in instance.specials.all()]
                for special in form.cleaned_data['specials'].exclude(id__in=specials):
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

            admins = [admin.id for admin in instance.admins.all()]
            for admin in form.cleaned_data['admins'].exclude(id__in=admins):
                instance.admins.add(admin)


            # Add default admin when created first
            if is_new and not instance.created_by.is_staff and not instance.admins.all().count():
                instance.admins.add(instance.created_by)


            portfolios = [portfolio.id for portfolio in form.cleaned_data['portfolios']]
            instance.portfolios.exclude(id__in=portfolios).delete()

            portfolios = [portfolio.id for portfolio in instance.portfolios.all()]
            for portfolio in form.cleaned_data['portfolios'].exclude(id__in=portfolios):
                instance.portfolios.add(portfolio)


            jobs = [job.id for job in form.cleaned_data['jobs']]
            instance.jobs.exclude(id__in=jobs).delete()

            jobs = [job.id for job in instance.jobs.all()]
            for job in form.cleaned_data['jobs'].exclude(id__in=jobs):
                instance.jobs.add(job)


            OrganizationHasPeople.objects.filter(src=instance).exclude(dst=form.cleaned_data['peoples']).delete()
            for people in form.cleaned_data['peoples']:
                OrganizationHasPeople.objects.get_or_create(src=instance, dst=people)

            PartyPartnerParty.objects.filter(src=instance).exclude(dst=form.cleaned_data['partners']).delete()
            PartyPartnerParty.objects.filter(dst=instance).exclude(src=form.cleaned_data['partners']).delete()
            for partner in form.cleaned_data['partners']:
                if instance.id == partner.id:
                    continue
                if not PartyPartnerParty.objects.filter(Q(src=instance, dst=partner) | Q(src=partner, dst=instance)).count():
                    PartyPartnerParty.objects.create(src=instance, dst=partner)



            PartySupportParty.objects.filter(dst=instance).exclude(src=form.cleaned_data['supporters']).delete()
            for supporter in form.cleaned_data['supporters']:
                if instance.id == supporter.id:
                    continue
                PartySupportParty.objects.get_or_create(src=supporter, dst=instance, defaults={
                    'src': supporter,
                    'dst': instance,
                    'swap': True
                })



            PartySupportParty.objects.filter(src=instance).exclude(dst=form.cleaned_data['recipients']).delete()
            for recipient in form.cleaned_data['recipients']:
                if instance.id == recipient.id:
                    continue
                PartySupportParty.objects.get_or_create(src=instance, dst=recipient)



            PartyInvestParty.objects.filter(dst=instance).exclude(src=form.cleaned_data['investors']).delete()
            for investor in form.cleaned_data['investors']:
                if instance.id == investor.id:
                    continue
                PartyInvestParty.objects.get_or_create(src=investor, dst=instance, defaults={
                    'src': investor,
                    'dst': instance,
                    'swap': True
                })

            PartyInvestParty.objects.filter(src=instance).exclude(dst=form.cleaned_data['invest_recipients']).delete()
            for invest_recipient in form.cleaned_data['invest_recipients']:
                if instance.id == invest_recipient.id:
                    continue
                PartyInvestParty.objects.get_or_create(src=instance, dst=invest_recipient)



            received_fundings = [received_funding.id for received_funding in form.cleaned_data['received_fundings']]
            PartyReceivedFundingParty.objects.filter(src__id=instance.id).exclude(id__in=received_fundings).delete()
            for received_funding in form.cleaned_data['received_fundings']:
                if not received_funding.src:
                    received_funding.src = instance.party_ptr
                    received_funding.save()

            gived_fundings = [gived_funding.id for gived_funding in form.cleaned_data['gived_fundings']]
            PartyReceivedFundingParty.objects.filter(dst__id=instance.id).exclude(id__in=gived_fundings).delete()
            for gived_funding in form.cleaned_data['gived_fundings']:
                if not gived_funding.dst:
                    gived_funding.dst = instance.party_ptr
                    gived_funding.swap = True
                    gived_funding.save()


            received_investings = [received_investing.id for received_investing in form.cleaned_data['received_investings']]
            PartyReceivedInvestingParty.objects.filter(src__id=instance.id).exclude(id__in=received_investings).delete()
            for received_investing in form.cleaned_data['received_investings']:
                if not received_investing.src:
                    received_investing.src = instance.party_ptr
                    received_investing.save()

            gived_investings = [gived_investing.id for gived_investing in form.cleaned_data['gived_investings']]
            PartyReceivedInvestingParty.objects.filter(dst__id=instance.id).exclude(id__in=gived_investings).delete()
            for gived_investing in form.cleaned_data['gived_investings']:
                if not gived_investing.dst:
                    gived_investing.dst = instance.party_ptr
                    gived_investing.swap = True
                    gived_investing.save()



            message_success = get_success_message(instance, is_new, [type_of_organization])

            if settings.THANK_AFTER_CREATE and is_new:
                message_success = '%s<script type="text/javascript">$(\'#thankyou-modal\').modal(\'show\')</script>' % message_success

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, organization_render_reference(instance).replace("'", "\\'"))

            messages.success(request, message_success)
            if instance.status is not 1:
                #messages.warning(request, '%s is not publish organization.' % instance.name)
                messages.warning(request, _('%s is %s.') % (instance.name, dict(STATUS_CHOICES_DISPLAY)[instance.status].lower()))

            return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:

            error_message = _('Your submission error. Please, check in tab has the icon') + '%s %s' % (
                '&nbsp;<span class="glyphicon glyphicon-exclamation-sign"></span>',
                render_form_field_errors(form)
            )

            messages.error(request, error_message)


    else:

        organization_primary_role = request.GET.get('organization_primary_role', None)
        initial = {
            # Internal
            'kind': instance.kind if instance.id else None,
            'permalink': instance.permalink,
            'name': instance.name or request.GET.get('name', ''),
            'summary': instance.summary,
            'description': instance.description,
            'image': instance.image,
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

            'deal_size_start': instance.deal_size_start,
            'deal_size_end': instance.deal_size_end
        }

        if type_of_organization == Organization.TYPE_SUPPORTING_ORGANIZATION:
            initial['kind'] = Organization.KIND_ORGANIZATION

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

            if instance.type_of_organization in [Organization.TYPE_SUPPORTING_ORGANIZATION]:
                initial['growth_stage'] = instance.growth_stage.all()
            else:
                try:
                    initial['growth_stage'] = instance.growth_stage.all()[0]
                except IndexError:
                    pass


            UserModel = get_user_model()

            # Relate (Holy query)
            initial['admins'] = instance.admins.all().distinct()
            initial['portfolios'] = instance.portfolios.all().distinct()
            initial['jobs'] = instance.jobs.all().distinct()

            initial['peoples'] = UserModel.objects.filter(organization_has_people_dst__src=instance).distinct()
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


        else:
            initial['status'] = process_status(request.user, initial['status'], True)


        form = OrganizationEditForm(instance, ModelClass, request.user, initial=initial)
        # Extra form
        organization_section1_form = OrganizationSection1EditForm(instance=instance)
        organization_section2_form = OrganizationSection2EditForm(instance=instance)
        organization_section3_form = OrganizationSection3EditForm(instance=instance)
        organization_section4_form = OrganizationSection4EditForm(instance=instance)
        organization_section5_form = OrganizationSection5EditForm(instance=instance)

        organization_section3_form.fields['financial_statement_review'].widget = forms.CheckboxInput()
        if request.user.is_authenticated():
            user = request.user
        if user.is_staff is False:
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


    return render(request, 'organization/form.html', {
        'form': form,
        'type_of_organization': type_of_organization,
        'type_of_organization_name': type_of_organization_name,
        # Section
        'organization_section1_form': organization_section1_form,
        'organization_section2_form': organization_section2_form,
        'organization_section3_form': organization_section3_form,
        'organization_section4_form': organization_section4_form,
        'organization_section5_form': organization_section5_form,
        # Formset
        'team_information_formset': team_information_formset,
        'phone_number_of_organizations_headquarters_formset': phone_number_of_organizations_headquarters_formset,
        'location_of_organizations_operating_facilities_formset': location_of_organizations_operating_facilities_formset,
        'measurement_year_values_formset': measurement_year_values_formset,
        'top_3_major_investors_year_and_amount_formset': top_3_major_investors_year_and_amount_formset,
        'top_3_major_donors_year_and_amount_formset': top_3_major_donors_year_and_amount_formset,
    })

@login_required
def organization_edit(request, organization_id=None):

    organization = get_object_or_404(Organization, id=organization_id)

    # Check permission
    user_can_edit_check(request, organization)

    return organization_create(request, organization.type_of_organization, organization)


@login_required
def organization_inline_create(request, instance=None):

    # Config for reuse
    ModelClass = Organization
    instance = instance or ModelClass()

    win_name = request.GET.get('_win_name') or request.POST.get('_win_name') or 'id_dst'
    no_script = request.GET.get('no_script') or request.POST.get('no_script') or 0
    return_display_name = request.GET.get('return_display_name') or request.POST.get('return_display_name') or 0

    type_of_organization = request.GET.get('type_of_organization')

    if request.method == 'POST':


        form = OrganizationEditInlineForm(instance, ModelClass, request.user, request.POST)

        is_new = form.is_new()

        if form.is_valid():

            # Relation
            if not instance.created_by_id:
                instance.created_by = request.user

            instance.name = form.cleaned_data['name']

            primary_role = form.cleaned_data['type_of_organization']

            if primary_role in [Organization.TYPE_SUPPORTING_ORGANIZATION, Organization.TYPE_INVESTOR]:

                primary_role = Organization.TYPE_SUPPORTING_ORGANIZATION
            else:
                primary_role = Organization.DEFAULT_TYPE_RECEIVER

            instance.type_of_organization = primary_role

            primary_role = OrganizationRole.objects.get(permalink=primary_role)
            instance.organization_primary_role = primary_role


            instance_set_permalink(instance, instance.name)

            instance_image = instance._meta.get_field('image')
            if instance_image:
                instance_image.save_form_data(instance, form.cleaned_data['image'])

            instance.save()

            instance.organization_roles.add(primary_role)

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
            'type_of_organization': type_of_organization
        }

        if instance.id:
            pass
        else:
            initial['status'] = process_status(request.user, initial['status'], True)


        form = OrganizationEditInlineForm(instance, ModelClass, request.user, initial=initial)

    return render(request, 'organization/inline_form.html', {
        'form': form,
        'win_name': win_name,
        'no_script': no_script,
        'return_display_name': return_display_name
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

        form = JobEditForm(instance, ModelClass, request.user, request.POST, user=request.user)

        is_new = form.is_new()

        is_valid = form.is_valid()
        if is_valid:

            if not instance.id:
                instance.created_by = request.user

            instance.title = form.cleaned_data['title']
            instance.contact_information = form.cleaned_data['contact_information']
            instance.description = form.cleaned_data['description']
            instance.role = form.cleaned_data['role']
            instance.position = form.cleaned_data['position']
            instance.salary_min = form.cleaned_data['salary_min']
            instance.salary_max = form.cleaned_data['salary_max']
            instance.equity_min = form.cleaned_data['equity_min']
            instance.equity_max = form.cleaned_data['equity_max']
            instance.remote = form.cleaned_data['remote'] == 'True'
            instance.years_of_experience = form.cleaned_data['years_of_experience']
            instance.country = form.cleaned_data['country']
            instance.location = form.cleaned_data['location']
            instance.skills = form.cleaned_data['skills']
            instance.status = int(form.cleaned_data['status'])

            instance.save()

            message_success = get_success_message(instance, is_new, [])

            form_organization = form.cleaned_data.get('organization')

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
            'position': instance.position,
            'salary_min': instance.salary_min,
            'salary_max': instance.salary_max,
            'equity_min': instance.equity_min,
            'equity_max': instance.equity_max,
            'remote': bool(instance.remote),
            'years_of_experience': instance.years_of_experience,
            'country': instance.country or (organization and organization.country),
            'location': instance.location,
            'skills': instance.skills,
            'status': instance.status,
        }


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

def job_list(request):
    return render(request, 'organization/job/list.html')