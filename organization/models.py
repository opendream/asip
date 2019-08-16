# -*- coding: utf-8 -*-
import ast
from datetime import timedelta
import inspect
import json
import pickle
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models, IntegrityError
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from haystack.inputs import Raw
from haystack.query import SearchQuerySet
from djmoney.models.fields import MoneyField
import tagging

from ckeditor.fields import RichTextField
from common.constants import STATUS_PENDING, STATUS_DRAFT, SUMMARY_MAX_LENGTH, STATUS_PUBLISHED, STATUS_CHOICES, \
    TYPE_SOCIAL_ENTERPRISE, TYPE_STARTUP, TYPE_SUPPORTING_ORGANIZATION, TYPE_INVESTOR, TYPE_PROGRAM, \
    TYPE_CHOICES, EXPAND_TYPE_CHOICES
from common.forms import BetterDecimalField, BetterPositiveIntegerField
from common.functions import instance_get_thumbnail, camelcase_to_underscore, convert_money

from common.models import AbstractPermalink, CommonTrashModel, CommonModel, CachedModel, PriorityModel, StatisitcAccess
from multiselectfield import MultiSelectField
from party.models import Party

import files_widget
from relation.models import BaseRelation
from tagging_autocomplete_tagit.models import TagAutocompleteTagItField
from taxonomy.models import Location, JobRole

USER_MODEL = settings.AUTH_USER_MODEL


def formset_getter(instance, field_name):

    field_name = 'store_%s' % field_name
    value = getattr(instance, field_name) or '[]'
    setattr(instance, field_name, value)

    return ast.literal_eval(value)

def formset_setter(instance, field_name, value):

    field_name = 'store_%s' % field_name
    value = value or []
    setattr(instance, field_name, value)


# Section 1
class AbstractOrganizationSection1(models.Model):

    class Meta:
        abstract = True

    report_start_date = models.DateField(verbose_name=_('Report Start Date'), null=True, blank=True,
        help_text=_('Start date of the reporting period for this IRIS report.')
    )
    report_end_date = models.DateField(verbose_name=_('Report End Date'), null=True, blank=True,
        help_text=_('End date of the reporting period for this IRIS report.')
    )

    # Duplicates
    # name_of_organization = name
    # organization_web_address = homepage_url

    year_founded = models.PositiveSmallIntegerField(verbose_name=_('Year Founded'), null=True, blank=True,
        help_text=_('Year the organization was founded.')
    )
    name_of_representative = models.CharField(verbose_name=_('Name of representative'), null=True, blank=True, max_length=255)

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('N', _('Prefer not to say')),
    )
    gender_of_representative = models.CharField(verbose_name=_('Gender of representative'), null=True, blank=True, max_length=1, choices=GENDER_CHOICES)
    brief_bio_of_representative = RichTextField(verbose_name=_('Brief bio of representative'), null=True, blank=True, config_name='minimal')

    LEGAL_STRUCTURE_CHOICES = (
        ('1', _('Corporation')),
        ('2', _('Limited Liability Company')),
        ('3', _('Non-Profit/Foundation/Association')),
        ('4', _('Partnership')),
        ('5', _('Sole-proprietorship')),
        ('6', _('Cooperative')),
        ('Other', _('Other'))
    )
    legal_structure = models.CharField(verbose_name=_('Legal Structure'), null=True, blank=True, max_length=255, choices=LEGAL_STRUCTURE_CHOICES,
        help_text=_('Current legal structure of the organization.')
    )
    location_of_organizations_headquarters = models.CharField(verbose_name=_("Location of Organization's Headquarters"), null=True, blank=True, max_length=255)
    store_phone_number_of_organizations_headquarters = models.TextField(null=True, blank=True)  # formset
    store_email_of_organizations_headquarters = models.EmailField(
        verbose_name=_('Email of Organization'),
        max_length=255,
        null=True,
        blank=True
    )

    title_of_contact_person = models.TextField(null=True, blank=True)
    email_of_contact_person = models.EmailField(
        verbose_name=_('Email of Contact Person'),
        max_length=255,
        null=True,
        blank=True
    )
    phone_number_of_contact_person = models.TextField(null=True, blank=True)

    store_location_of_organizations_operating_facilities = models.TextField(verbose_name=_("Location of Organization's Operating Facilities"), null=True, blank=True) # formset

    name_of_referring_organization = models.CharField(verbose_name=_("Name of referring organization"), null=True, blank=True, max_length=255)
    contact_information_of_referring_organization = models.CharField(verbose_name=_("Contact information of referring organization"), null=True, blank=True, max_length=255)

    sector_activities = models.ManyToManyField('taxonomy.Topic', verbose_name=_('Sector Activities'),  null=True, blank=True, related_name='sector_activities_topics',
        help_text= _("Primary sectors impacted by the organization's operations.")
    )
    TARGET_BENEFICIARY_CHOICES = (
        ('1', _('Women')),
        ('2', _('Diabilities')),
        ('3', _('Children')),
        ('4', _('Ethnic Minority')),
        ('5', _('Elderly')),
        ('6', _('NEET')),
        ('7', _('Migrant Workers')),
        ('8', _('Youth')),
        ('9', _('LGBT')),
        ('Other', _('Others'))
    )
    target_beneficiary = MultiSelectField(verbose_name=_('Target Beneficiary'), null=True, blank=True, max_length=255, choices=TARGET_BENEFICIARY_CHOICES)

    # Duplicates
    # company_description = description

    mission_statement = RichTextField(verbose_name=_('Mission Statement'), null=True, blank=True,
        help_text=_('Mission statement of the organization.'),
        config_name='minimal'
    )

    @property
    def phone_number_of_organizations_headquarters(self):
        return formset_getter(self, inspect.stack()[0][3])

    @phone_number_of_organizations_headquarters.setter
    def phone_number_of_organizations_headquarters(self, value):
        formset_setter(self, inspect.stack()[0][3], value)

    @property
    def location_of_organizations_operating_facilities(self):
        return formset_getter(self, inspect.stack()[0][3])

    @location_of_organizations_operating_facilities.setter
    def location_of_organizations_operating_facilities(self, value):
        formset_setter(self, inspect.stack()[0][3], value)



# Section 2
class AbstractOrganizationSection2(models.Model):

    class Meta:
        abstract = True

    productservice_type = models.ManyToManyField('taxonomy.Topic', verbose_name=_('Product/Service Type'), null=True, blank=True, related_name='productservice_type_topics',
        help_text=_('Type of product or service provided by the organization')
    )
    productservice_description = RichTextField(verbose_name=_('Product/Service Description'), null=True, blank=True,
        help_text=_('Description of the product or service.'),
        config_name='default'
    )

    # ==============================================================
    definition_of_unit_of_measure_1 = models.CharField(verbose_name=_('Definition of unit of measure 1'), null=True, blank=True, max_length=512)
    unit_of_impact_measurement_1 = models.CharField(verbose_name=_('Unit of Impact Measurement 1'), null=True, blank=True, max_length=512)

    definition_of_unit_of_measure_2 = models.CharField(verbose_name=_('Definition of unit of measure 2'), null=True, blank=True, max_length=512)
    unit_of_impact_measurement_2 = models.CharField(verbose_name=_('Unit of Impact Measurement 2'), null=True, blank=True, max_length=512)

    definition_of_unit_of_measure_3 = models.CharField(verbose_name=_('Definition of unit of measure 3'), null=True, blank=True, max_length=512)
    unit_of_impact_measurement_3 = models.CharField(verbose_name=_('Unit of Impact Measurement 3'), null=True, blank=True, max_length=512)

    store_measurement_year_values = models.TextField(verbose_name=_("Measurement Year and Values"), null=True, blank=True) # formset

    # ==============================================================

    CLIENT_TYPE_CHOICES = (
        ('1', _('Individuals/Households')),
        ('2', _('Microenterprises')),
        ('3', _('Small-to-Medium Enterprises')),
        ('4', _('Large Enterprises')),
        ('5', _('Non-profit / Non-Governmental Organization / Foundations')),
        ('6', _('Government')),
        ('7', _('International Organizations')),
        ('Other', _('Others'))
    )
    client_type = MultiSelectField(verbose_name=_('Client Type'), null=True, blank=True, max_length=255, choices=CLIENT_TYPE_CHOICES,
        help_text=_("Types of entities that are buyers or recipients of the organization's products and/or services")
    )
    client_information = RichTextField(verbose_name=_('Client Information'), null=True, blank=True,
        help_text=_('Name of major clients, if they are business or government'),
        config_name='minimal'
    )

    client_locations = models.ManyToManyField('taxonomy.Country', verbose_name=_('Client Locations'), null=True, blank=True, related_name='client_locations',)
    # Duplicates
    # client_locations = country

    @property
    def measurement_year_values(self):
        result = formset_getter(self, inspect.stack()[0][3])
        result = sorted(result, key=lambda k: k['year_of_datapoint'])
        return result

    @measurement_year_values.setter
    def measurement_year_values(self, value):
        formset_setter(self, inspect.stack()[0][3], value)

# Section 3
class AbstractOrganizationSection3(models.Model):

    class Meta:
        abstract = True

    store_top_3_major_investors_year_and_amount = models.TextField(verbose_name=_('Top 3 major investors, year and amount'), null=True, blank=True)
    store_top_3_major_donors_year_and_amount = models.TextField(verbose_name=_('Top 3 major donors, year and amount'), null=True, blank=True)

    ANNUAL_REVENUE_CHOICES = (
        ('1', _('Under $50K')),
        ('2', _('$50K-$100K')),
        ('3', _('$100K-$250K')),
        ('4', _('$250K-$500K')),
        ('5', _('$500K-$1MM')),
        ('6', _('$1MM-$2MM')),
        ('7', _('$1MM-$5MM')),
        ('8', _('Over $5MM'))
    )
    annual_revenue = models.CharField(verbose_name=_('Annual revenue'), null=True, blank=True, max_length=255, choices=ANNUAL_REVENUE_CHOICES)
    REVENUE_MODEL_CHOICES = (
        ('1', _('Social Business (Business revenue more than 75% of total revenue)')),
        ('2', _('Hybird (Business revenue range 25% to 75% of total revenue)')),
        ('3', _('Charity (Business revenue less than 25%)'))
    )
    revenue_model = models.CharField(verbose_name=_('Revenue Model'), null=True, blank=True, max_length=255, choices=REVENUE_MODEL_CHOICES)
    earned_revenue = BetterDecimalField(
        verbose_name=_('Earned Revenue'),
        suffix=settings.CURRENCY, # This is example for suffix field
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Revenue resulting from all business activities during the reporting period. Earned revenue is total revenues less "Contributed Revenue" (Grants and Donations).')
    )
    cost_of_goods_sold = BetterDecimalField(
        verbose_name=_('Cost of Goods Sold'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Direct costs attributable to the production of the goods sold by the organization during the reporting period.  The cost should include all costs of purchase, costs of conversion, and other direct costs incurred in producing and selling the organization's")
    )
    gross_profit = BetterDecimalField(
        verbose_name=_('Gross Profit'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The organization's residual profit after selling a product or service and deducting the costs directly associated with its production. Gross Profit is 'Earned Revenue' less 'Cost of Goods Sold'.")
    )
    personnel_expense = BetterDecimalField(
        verbose_name=_('Personnel Expense'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Expenses related to personnel, including wages, benefits, trainings, and payroll taxes incurred by the organization during the reporting period.')
    )
    selling_general_and_administration_expense = BetterDecimalField(
        verbose_name=_('Selling, General, and Administration Expense'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Sum of all direct and indirect selling expenses and all general and administrative expenses incurred by the organization during the reporting period.')
    )
    operating_expense = BetterDecimalField(
        verbose_name=_('Operating Expense'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Expenditures incurred by the organization as a result of performing its normal business operations. NOTE: For financial services companies this does not include Financial Expenses or provisions for loan losses (impairment losses).')
    )
    ebitda = BetterDecimalField(
        verbose_name=_('EBITDA'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Organization's earnings, excluding contributed revenues, before interest, taxes, depreciation and amortization during the reporting period.")
    )
    interest_expense = BetterDecimalField(
        verbose_name=_('Interest Expense'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Interest incurred during the reporting period on all liabilities, including any client deposit accounts held by the organization, borrowings, subordinated debt, and other liabilities.")
    )
    depreciation_and_amortization_expense = BetterDecimalField(
        verbose_name=_('Depreciation and Amortization Expense'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Value of expenses recorded by the organization during the reporting period for depreciation and amortization.')
    )
    taxes = BetterDecimalField(
        verbose_name=_('Taxes'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Value of corporate income taxes expensed by the organization during the reporting period.')
    )
    net_income_before_donations = BetterDecimalField(
        verbose_name=_('Net Income Before Donations'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Net Income or change in unrestricted net assets resulting from all business activities during the reporting period, excluding donations. The organization's net profit before donations.")
    )
    contributed_revenue = BetterDecimalField(
        verbose_name=_('Contributed Revenue'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Contributed revenue during the reporting period. Includes both unrestricted and restricted operating grants and donations and in-kind contributions. Does NOT include equity grants for capital, grants that are intended for future operating periods, or gra")
    )
    net_income = BetterDecimalField(
        verbose_name=_('Net Income'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Net Income or change in unrestricted net assets resulting from all business activities during the reporting period and all Contributed Revenue. The organization's net profit.")
    )
    # ===================================== New field section 3 after demo
    current_assets = BetterDecimalField(
        verbose_name=_('Current Assets'),
        max_digits=19,
        suffix=settings.CURRENCY,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of all assets that are reasonably expected to be converted into cash within one year in the normal course of business. Current assets can include cash, accounts receivable, inventory, marketable securities, prepa.")
    )
    total_value_of_loans_and_investments = BetterDecimalField(
        verbose_name=_('Total Value of Loans and Investments'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of financial portfolio products including loans and investments in investees.")
    )
    financial_assets = BetterDecimalField(
        verbose_name=_('Financial Assets'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of all assets that represent debt, equity, and cash assets such as: stocks, bonds, mutual funds, cash, and cash management accounts.  Values of assets should be based upon fair market value where efficient second.")
    )
    fixed_assets = BetterDecimalField(
        verbose_name=_('Fixed Assets'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of all long-term tangible assets  that are not expected to be converted into cash in the current or upcoming fiscal year, e.g., buildings, real estate, production equipment, and furniture. Sometimes called PLANT.")
    )
    total_assets = BetterDecimalField(
        verbose_name=_('Total Assets'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of all assets.")
    )
    retained_earnings = BetterDecimalField(
        verbose_name=_('Retained Earnings'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The sum of the organization's profits, cumulative from inception to the end of the reporting period, not paid out as dividends, but retained by the company to be reinvested in its core business or to pay debt. Also referred to as retained capital, accumul.")
    )
    accounts_payable = BetterDecimalField(
        verbose_name=_('Accounts Payable'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of all outstanding debts that must be paid within a given period of time in order to avoid default.")
    )
    accounts_receivable = BetterDecimalField(
        verbose_name=_('Accounts Receivable'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of outstanding debts from clients who received goods or services on credit.")
    )
    current_liabilities = BetterDecimalField(
        verbose_name=_('Current Liabilities'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of all liabilities that are expected to be settled with one year in the normal course of business. Current liabilities can include accounts payable, lines of credit, or other short term debts.")
    )
    financial_liabilities = BetterDecimalField(
        verbose_name=_('Financial Liabilities'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value, at the end of the reporting period, of an organization's financial liabilities. Financial liabilities include all borrowed funds, deposits held, or other contractual obligations to deliver cash.")
    )
    loans_payable = BetterDecimalField(
        verbose_name=_('Loans Payable'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The remaining balance, at the end of the reporting period, on all the organization's outstanding debt obligations carried on the balance sheet.")
    )
    total_liabilities = BetterDecimalField(
        verbose_name=_('Total Liabilities'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of organization's liabilities at the end of the reporting period.")
    )
    equity_or_net_assets = BetterDecimalField(
        verbose_name=_('Equity or Net Assets'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The residual interest, at the end of the reporting period, in the assets of the organization after deducting all its liabilities.")
    )
    cash_and_cash_equivalents_period_start = BetterDecimalField(
        verbose_name=_('Cash and Cash Equivalents- Period Start'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of the organization's cash equivalents at the beginning of the reporting period.")
    )
    cash_flow_from_operating_activities = BetterDecimalField(
        verbose_name=_('Cash Flow from Operating Activities'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of cash flows during the reporting period related to operating activities. Operating activities are the principal revenue-producing activities of the entity and other activities that are not investing or financing activities.")
    )
    cash_flow_from_investing_activities = BetterDecimalField(
        verbose_name=_('Cash Flow from Investing Activities'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of cash flows during the reporting period related to investing activities by the organization. Investing activities are the acquisition and disposal of long-term assets and other investments that are not considered to be cash equivalents.")
    )
    cash_flow_from_financing_activities = BetterDecimalField(
        verbose_name=_('Cash Flow from Financing Activities'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of cash flows during the reporting period related to financing activities by the organization. Financing activities are activities that result in changes in the size and composition of the contributed equity and borrowings of the organization.")
    )
    new_investment_capital = BetterDecimalField(
        verbose_name=_('New Investment Capital'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of cash flows from the organization's financing activities (both loans and investments) during the reporting period.")
    )
    net_cash_flow = BetterDecimalField(
        verbose_name=_('Net Cash Flow'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The net cash flow of the organization during the reporting period. Net cash flow equals inflows less outflows of cash and cash equivalents.")
    )
    cash_and_cash_equivalents_period_end = BetterDecimalField(
        verbose_name=_('Cash and Cash Equivalents- Period End'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of the organizations cash equivalents at the end of the reporting period.")
    )
    revenue_growth = BetterDecimalField(
        verbose_name=_('Revenue Growth'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Growth in value of the organization's revenue from one reporting period to another.Calculation: (Earned Revenue in reporting period 2 - Earned Revenue in reporting period 1) / Earned Revenue in reporting period 1")
    )
    income_growth = BetterDecimalField(
        verbose_name=_('Income Growth'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Growth in value of the organization's Net income Before Donations from one reporting period to another.Calculation: (Net Income Before Donations in reporting period 2 - Net Income Before Donations in reporting period 1) / Net Income Before Donations")
    )
    gross_margin = BetterDecimalField(
        verbose_name=_('Gross Margin'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Percent of earned revenues that the organization retains after incurring the direct costs associated with producing the goods and services sold by the company.Calculation: 'Cost of Goods Sold' / 'Earned Revenue'")
    )
    operating_profit_margin = BetterDecimalField(
        verbose_name=_('Operating Profit Margin'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Organization's effectiveness at managing costs and turning earned revenues into income.Calculation: (Net Income Before Donations + Taxes) / Earned Revenue")
    )
    working_capital = BetterDecimalField(
        verbose_name=_('Working Capital'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Organization's operating liquidity.Calculation: Current Assets - Current Liabilities")
    )
    return_on_assets_roa = BetterDecimalField(
        verbose_name=_('Return on Assets (ROA)'),
        suffix='%',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Measurement of how well the organization uses assets to generate returns.Calculation: Net Income Before Donations / Average Total Assets Average Total Assets: (Total Assets at the beginning of the period + Total Assets at the end of the period) / 2")
    )
    return_on_equity_roe = BetterDecimalField(
        verbose_name=_('Return on Equity (ROE)'),
        suffix='%',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Measurement of commercial profitability.Calculation: Net Income Before Donations / Average Equity or Net Assets Average Equity or Net Assets: (Average Equity or Net Assets at the beginning of the period + Average Equity or Net Assets at the end of")
    )
    fixed_costs = BetterDecimalField(
        verbose_name=_('Fixed Costs'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Costs that do not vary based on production or sales levels.")
    )
    entrepreneur_investment = BetterDecimalField(
        verbose_name=_('Entrepreneur Investment'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of the equity and/or other financial contribution in the organization provided by the entrepreneur/s at the time of investment.")
    )
    community_service_donations = BetterDecimalField(
        verbose_name=_('Community Service Donations'),
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Value of all charitable donations made by the organization")
    )
    board_of_directors = BetterPositiveIntegerField(
        verbose_name=_('Board of Directors'),
        suffix='Person',
        null=True,
        blank=True,
        help_text=_("Number of members of organization's Board of Directors or other governing body, as of the end of the reporting period.")
    )
    female_ownership = BetterDecimalField(
        verbose_name=_('Female Ownership'),
        suffix='%',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Percentage of the company that is female-owned as of the end of the reporting period.Calculation: number of total shares owned by females/number of total shares.Note: Where regional or local laws apply for calculating ownership by previously excluded")
    )
    financial_statement_review = models.NullBooleanField(
        verbose_name=_('Financial Statement Review'),
        null=True,
        blank=True,
        help_text=_("Indicate whether it is the organization's policy to produce financial statements that are verified annually by a certified accountant.")
    )
    # ================   End new field section 3 after demo
    @property
    def top_3_major_investors_year_and_amount(self):
        return formset_getter(self, inspect.stack()[0][3])

    @top_3_major_investors_year_and_amount.setter
    def top_3_major_investors_year_and_amount(self, value):
        formset_setter(self, inspect.stack()[0][3], value)

    @property
    def top_3_major_donors_year_and_amount(self):
        return formset_getter(self, inspect.stack()[0][3])

    @top_3_major_donors_year_and_amount.setter
    def top_3_major_donors_year_and_amount(self, value):
        formset_setter(self, inspect.stack()[0][3], value)


# Section 4
class AbstractOrganizationSection4(models.Model):
    # =========   New field sectino 4 after demo
    full_time_employees = models.PositiveIntegerField(
        verbose_name=_('Full-time Employees'),
        null=True,
        blank=True,
        help_text=_("Number of full-time employees at the end of the reporting period.")
    )
    full_time_employees_female = models.PositiveIntegerField(
        verbose_name=_('Full-time Employees: Female'),
        null=True,
        blank=True,
        help_text=_("Number of full-time female employees at the end of the reporting period.")
    )
    part_time_employees = models.PositiveIntegerField(
        verbose_name=_('Part-time Employees'),
        null=True,
        blank=True,
        help_text=_("Number of part-time employees at the end of the reporting period.")
    )
    part_time_employees_female = models.PositiveIntegerField(
        verbose_name=_('Part-time Employees: Female'),
        null=True,
        blank=True,
        help_text=_("Number of female part-time employees at the end of the reporting period.")
    )
    volunteer_hours_worked = BetterDecimalField(
        verbose_name=_('Volunteer Hours Worked'),
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Total number of hours worked by volunteers that supported the organization during the reporting period.")
    )
    client_individuals = BetterDecimalField(
        verbose_name=_('Client Individuals'),
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Number of individuals or households who were clients during the reporting period.For microfinance clients, this refers to active clients.For healthcare providers, this refers to patients.Note: Organizations tracking households should report num")
    )
    client_organizations = models.PositiveIntegerField(
        verbose_name=_('Client Organizations'),
        null=True,
        blank=True,
        help_text=_("Number of businesses or other organizations that were clients during the reporting period.")
    )
    # =============  End new field
    store_team_information = models.TextField(
        verbose_name=_('Key Officers (Name and title)'),
        null=True,
        blank=True
    )  # formset

    class Meta:
        abstract = True

    @property
    def team_information(self):
        return formset_getter(self, inspect.stack()[0][3])

    @team_information.setter
    def team_information(self, value):
        formset_setter(self, inspect.stack()[0][3], value)


# Section 5
class AbstractOrganizationSection5(models.Model):

    class Meta:
        abstract = True

    POSSIBLE_FORM_OF_FINANCIAL_SUPPORT_CHOICES = (
        ('1', _('Grant')),
        ('2', _('Loan')),
        ('3', _('Equity'))
    )
    possible_form_of_financial_support = MultiSelectField(verbose_name=_('Possible form of financial support'), null=True, blank=True, max_length=255, choices=POSSIBLE_FORM_OF_FINANCIAL_SUPPORT_CHOICES,
        help_text=_("Grant, Loan or investment")
    )
    potential_size_of_investment = BetterDecimalField(verbose_name=_('Potential size of investment'), max_digits=19, decimal_places=2, null=True, blank=True,
        help_text=_("Potential size of investment in %s") % settings.CURRENCY
    )
    POTENTIAL_USE_OF_INVESTMENT_CHOICES = (
        ('1', _('Land/building')),
        ('2', _('Equipment')),
        ('3', _('Human resources development')),
        ('4', _('Revolving Capital')),
        ('Other', _('Other'))
    )
    potential_use_of_investment = MultiSelectField(verbose_name=_('Potential use of investment'), null=True, blank=True, max_length=255, choices=POTENTIAL_USE_OF_INVESTMENT_CHOICES)
    POSSIBLE_FORM_OF_NON_FINANCIAL_SUPPORT_CHOICES = (
        ('1', _('Strategy Planning')),
        ('2', _('Financial Management')),
        ('4', _('PR')),
        ('5', _('HR')),
        ('6', _('Legal')),
        ('7', _('Market Access')),
        ('8', _('External Relations')),
        ('9', _('Techinical Expertise')),
        ('10', _('Fundraising')),
        ('3', _('Operational Management')),
        ('Other', _('Others'))
    )
    possible_form_of_non_financial_support = MultiSelectField(verbose_name=_('Possible form of non-financial support'), null=True, blank=True, max_length=255, choices=POSSIBLE_FORM_OF_NON_FINANCIAL_SUPPORT_CHOICES,
        help_text=_("Strategy, PR, Marketing, Legal, Operation Management, Financial Management")
    )


class AbstractOrganizationStartup(models.Model):
    class Meta:
        abstract = True

    is_register_to_nia = models.NullBooleanField(null=True, blank=True, default=False)

    company_vision = RichTextField(null=True, blank=True)
    company_mission = RichTextField(null=True, blank=True)
    business_model = RichTextField(null=True, blank=True)
    growth_strategy = RichTextField(null=True, blank=True)

    has_participate_in_program = models.NullBooleanField(null=True, blank=True)
    participate_program = models.ManyToManyField('organization.Program', related_name='organization_programs', null=True, blank=True)

    has_received_investment = models.NullBooleanField(null=True, blank=True)

    financial_source = models.ManyToManyField('taxonomy.TypeOfFinancialSource', null=True, blank=True,
                                               related_name='organization_financial_source')
    other_financial_source = models.TextField(null=True, blank=True)

    has_taken_equity_in_startup = models.NullBooleanField(null=True, blank=True)
    taken_equity_amount = models.CharField(max_length=255, null=True, blank=True)


class AbstractOrganizationInvestor(models.Model):
    class Meta:
        abstract = True

    specialty = RichTextField(null=True, blank=True)

    is_lead_investor = models.NullBooleanField(null=True, blank=True)

    has_taken_equity_in_fund_organization = models.NullBooleanField(null=True, blank=True)

    funding_type = models.ManyToManyField('taxonomy.TypeOfFunding', null=True, blank=True,
                                          related_name='organization_funding')

    # money_raise = models.PositiveIntegerField(null=True, blank=True)
    # target_funding = models.PositiveIntegerField(null=True, blank=True)
    # pre_money_valuation = models.PositiveIntegerField(null=True, blank=True)
    # amount_of_money_invested = models.PositiveIntegerField(null=True, blank=True)

    money_money_raise = MoneyField(null=True, blank=True, max_digits=19, decimal_places=2, default_currency='THB')
    money_target_funding = MoneyField(null=True, blank=True, max_digits=19, decimal_places=2, default_currency='THB')
    money_pre_money_valuation = MoneyField(null=True, blank=True, max_digits=19, decimal_places=2, default_currency='THB')
    money_amount_of_money_invested = MoneyField(null=True, blank=True, max_digits=19, decimal_places=2, default_currency='THB')


class AbstractOrganizationAttachment(models.Model):
    class Meta:
        abstract = True

    # Global
    attachments_incorporation_registration_certificate = files_widget.XFilesField(null=True, blank=True, verbose_name='Incorporation/Registration Certificate')

    # Startup
    attachments_biography_consisting_of_major_achievements_of_management_levels = files_widget.XFilesField(null=True, blank=True, verbose_name='Minimum 5 biography consisting of major achievements (if any) of management levels')
    attachments_list_of_organizational_or_program_partners = files_widget.XFilesField(null=True, blank=True, verbose_name='List of organizational or program partners (if any)')

    # Investor
    attachments_financial_statement = files_widget.XFilesField(null=True, blank=True, verbose_name='Financial Statement')
    attachments_investment_portfolio = files_widget.XFilesField(null=True, blank=True, verbose_name='Investment Portfolio')

    # Program
    attachments_summary_of_the_activities_of_the_program = files_widget.XFilesField(null=True, blank=True, verbose_name='Summary of the activities of the program')
    attachments_long_term_sustainable_revenue_model = files_widget.XFilesField(null=True, blank=True, verbose_name='Long-term sustainable revenue model')
    attachments_resumes_or_portfolio_of_mentors_coaches_speaker_and_trainers = files_widget.XFilesField(null=True, blank=True, verbose_name='Minimum 5 resumes or portfolio(consisting of previous achievement) of mentors, coaches, speaker, and trainers')
    attachments_program_plans_in_the_future = files_widget.XFilesField(null=True, blank=True, verbose_name='Program plans in the future')
    attachments_list_of_notable_startup_team_alumni = files_widget.XFilesField(null=True, blank=True, verbose_name='List of notable startup/team alumni')
    attachments_list_of_organization_or_program_partners = files_widget.XFilesField(null=True, blank=True, verbose_name='List of organization or program partners')

    # Other
    attachments_other_attached_documents_text = models.CharField(null=True, blank=True, max_length=1024, verbose_name='Other attached documents, Please specify')
    attachments_other_attached_documents = files_widget.XFilesField(null=True, blank=True, verbose_name='')

class OrganizationAssistance(models.Model):
    organization = models.ForeignKey('organization.Organization', related_name='assistance_organization')
    assistance = models.ForeignKey('taxonomy.TypeOfAssistantship', related_name='organization_assistance')
    is_required = models.NullBooleanField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class OrganizationFundingRound(models.Model):
    organization = models.ForeignKey('organization.Organization', related_name='funding_round_organization')
    announced_date = models.DateField(null=True, blank=True)
    closed_date = models.DateField(null=True, blank=True)


class Organization(Party, AbstractPermalink, AbstractOrganizationSection1, AbstractOrganizationSection2, \
                   AbstractOrganizationSection3, AbstractOrganizationSection4, AbstractOrganizationSection5, \
                   AbstractOrganizationStartup, AbstractOrganizationInvestor, AbstractOrganizationAttachment):

    inst_type = 'organization'

    KIND_ORGANIZATION = 'organization'
    KIND_PRODUCT = 'product'

    KIND_CHOICES = (
        (KIND_PRODUCT, _('Product/Service')),
        (KIND_ORGANIZATION, pgettext_lazy('model_choice', 'Organization'))
    )

    TYPE_SOCIAL_ENTERPRISE = TYPE_SOCIAL_ENTERPRISE
    TYPE_STARTUP = TYPE_STARTUP
    TYPE_SUPPORTING_ORGANIZATION = TYPE_SUPPORTING_ORGANIZATION
    TYPE_INVESTOR = TYPE_INVESTOR
    TYPE_PROGRAM = TYPE_PROGRAM

    DEFAULT_TYPE_RECEIVER = settings.DEFAULT_TYPE_RECEIVER

    TYPE_CHOICES = TYPE_CHOICES
    EXPAND_TYPE_CHOICES = EXPAND_TYPE_CHOICES

    CLAIM_RELATED_VERBS = ['PartyPartnerParty', 'PartyReceivedFundingParty', 'PartyReceivedInvestingParty']

    # kind
    kind = models.CharField(max_length=100, choices=KIND_CHOICES, default=KIND_ORGANIZATION)

    # Relation
    created_by = models.ForeignKey(USER_MODEL, related_name='created_by')
    published_by = models.ForeignKey(USER_MODEL, related_name='published_by', null=True, blank=True)
    published_claim = models.ForeignKey('self', related_name='published_claim_organization', null=True, blank=True)

    admins = models.ManyToManyField(USER_MODEL, related_name='admins')
    jobs = models.ManyToManyField('organization.Job', related_name='organization_jobs', null=True, blank=True)
    in_the_news = models.ManyToManyField('organization.InTheNews', related_name='organization_in_the_news', null=True, blank=True)



    # Internal
    cover_image = files_widget.ImageField(null=True, blank=True)

    image = files_widget.ImageField(null=True, blank=True)
    images = files_widget.ImagesField(null=True, blank=True)

    name = models.CharField(max_length=255)

    summary = models.TextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)

    # Taxonomy
    type_of_needs = models.ManyToManyField('taxonomy.TypeOfNeed', null=True, blank=True, related_name='type_of_needs')
    type_of_supports = models.ManyToManyField('taxonomy.TypeOfSupport', null=True, blank=True,
                                              related_name='type_of_supports')
    topics = models.ManyToManyField('taxonomy.Topic', null=True, blank=True, related_name='topics')
    organization_roles = models.ManyToManyField('taxonomy.OrganizationRole', null=True, blank=True, related_name='organization_roles')
    organization_primary_role = models.ForeignKey('taxonomy.OrganizationRole', null=True, blank=True, related_name='primary_organization_role')

    # deprecated
    organization_type = models.ForeignKey('taxonomy.OrganizationType', null=True, blank=True, related_name='organization_type')
    investor_type = models.ForeignKey('taxonomy.InvestorType', null=True, blank=True, related_name='investor_type')

    organization_types = models.ManyToManyField('taxonomy.OrganizationType', null=True, blank=True, related_name='organization_types')
    investor_types = models.ManyToManyField('taxonomy.InvestorType', null=True, blank=True, related_name='investor_types')

    product_launch = models.ForeignKey('taxonomy.OrganizationProductLaunch', null=True, blank=True, related_name='organization_product_launch')
    funding = models.ForeignKey('taxonomy.OrganizationFunding', null=True, blank=True, related_name='organization_funding')
    request_funding = models.ForeignKey('taxonomy.OrganizationFunding', null=True, blank=True, related_name='organization_request_funding')

    office_type = models.ManyToManyField('taxonomy.TypeOfOffice', null=True, blank=True,
                                          related_name='organization_office_type')
    other_office_type = models.TextField(null=True, blank=True)


    focus_sector = models.ManyToManyField('taxonomy.TypeOfFocusSector', null=True, blank=True,
                                          related_name='organization_focus_sector')
    other_focus_sector = models.TextField(null=True, blank=True)

    focus_industry = models.ManyToManyField('taxonomy.TypeOfFocusIndustry', null=True, blank=True,
                                            related_name='organization_focus_industry')
    other_focus_industry = models.TextField(null=True, blank=True)

    stage_of_participants = models.ManyToManyField('taxonomy.TypeOfStageOfParticipant', null=True, blank=True,
                                                   related_name='organization_stage_of_participants')

    growth_stage = models.ManyToManyField('taxonomy.OrganizationGrowthStage', null=True, blank=True, related_name='organization_growth_stage')

    # deal_size_start = models.PositiveIntegerField(null=True, blank=True)
    # deal_size_end = models.PositiveIntegerField(null=True, blank=True)

    money_deal_size_start = MoneyField(null=True, blank=True, max_digits=19, decimal_places=2, default_currency='THB')
    money_deal_size_end = MoneyField(null=True, blank=True, max_digits=19, decimal_places=2, default_currency='THB')

    priority = models.PositiveIntegerField(default=0)
    ordering = models.PositiveIntegerField(null=True, blank=True)

    # External
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    homepage_url = models.URLField(max_length=255, null=True, blank=True)

    # 2018
    preferred_name = models.CharField(max_length=255, null=True, blank=True)
    company_registration_number = models.CharField(max_length=255, null=True, blank=True)

    instagram_url = models.URLField(max_length=255, null=True, blank=True)
    other_channel = models.TextField(null=True, blank=True)

    attachments_types = models.ManyToManyField('taxonomy.TypeOfAttachment', null=True, blank=True,
                                               related_name='orgazation_attachments_types')
    other_attachments_types = models.CharField(max_length=1024, null=True, blank=True)

    attachments = files_widget.XFilesField(null=True, blank=True)

    date_of_establishment = models.DateField(null=True, blank=True)

    extra_information = models.TextField(null=True, blank=True)

    # Meta
    type_of_organization = models.CharField(max_length=128, choices=TYPE_CHOICES, default=DEFAULT_TYPE_RECEIVER)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)

    created_raw = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    changed_raw = models.DateTimeField(null=True, blank=True)
    changed = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)

    point = models.IntegerField(default=0)

    claim_checked = models.BooleanField(default=False)
    is_mockup = models.BooleanField(default=False)
    code = models.CharField(max_length=512, null=True, blank=True, unique=True)

    edit_link = 'Edit'
    pdf = 'Download'


    cached_vars = ['status', 'published']

    class Meta:
        ordering = ['-store_popular']

    def get_class_display(self):
        class_display = self.type_of_organization.title()

        if not class_display:
            class_display = super(Organization, self).get_class_display()

        return class_display

    def get_inst_type_human_readable(self):
        return _(camelcase_to_underscore(self.type_of_organization).replace('_', ' '))

    def get_thumbnail(self):
        return instance_get_thumbnail(self, crop=None)

    def get_thumbnail_in_primary(self):
        return instance_get_thumbnail(self, size='150x150', crop=None, upscale=False)

    def get_thumbnail_images(self):
        return instance_get_thumbnail(self, field_name='images', size='500x500', crop=None, upscale=False, no_default=True)

    def get_thumbnail_cover_image(self):
        return instance_get_thumbnail(self, field_name='cover_image', size='1170x10000', crop=None, upscale=False, no_default=True)

    def get_type_of_organization(self):
        return TYPE_SUPPORTING_ORGANIZATION if self.type_of_organization == TYPE_PROGRAM else self.type_of_organization


    def get_absolute_url(self):
        if not self.permalink:
            return ''

        return reverse('organization_detail', args=[self.permalink])

    def get_display_name(self):
        return self.name

    def get_short_name(self):
        return self.get_display_name()

    def get_summary(self):
        summary = truncatechars(self.summary or '', SUMMARY_MAX_LENGTH)

        if not summary:
            summary = []
            if self.preferred_name:
                summary += [self.preferred_name]

            try:
                summary += [item.title for item in self.focus_sector.all()[0:2] if item.title != 'Other']
            except ValueError:
                pass

            if self.other_focus_sector:
                summary += [self.other_focus_sector]
            summary = u' — '.join(summary)

        return summary

    @property
    def is_publish(self):
        return self.status == STATUS_PUBLISHED

    @property
    def last_visit_date(self):
        organization_type = ContentType.objects.get_for_model(self)
        try:
            last_visit = StatisitcAccess.objects.filter(content_type__pk=organization_type.id, object_id=self.id).latest('created').created
        except StatisitcAccess.DoesNotExist:
            last_visit = self.created

        return last_visit

    @property
    def social_networks(self):
        url_text = ""
        for sns_url in [self.facebook_url, self.twitter_url, self.linkedin_url]:
            if sns_url:
                if url_text:
                    url_text += ', ' + sns_url
                else:
                    url_text = sns_url
        return url_text

    @property
    def uptodate_status(self):

        # Logic make from "test_uptodate_status (domain.tests.test_model.TestStatement)"

        if self.status == STATUS_DRAFT:
            return {'code': 'draft', 'text': _('Draft')}

        elif self.status == STATUS_PENDING:
            return {'code': 'pending', 'text': _('Pending')}

        outdate = timezone.now() - timedelta(days=settings.UPTODATE_DAYS)

        # Don't refactor this if case it's short hand for check None
        if (self.created and self.created >= outdate) or (self.changed and self.changed >= outdate):

            if self.created and not self.changed:
                return {'code': 'new', 'text': _('New')}

            elif self.created and self.changed:
                return {'code': 'updated', 'text': _('Updated')}

        return False

    def build_claim(self):
        if self.claim_checked or int(self.status) not in [STATUS_PENDING, STATUS_PUBLISHED]:
        # if int(self.status) not in [STATUS_PENDING, STATUS_PUBLISHED]:
            return

        from notification.models import notification_create

        self.claim_checked = True
        Organization.objects.filter(id=self.id).update(claim_checked=True)

        names = self.name.lower().replace('co.,', '').replace('co.', '').replace(' ltd', '').replace(',ltd', '').replace('ltd.', '').replace('ministry', '').replace('department', '').replace('office', '').replace('government', '').split()
        names = [name for name in names if name not in ['.', ',', ' ']]

        keyword = '(%s)' % ' OR '.join(names)

        look_alike_list_dst = SearchQuerySet().filter(content_type='Relation', verb__in=self.CLAIM_RELATED_VERBS, dst_status=STATUS_DRAFT, dst_is_mockup=True).filter(dst=Raw(keyword))
        look_alike_list_src = SearchQuerySet().filter(content_type='Relation', verb__in=self.CLAIM_RELATED_VERBS, src_status=STATUS_DRAFT, src_is_mockup=True, swap=True).filter(src=Raw(keyword))
        look_alike_list = list(look_alike_list_dst) + list(look_alike_list_src)

        print 'keyword', keyword

        for item in look_alike_list:
            print item, item.score

            if item.score < 3.0:
                continue

            obj = item.object
            print obj, obj.src, obj.dst

            if obj:
                notification_create(obj, claim_receiver=self)

    def generate_code(self, with_save=False):
        if not self.code and self.status == STATUS_PUBLISHED:
            self.code = '%s-%s' % (self.type_of_organization, '%05d' % 1)
            try:
                instance = Organization._default_manager.filter(type_of_organization=self.type_of_organization, code__isnull=False).latest('code')
                self.code = '%s-%s' % (self.type_of_organization, '%05d' % (int(instance.code.split('-')[-1]) + 1))
            except Organization.DoesNotExist:
                pass

        if with_save:
            try:
                self.save()
            except IntegrityError:
                self.generate_code(with_save=with_save)

        return self.code


    def save(self, not_changed=False, not_claim_approve=False, *args, **kwargs):

        # Logic make from "test_uptodate_status (domain.tests.test_model.TestStatement)"
        now = timezone.now()
        self.changed_raw = now

        if not self.id and not self.created_raw:
            self.created_raw = now


        try:
            before = type(self).objects.get(id=self.id)
        except:
            before = self

        if not before.created and self.status != STATUS_DRAFT:
            self.created = timezone.now()

        if before.id and self.status not in [STATUS_DRAFT, STATUS_PENDING] and before.status not in [STATUS_DRAFT, STATUS_PENDING] and before.changed == self.changed:

            if not not_changed:
                self.changed = timezone.now()

        if not self.id or before.priority != self.priority:
            self.build_total(field_names=['popular'], not_save=True)

        # from appen ordering field
        # TODO: move to  extended from common.PriorityModel

        self.generate_code()

        if not self.id:
            super(Organization, self).save(*args, **kwargs)
            instance = Organization.objects.get(id=self.id)

            instance.save(not_changed=True)

        else:

            self.ordering = int('%s%s' % (('0'*2 + '%s' % self.priority)[-2:], ('0'*8 + '%s' % self.id)[-8:]))
            super(Organization, self).save(*args, **kwargs)

        if self.type_of_organization != Organization.TYPE_STARTUP and before.status != STATUS_PUBLISHED and self.status == STATUS_PUBLISHED and not not_claim_approve:
            for program in self.program_organization.filter(status=STATUS_PENDING):
                program.status = STATUS_PUBLISHED
                program.published = self.published
                program.published_by = self.published_by
                program.save()

            stamp = {}
            for related_model in BaseRelation.__subclasses__():
                if related_model.CLAIM_APPROVE:
                    try:
                        related_list = related_model.objects.filter(status=STATUS_PUBLISHED, dst__id=self.id, src__organization__status=STATUS_PENDING)
                    except:
                        related_list = related_model.objects.filter(status=STATUS_PUBLISHED, dst__id=self.id, src__status=STATUS_PENDING)

                    for related in related_list:
                        src = related.src

                        if stamp.get(src.id):
                            continue

                        src = src.get_inst()
                        src.status = STATUS_PUBLISHED
                        src.published = self.published
                        src.published_by = self.published_by
                        src.published_claim = self
                        try:
                            src.save(not_claim_approve=True)
                        except TypeError:
                            src.save()

                        stamp[src.id] = True


                    try:
                        related_list = related_model.objects.filter(status=STATUS_PUBLISHED, src__id=self.id, dst__organization__status=STATUS_PENDING)
                    except:
                        related_list = related_model.objects.filter(status=STATUS_PUBLISHED, src__id=self.id, dst__status=STATUS_PENDING)

                    for related in related_list:
                        dst = related.dst

                        if stamp.get(dst.id):
                            continue

                        dst = dst.get_inst()
                        dst.status = STATUS_PUBLISHED
                        dst.published = self.published
                        dst.published_by = self.published_by
                        dst.published_claim = self
                        try:
                            dst.save(not_claim_approve=True)
                        except TypeError:
                            dst.save()

                        stamp[dst.id] = True


class Staff(models.Model):
    name = models.CharField(max_length=512)
    job_title = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(null=True, blank=True, max_length=100)

    attachments = files_widget.XFilesField(null=True, blank=True)
    user = models.ForeignKey(USER_MODEL, related_name='user_staff', null=True, blank=True)

    def __unicode__(self):
        return self.name


class OrganizationStaff(Staff, CommonModel, CachedModel, PriorityModel):
    STATUS_MENTOR = 101
    STATUS_KEY_PERSON = 100
    STATUS_STAFF = 1

    STAFF_STATUS_CHOICES = (
        (STATUS_MENTOR, _('Mentor')),
        (STATUS_KEY_PERSON, _('Key Person')),
        (STATUS_STAFF, _('Staff')),
    )

    staff_status = models.IntegerField(choices=STAFF_STATUS_CHOICES, default=STATUS_STAFF)
    organization = models.ForeignKey(Organization, null=True, blank=True, related_name='staff_organization')


class Job(CommonModel, CachedModel, PriorityModel):

    POSITION_DEFAULT = 'full-time'

    POSITION_CHOICES = (
        (POSITION_DEFAULT, _('Full-time Employee')),
        ('contract', _('Contractor')),
        ('internship', _('Intern')),
        ('cofounder', _('Co-founder'))
    )

    ROLE_CHOICES = (
        ('administration', _('Administration')),
        ('analyst-scientist', _('Analyst/Scientist')),
        ('designer', _('Designer')),
        ('finance-accounting', _('Finance/Accounting')),
        ('hardware-engineer', _('Hardware Engineer')),
        ('hr', _('HR')),
        ('legal', _('Legal')),
        ('management', _('Management')),
        ('marketing-and-pr', _('Marketing and PR')),
        ('operations', _('Operations')),
        ('others', _('Others')),
        ('product-manager', _('Product Manager')),
        ('sales', _('Sales')),
        ('software-engineer', _('Software Engineer')),
    )

    # Deprecate
    # organization = models.ForeignKey(Organization, related_name='job_organization', null=True, blank=True) # denormalize

    STATUS_CHOICES = (
        (STATUS_PUBLISHED, _('Active')),
        (STATUS_PENDING, _('Close')),
    )
    REMOTE_CHOICES = (
        (False, _('No')),
        (True, _('Yes')),
    )

    title = models.CharField(max_length=255)
    contact_information = RichTextField()
    description = RichTextField(null=True, blank=True)

    role = models.CharField(null=True, blank=True, max_length=128, choices=ROLE_CHOICES) #deprecated
    job_primary_role = models.ForeignKey(JobRole, null=True, blank=True, related_name='job_job_primary_role')
    job_roles = models.ManyToManyField(JobRole, null=True, blank=True, related_name='job_job_roles')

    position = models.CharField(null=True, blank=True, max_length=128, choices=POSITION_CHOICES)

    salary_min = models.PositiveIntegerField(null=True, blank=True) # USD
    salary_max = models.PositiveIntegerField(null=True, blank=True) # USD

    money_salary_min = MoneyField(null=True, blank=True, max_digits=19, decimal_places=2, default_currency='THB')
    money_salary_max = MoneyField(null=True, blank=True, max_digits=19, decimal_places=2, default_currency='THB')

    money_salary_min_thb = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2)
    money_salary_max_thb = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2)
    money_salary_min_usd = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2)
    money_salary_max_usd = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2)


    equity_min = BetterDecimalField(null=True, blank=True, max_digits=19, decimal_places=2) # %
    equity_max = BetterDecimalField(null=True, blank=True, max_digits=19, decimal_places=2) # %

    remote = models.NullBooleanField(null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)

    country = models.ForeignKey('taxonomy.Country', null=True, blank=True, related_name='job_country')
    location = models.CharField(max_length=255, null=True, blank=True) #deprecated
    locations = models.ManyToManyField(Location, null=True, blank=True)

    skills = TagAutocompleteTagItField(max_tags=False, null=True, blank=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PUBLISHED)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(USER_MODEL, related_name='job_created_by', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('job_detail', args=[self.id])

    def __unicode__(self):
        return self.title

    def get_display_name(self):
        return self.title


    def get_summary(self):

        summary = []

        if self.locations.exists():
            summary.extend(self.locations.all().values_list('title', flat=True))

        if self.position:
            summary.append(self.get_position_display())

        if self.remote:
            summary.append('Remote OK')

        if self.money_salary_min and self.money_salary_max:
            summary.append(('%s - %s' % (self.money_salary_min, self.money_salary_max)).replace(',000.00', 'k'))
        elif self.money_salary_min:
            summary.append(('%s' % (self.money_salary_min)).replace(',000.00', 'k'))
        elif self.money_salary_max:
            summary.append(('%s' % (self.money_salary_max)).replace(',000.00', 'k'))

        if self.equity_min and self.equity_max:
            summary.append('Equity:  %s%% - %s%%' % (self.equity_min, self.equity_max))
        elif self.equity_min:
            summary.append('Equity: %s%%' % (self.equity_min))
        elif self.equity_max:
            summary.append('Equity: %s%%' % (self.equity_max))


        return '\n'.join(summary)

    @property
    def image(self):
        try:
            org = self.organization_jobs.all().first()
            return org and org.image
        except Organization.DoesNotExist:
            return None

    def get_thumbnail(self):
        try:
            org = self.organization_jobs.all().first()
            return org and org.get_thumbnail()
        except Organization.DoesNotExist:
            return None

    def get_thumbnail_in_primary(self):
        try:
            org = self.organization_jobs.all().first()
            return org and org.get_thumbnail_in_primary()
        except Organization.DoesNotExist:
            return None

    @property
    def permalink(self):
        return self.id

    def save(self, *args, **kwargs):

        self.money_salary_min_thb = convert_money(self.money_salary_min, 'THB')
        self.money_salary_max_thb = convert_money(self.money_salary_max, 'THB')
        self.money_salary_min_usd = convert_money(self.money_salary_min, 'USD')
        self.money_salary_max_usd = convert_money(self.money_salary_max, 'USD')

        super(Job, self).save()


tagging.register(Job, tag_descriptor_attr='skill_set')


class Program(Organization):

    inst_type = 'program'

    CLAIM_RELATED_VERBS = ['OrganizationParticipate']


    program_type = models.ManyToManyField('taxonomy.ProgramType', null=True, blank=True, related_name='program_program_type')
    organization = models.ForeignKey(Organization, related_name='program_organization', null=True, blank=True)

    is_partner = models.NullBooleanField(null=True, blank=True)
    is_acting_as_an_investor = models.NullBooleanField(null=True, blank=True)
    has_invited_in_participants_team = models.NullBooleanField(null=True, blank=True)

    contact_information = models.TextField(null=True, blank=True)
    contact_person = models.TextField(null=True, blank=True)

    investment_type = models.ManyToManyField('taxonomy.TypeOfInvestment', null=True, blank=True, related_name='program_investment_type')
    investment_stage_type = models.ManyToManyField('taxonomy.TypeOfInvestmentStage', null=True, blank=True, related_name='program_investment_stage_type')
    has_specific_stage = models.NullBooleanField(null=True, blank=True)
    specific_stage = models.TextField(null=True, blank=True)

    has_taken_equity_in_participating_team = models.NullBooleanField(null=True, blank=True)
    does_provide_financial_supports = models.NullBooleanField(null=True, blank=True)

    amount_of_financial_supports = models.CharField(max_length=255, null=True, blank=True)

    period_of_engagement = models.PositiveIntegerField(null=True, blank=True)

    does_provide_working_spaces = models.NullBooleanField(null=True, blank=True)
    working_spaces_information = RichTextField(null=True, blank=True)

    is_own_working_space = models.NullBooleanField(null=True, blank=True)

    does_provide_service_and_facility = models.NullBooleanField(null=True, blank=True)
    service_and_facility_information = RichTextField(null=True, blank=True)

    def get_service_and_facility_information(self):
        try:
            return pickle.loads(self.service_and_facility_information)
        except EOFError:
            return None


class ProgramBatch(CommonModel, CachedModel):
    title = models.CharField(max_length=255)
    batch_type = models.ForeignKey('taxonomy.TypeOfBatch', null=True, blank=True, related_name='batch_type_program')

    has_pre_seed_stage = models.NullBooleanField(null=True, blank=True)
    has_seed_stage = models.NullBooleanField(null=True, blank=True)
    has_pre_series_a_stage = models.NullBooleanField(null=True, blank=True)

    has_series_a_stage = models.NullBooleanField(null=True, blank=True)
    has_series_b_stage = models.NullBooleanField(null=True, blank=True)
    has_series_c_stage = models.NullBooleanField(null=True, blank=True)

    amount_pre_seed_stage = models.CharField(max_length=512, null=True, blank=True)
    amount_seed_stage = models.CharField(max_length=512, null=True, blank=True)
    amount_pre_series_a_stage = models.CharField(max_length=512, null=True, blank=True)

    amount_series_a_stage = models.CharField(max_length=512, null=True, blank=True)
    amount_series_b_stage = models.CharField(max_length=512, null=True, blank=True)
    amount_series_c_stage = models.CharField(max_length=512, null=True, blank=True)

    amount_specific_stage = models.CharField(max_length=512, null=True, blank=True)
    amount_total_stage = models.CharField(max_length=512, null=True, blank=True)

    total_teams_applying = models.TextField(null=True, blank=True)
    total_teams_accepted = models.TextField(null=True, blank=True)
    total_participants_accepted = models.TextField(null=True, blank=True)
    total_graduated_teams_accepted = models.TextField(null=True, blank=True)

    total_training_program = models.TextField(null=True, blank=True)
    total_organized_event = models.TextField(null=True, blank=True)

    total_coached_staff = models.TextField(null=True, blank=True)
    total_assisting_staff = models.TextField(null=True, blank=True)

    total_approximated_products = models.TextField(null=True, blank=True)

    program = models.ForeignKey(Program, related_name='batch_program')

    def __unicode__(self):
        return self.title


class InTheNews(CommonModel):

    url = models.URLField()
    date = models.DateField(null=True, blank=True)

    title = models.CharField(max_length=1024, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = files_widget.ImageField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created']


    def get_thumbnail(self):
        return instance_get_thumbnail(self, crop=None)