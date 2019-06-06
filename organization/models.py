import ast
from datetime import timedelta
import inspect
import json
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
import tagging

from ckeditor.fields import RichTextField
from common.constants import STATUS_PENDING, STATUS_DRAFT, SUMMARY_MAX_LENGTH, STATUS_PUBLISHED, STATUS_CHOICES, \
    TYPE_SOCIAL_ENTERPRISE, TYPE_STARTUP, TYPE_SUPPORTING_ORGANIZATION, TYPE_INVESTOR, TYPE_CHOICES, EXPAND_TYPE_CHOICES
from common.forms import BetterDecimalField, BetterPositiveIntegerField
from common.functions import instance_get_thumbnail

from common.models import AbstractPermalink, CommonTrashModel, CommonModel, CachedModel, PriorityModel, StatisitcAccess
from multiselectfield import MultiSelectField
from party.models import Party

import files_widget
from tagging_autocomplete_tagit.models import TagAutocompleteTagItField

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

    report_start_date = models.DateField(verbose_name='Report Start Date', null=True, blank=True,
        help_text='Start date of the reporting period for this IRIS report.'
    )
    report_end_date = models.DateField(verbose_name='Report End Date', null=True, blank=True,
        help_text='End date of the reporting period for this IRIS report.'
    )

    # Duplicates
    # name_of_organization = name
    # organization_web_address = homepage_url

    year_founded = models.PositiveSmallIntegerField(verbose_name='Year Founded', null=True, blank=True,
        help_text='Year the organization was founded.'
    )
    name_of_representative = models.CharField(verbose_name=_('Name of representative'), null=True, blank=True, max_length=255)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender_of_representative = models.CharField(verbose_name=_('Gender of representative'), null=True, blank=True, max_length=1, choices=GENDER_CHOICES)
    brief_bio_of_representative = RichTextField(verbose_name='Brief bio of representative', null=True, blank=True, config_name='minimal')

    LEGAL_STRUCTURE_CHOICES = (
        ('1', 'Corporation'),
        ('2', 'Limited Liability Company'),
        ('3', 'Non-Profit/Foundation/Association'),
        ('4', 'Partnership'),
        ('5', 'Sole-proprietorship'),
        ('6', 'Cooperative'),
        ('Other', 'Other')
    )
    legal_structure = models.CharField(verbose_name='Legal Structure', null=True, blank=True, max_length=255, choices=LEGAL_STRUCTURE_CHOICES,
        help_text='Current legal structure of the organization.'
    )
    location_of_organizations_headquarters = models.CharField(verbose_name=_("Location of Organization's Headquarters"), null=True, blank=True, max_length=255)
    store_phone_number_of_organizations_headquarters = models.TextField(null=True, blank=True)  # formset

    email_of_contact_person = models.EmailField(
        verbose_name=_('Email of Contact Person'),
        max_length=255,
        null=True,
        blank=True
    )

    store_location_of_organizations_operating_facilities = models.TextField(verbose_name="Location of Organization's Operating Facilities", null=True, blank=True) # formset

    name_of_referring_organization = models.CharField(verbose_name="Name of referring organization", null=True, blank=True, max_length=255)
    contact_information_of_referring_organization = models.CharField(verbose_name="Contact information of referring organization", null=True, blank=True, max_length=255)

    sector_activities = models.ManyToManyField('taxonomy.Topic', verbose_name='Sector Activities',  null=True, blank=True, related_name='sector_activities_topics',
        help_text= "Primary sectors impacted by the organization's operations."
    )
    TARGET_BENEFICIARY_CHOICES = (
        ('1', 'Women'),
        ('2', 'Diabilities'),
        ('3', 'Children'),
        ('4', 'Ethnic Minority'),
        ('5', 'Elderly'),
        ('6', 'NEET'),
        ('7', 'Migrant Workers'),
        ('8', 'Youth'),
        ('9', 'LGBT'),
        ('Other', 'Others')
    )
    target_beneficiary = MultiSelectField(verbose_name='Target Beneficiary', null=True, blank=True, max_length=255, choices=TARGET_BENEFICIARY_CHOICES)

    # Duplicates
    # company_description = description

    mission_statement = RichTextField(verbose_name='Mission Statement', null=True, blank=True,
        help_text='Mission statement of the organization.',
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

    productservice_type = models.ManyToManyField('taxonomy.Topic', verbose_name='Product/Service Type', null=True, blank=True, related_name='productservice_type_topics',
        help_text='Type of product or service provided by the organization'
    )
    productservice_description = RichTextField(verbose_name='Product/Service Description', null=True, blank=True,
        help_text='Description of the product or service.',
        config_name='default'
    )

    # ==============================================================
    definition_of_unit_of_measure_1 = models.CharField(verbose_name='Definition of unit of measure 1', null=True, blank=True, max_length=512)
    unit_of_impact_measurement_1 = models.CharField(verbose_name='Unit of Impact Measurement 1', null=True, blank=True, max_length=512)

    definition_of_unit_of_measure_2 = models.CharField(verbose_name='Definition of unit of measure 2', null=True, blank=True, max_length=512)
    unit_of_impact_measurement_2 = models.CharField(verbose_name='Unit of Impact Measurement 2', null=True, blank=True, max_length=512)

    definition_of_unit_of_measure_3 = models.CharField(verbose_name='Definition of unit of measure 3', null=True, blank=True, max_length=512)
    unit_of_impact_measurement_3 = models.CharField(verbose_name='Unit of Impact Measurement 3', null=True, blank=True, max_length=512)

    store_measurement_year_values = models.TextField(verbose_name="Measurement Year and Values", null=True, blank=True) # formset

    # ==============================================================

    CLIENT_TYPE_CHOICES = (
        ('1', 'Individuals/Households'),
        ('2', 'Microenterprises'),
        ('3', 'Small-to-Medium Enterprises'),
        ('4', 'Large Enterprises'),
        ('5', 'Non-profit / Non-Governmental Organization / Foundations'),
        ('6', 'Government'),
        ('7', 'International Organizations'),
        ('Other', 'Others')
    )
    client_type = MultiSelectField(verbose_name='Client Type', null=True, blank=True, max_length=255, choices=CLIENT_TYPE_CHOICES,
        help_text="Types of entities that are buyers or recipients of the organization's products and/or services"
    )
    client_information = RichTextField(verbose_name='Client Information', null=True, blank=True,
        help_text='Name of major clients, if they are business or government',
        config_name='minimal'
    )

    client_locations = models.ManyToManyField('taxonomy.Country', verbose_name='Client Locations', null=True, blank=True, related_name='client_locations',
    )
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

    store_top_3_major_investors_year_and_amount = models.TextField(verbose_name='Top 3 major investors, year and amount', null=True, blank=True)
    store_top_3_major_donors_year_and_amount = models.TextField(verbose_name='Top 3 major donors, year and amount', null=True, blank=True)

    ANNUAL_REVENUE_CHOICES = (
        ('1', 'Under $50K'),
        ('2', '$50K-$100K'),
        ('3', '$100K-$250K'),
        ('4', '$250K-$500K'),
        ('5', '$500K-$1MM'),
        ('6', '$1MM-$2MM'),
        ('7', '$1MM-$5MM'),
        ('8', 'Over $5MM')
    )
    annual_revenue = models.CharField(verbose_name='Annual revenue', null=True, blank=True, max_length=255, choices=ANNUAL_REVENUE_CHOICES)
    REVENUE_MODEL_CHOICES = (
        ('1', 'Social Business (Business revenue more than 75% of total revenue)'),
        ('2', 'Hybird (Business revenue range 25% to 75% of total revenue)'),
        ('3', 'Charity (Business revenue less than 25%)')
    )
    revenue_model = models.CharField(verbose_name='Revenue Model', null=True, blank=True, max_length=255, choices=REVENUE_MODEL_CHOICES)
    earned_revenue = BetterDecimalField(
        verbose_name='Earned Revenue',
        suffix=settings.CURRENCY, # This is example for suffix field
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Revenue resulting from all business activities during the reporting period. Earned revenue is total revenues less "Contributed Revenue" (Grants and Donations).'
    )
    cost_of_goods_sold = BetterDecimalField(
        verbose_name='Cost of Goods Sold',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Direct costs attributable to the production of the goods sold by the organization during the reporting period.  The cost should include all costs of purchase, costs of conversion, and other direct costs incurred in producing and selling the organization's"
    )
    gross_profit = BetterDecimalField(
        verbose_name='Gross Profit',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="The organization's residual profit after selling a product or service and deducting the costs directly associated with its production. Gross Profit is 'Earned Revenue' less 'Cost of Goods Sold'."
    )
    personnel_expense = BetterDecimalField(
        verbose_name='Personnel Expense',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Expenses related to personnel, including wages, benefits, trainings, and payroll taxes incurred by the organization during the reporting period.'
    )
    selling_general_and_administration_expense = BetterDecimalField(
        verbose_name='Selling, General, and Administration Expense',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Sum of all direct and indirect selling expenses and all general and administrative expenses incurred by the organization during the reporting period.'
    )
    operating_expense = BetterDecimalField(
        verbose_name='Operating Expense',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Expenditures incurred by the organization as a result of performing its normal business operations. NOTE: For financial services companies this does not include Financial Expenses or provisions for loan losses (impairment losses).'
    )
    ebitda = BetterDecimalField(
        verbose_name='EBITDA',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Organization's earnings, excluding contributed revenues, before interest, taxes, depreciation and amortization during the reporting period."
    )
    interest_expense = BetterDecimalField(
        verbose_name='Interest Expense',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Interest incurred during the reporting period on all liabilities, including any client deposit accounts held by the organization, borrowings, subordinated debt, and other liabilities."
    )
    depreciation_and_amortization_expense = BetterDecimalField(
        verbose_name='Depreciation and Amortization Expense',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Value of expenses recorded by the organization during the reporting period for depreciation and amortization.'
    )
    taxes = BetterDecimalField(
        verbose_name='Taxes',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Value of corporate income taxes expensed by the organization during the reporting period.'
    )
    net_income_before_donations = BetterDecimalField(
        verbose_name='Net Income Before Donations',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Net Income or change in unrestricted net assets resulting from all business activities during the reporting period, excluding donations. The organization's net profit before donations."
    )
    contributed_revenue = BetterDecimalField(
        verbose_name='Contributed Revenue',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Contributed revenue during the reporting period. Includes both unrestricted and restricted operating grants and donations and in-kind contributions. Does NOT include equity grants for capital, grants that are intended for future operating periods, or gra"
    )
    net_income = BetterDecimalField(
        verbose_name='Net Income',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Net Income or change in unrestricted net assets resulting from all business activities during the reporting period and all Contributed Revenue. The organization's net profit."
    )
    # ===================================== New field section 3 after demo
    current_assets = BetterDecimalField(
        verbose_name='Current Assets',
        max_digits=19,
        suffix=settings.CURRENCY,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of all assets that are reasonably expected to be converted into cash within one year in the normal course of business. Current assets can include cash, accounts receivable, inventory, marketable securities, prepa."
    )
    total_value_of_loans_and_investments = BetterDecimalField(
        verbose_name='Total Value of Loans and Investments',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of financial portfolio products including loans and investments in investees."
    )
    financial_assets = BetterDecimalField(
        verbose_name='Financial Assets',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of all assets that represent debt, equity, and cash assets such as: stocks, bonds, mutual funds, cash, and cash management accounts.  Values of assets should be based upon fair market value where efficient second."
    )
    fixed_assets = BetterDecimalField(
        verbose_name='Fixed Assets',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of all long-term tangible assets  that are not expected to be converted into cash in the current or upcoming fiscal year, e.g., buildings, real estate, production equipment, and furniture. Sometimes called PLANT."
    )
    total_assets = BetterDecimalField(
        verbose_name='Total Assets',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of all assets."
    )
    retained_earnings = BetterDecimalField(
        verbose_name='Retained Earnings',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="The sum of the organization's profits, cumulative from inception to the end of the reporting period, not paid out as dividends, but retained by the company to be reinvested in its core business or to pay debt. Also referred to as retained capital, accumul."
    )
    accounts_payable = BetterDecimalField(
        verbose_name='Accounts Payable',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of all outstanding debts that must be paid within a given period of time in order to avoid default."
    )
    accounts_receivable = BetterDecimalField(
        verbose_name='Accounts Receivable',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of outstanding debts from clients who received goods or services on credit."
    )
    current_liabilities = BetterDecimalField(
        verbose_name='Current Liabilities',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of all liabilities that are expected to be settled with one year in the normal course of business. Current liabilities can include accounts payable, lines of credit, or other short term debts."
    )
    financial_liabilities = BetterDecimalField(
        verbose_name='Financial Liabilities',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value, at the end of the reporting period, of an organization's financial liabilities. Financial liabilities include all borrowed funds, deposits held, or other contractual obligations to deliver cash."
    )
    loans_payable = BetterDecimalField(
        verbose_name='Loans Payable',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="The remaining balance, at the end of the reporting period, on all the organization's outstanding debt obligations carried on the balance sheet."
    )
    total_liabilities = BetterDecimalField(
        verbose_name='Total Liabilities',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of organization's liabilities at the end of the reporting period."
    )
    equity_or_net_assets = BetterDecimalField(
        verbose_name='Equity or Net Assets',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="The residual interest, at the end of the reporting period, in the assets of the organization after deducting all its liabilities."
    )
    cash_and_cash_equivalents_period_start = BetterDecimalField(
        verbose_name='Cash and Cash Equivalents- Period Start',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of the organization's cash equivalents at the beginning of the reporting period."
    )
    cash_flow_from_operating_activities = BetterDecimalField(
        verbose_name='Cash Flow from Operating Activities',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of cash flows during the reporting period related to operating activities. Operating activities are the principal revenue-producing activities of the entity and other activities that are not investing or financing activities."
    )
    cash_flow_from_investing_activities = BetterDecimalField(
        verbose_name='Cash Flow from Investing Activities',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of cash flows during the reporting period related to investing activities by the organization. Investing activities are the acquisition and disposal of long-term assets and other investments that are not considered to be cash equivalents."
    )
    cash_flow_from_financing_activities = BetterDecimalField(
        verbose_name='Cash Flow from Financing Activities',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of cash flows during the reporting period related to financing activities by the organization. Financing activities are activities that result in changes in the size and composition of the contributed equity and borrowings of the organization."
    )
    new_investment_capital = BetterDecimalField(
        verbose_name='New Investment Capital',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of cash flows from the organization's financing activities (both loans and investments) during the reporting period."
    )
    net_cash_flow = BetterDecimalField(
        verbose_name='Net Cash Flow',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="The net cash flow of the organization during the reporting period. Net cash flow equals inflows less outflows of cash and cash equivalents."
    )
    cash_and_cash_equivalents_period_end = BetterDecimalField(
        verbose_name='Cash and Cash Equivalents- Period End',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of the organizations cash equivalents at the end of the reporting period."
    )
    revenue_growth = BetterDecimalField(
        verbose_name='Revenue Growth',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Growth in value of the organization's revenue from one reporting period to another.Calculation: (Earned Revenue in reporting period 2 - Earned Revenue in reporting period 1) / Earned Revenue in reporting period 1"
    )
    income_growth = BetterDecimalField(
        verbose_name='Income Growth',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Growth in value of the organization's Net income Before Donations from one reporting period to another.Calculation: (Net Income Before Donations in reporting period 2 - Net Income Before Donations in reporting period 1) / Net Income Before Donations"
    )
    gross_margin = BetterDecimalField(
        verbose_name='Gross Margin',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Percent of earned revenues that the organization retains after incurring the direct costs associated with producing the goods and services sold by the company.Calculation: 'Cost of Goods Sold' / 'Earned Revenue'"
    )
    operating_profit_margin = BetterDecimalField(
        verbose_name='Operating Profit Margin',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Organization's effectiveness at managing costs and turning earned revenues into income.Calculation: (Net Income Before Donations + Taxes) / Earned Revenue"
    )
    working_capital = BetterDecimalField(
        verbose_name='Working Capital',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Organization's operating liquidity.Calculation: Current Assets - Current Liabilities"
    )
    return_on_assets_roa = BetterDecimalField(
        verbose_name='Return on Assets (ROA)',
        suffix='%',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Measurement of how well the organization uses assets to generate returns.Calculation: Net Income Before Donations / Average Total Assets Average Total Assets: (Total Assets at the beginning of the period + Total Assets at the end of the period) / 2"
    )
    return_on_equity_roe = BetterDecimalField(
        verbose_name='Return on Equity (ROE)',
        suffix='%',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Measurement of commercial profitability.Calculation: Net Income Before Donations / Average Equity or Net Assets Average Equity or Net Assets: (Average Equity or Net Assets at the beginning of the period + Average Equity or Net Assets at the end of"
    )
    fixed_costs = BetterDecimalField(
        verbose_name='Fixed Costs',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Costs that do not vary based on production or sales levels."
    )
    entrepreneur_investment = BetterDecimalField(
        verbose_name='Entrepreneur Investment',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of the equity and/or other financial contribution in the organization provided by the entrepreneur/s at the time of investment."
    )
    community_service_donations = BetterDecimalField(
        verbose_name='Community Service Donations',
        suffix=settings.CURRENCY,
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Value of all charitable donations made by the organization"
    )
    board_of_directors = BetterPositiveIntegerField(
        verbose_name='Board of Directors',
        suffix='Person',
        null=True,
        blank=True,
        help_text="Number of members of organization's Board of Directors or other governing body, as of the end of the reporting period."
    )
    female_ownership = BetterDecimalField(
        verbose_name='Female Ownership',
        suffix='%',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Percentage of the company that is female-owned as of the end of the reporting period.Calculation: number of total shares owned by females/number of total shares.Note: Where regional or local laws apply for calculating ownership by previously excluded"
    )
    financial_statement_review = models.NullBooleanField(
        verbose_name='Financial Statement Review',
        null=True,
        blank=True,
        help_text="Indicate whether it is the organization's policy to produce financial statements that are verified annually by a certified accountant."
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
        verbose_name='Full-time Employees',
        null=True,
        blank=True,
        help_text="Number of full-time employees at the end of the reporting period."
    )
    full_time_employees_female = models.PositiveIntegerField(
        verbose_name='Full-time Employees: Female',
        null=True,
        blank=True,
        help_text="Number of full-time female employees at the end of the reporting period."
    )
    part_time_employees = models.PositiveIntegerField(
        verbose_name='Part-time Employees',
        null=True,
        blank=True,
        help_text="Number of part-time employees at the end of the reporting period."
    )
    part_time_employees_female = models.PositiveIntegerField(
        verbose_name='Part-time Employees: Female',
        null=True,
        blank=True,
        help_text="Number of female part-time employees at the end of the reporting period."
    )
    volunteer_hours_worked = BetterDecimalField(
        verbose_name='Volunteer Hours Worked',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total number of hours worked by volunteers that supported the organization during the reporting period."
    )
    client_individuals = BetterDecimalField(
        verbose_name='Client Individuals',
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Number of individuals or households who were clients during the reporting period.For microfinance clients, this refers to active clients.For healthcare providers, this refers to patients.Note: Organizations tracking households should report num"
    )
    client_organizations = models.PositiveIntegerField(
        verbose_name='Client Organizations',
        null=True,
        blank=True,
        help_text="Number of businesses or other organizations that were clients during the reporting period."
    )
    # =============  End new field
    store_team_information = models.TextField(
        verbose_name='Key Officers (Name and title)',
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
        ('1', 'Grant'),
        ('2', 'Loan'),
        ('3', 'Equity')
    )
    possible_form_of_financial_support = MultiSelectField(verbose_name='Possible form of financial support', null=True, blank=True, max_length=255, choices=POSSIBLE_FORM_OF_FINANCIAL_SUPPORT_CHOICES,
        help_text="Grant, Loan or investment"
    )
    potential_size_of_investment = BetterDecimalField(verbose_name='Potential size of investment', max_digits=19, decimal_places=2, null=True, blank=True,
        help_text="Potential size of investment in %s" % settings.CURRENCY
    )
    POTENTIAL_USE_OF_INVESTMENT_CHOICES = (
        ('1', 'Land/building'),
        ('2', 'Equipment'),
        ('3', 'Human resources development'),
        ('4', 'Revolving Capital'),
        ('Other', 'Other')
    )
    potential_use_of_investment = MultiSelectField(verbose_name='Potential use of investment', null=True, blank=True, max_length=255, choices=POTENTIAL_USE_OF_INVESTMENT_CHOICES)
    POSSIBLE_FORM_OF_NON_FINANCIAL_SUPPORT_CHOICES = (
        ('1', 'Strategy Planning'),
        ('2', 'Financial Management'),
        ('4', 'PR'),
        ('5', 'HR'),
        ('6', 'Legal'),
        ('7', 'Market Access'),
        ('8', 'External Relations'),
        ('9', 'Techinical Expertise'),
        ('10', 'Fundraising'),
        ('3', 'Operational Management'),
        ('Other', 'Others')
    )
    possible_form_of_non_financial_support = MultiSelectField(verbose_name='Possible form of non-financial support', null=True, blank=True, max_length=255, choices=POSSIBLE_FORM_OF_NON_FINANCIAL_SUPPORT_CHOICES,
        help_text="Strategy, PR, Marketing, Legal, Operation Management, Financial Management"
    )

class Organization(Party, AbstractPermalink, AbstractOrganizationSection1, AbstractOrganizationSection2, \
                   AbstractOrganizationSection3, AbstractOrganizationSection4, AbstractOrganizationSection5):

    inst_type = 'organization'

    KIND_ORGANIZATION = 'organization'
    KIND_PRODUCT = 'product'

    KIND_CHOICES = (
        (KIND_PRODUCT, _('Product/Service')),
        (KIND_ORGANIZATION, pgettext_lazy('model_choice', 'Organization')),
    )

    TYPE_SOCIAL_ENTERPRISE = TYPE_SOCIAL_ENTERPRISE
    TYPE_STARTUP = TYPE_STARTUP
    TYPE_SUPPORTING_ORGANIZATION = TYPE_SUPPORTING_ORGANIZATION
    TYPE_INVESTOR = TYPE_INVESTOR

    DEFAULT_TYPE_RECEIVER = settings.DEFAULT_TYPE_RECEIVER

    TYPE_CHOICES = TYPE_CHOICES
    EXPAND_TYPE_CHOICES = EXPAND_TYPE_CHOICES

    # kind
    kind = models.CharField(max_length=100, choices=KIND_CHOICES, default=KIND_ORGANIZATION)

    # Relation
    created_by = models.ForeignKey(USER_MODEL, related_name='created_by')
    published_by = models.ForeignKey(USER_MODEL, related_name='published_by', null=True, blank=True)

    admins = models.ManyToManyField(USER_MODEL, related_name='admins')
    jobs = models.ManyToManyField('organization.Job', related_name='organization_jobs', null=True, blank=True)


    # Internal
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

    growth_stage = models.ManyToManyField('taxonomy.OrganizationGrowthStage', null=True, blank=True, related_name='organization_growth_stage')
    deal_size_start = models.PositiveIntegerField(null=True, blank=True)
    deal_size_end = models.PositiveIntegerField(null=True, blank=True)

    priority = models.PositiveIntegerField(default=0)
    ordering = models.PositiveIntegerField(null=True, blank=True)

    # External
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    homepage_url = models.URLField(max_length=255, null=True, blank=True)

    # Meta
    type_of_organization = models.CharField(max_length=128, choices=TYPE_CHOICES, default=DEFAULT_TYPE_RECEIVER)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)

    created_raw = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    changed = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)

    point = models.IntegerField(default=0)

    cached_vars = ['status', 'published']


    class Meta:
        ordering = ['-store_popular']

    def get_class_display(self):
        class_display = dict(EXPAND_TYPE_CHOICES).get(self.organization_primary_role.permalink)

        if not class_display:
            class_display = dict(TYPE_CHOICES).get(self.organization_primary_role.permalink)

        if not class_display:
            class_display = super(Organization, self).get_class_display()

        return class_display

    def get_thumbnail(self):
        return instance_get_thumbnail(self, crop=None)

    def get_thumbnail_in_primary(self):
        return instance_get_thumbnail(self, size='150x150', crop=None, upscale=False)

    def get_thumbnail_images(self):
        return instance_get_thumbnail(self, field_name='images', size='500x500', crop=None, upscale=False, no_default=True)


    def get_absolute_url(self):
        if not self.permalink:
            return ''

        return reverse('organization_detail', args=[self.permalink])

    def get_display_name(self):
        return self.name

    def get_short_name(self):
        return self.get_display_name()

    def get_summary(self):
        return truncatechars(self.summary or '', SUMMARY_MAX_LENGTH)

    @property
    def last_visit_date(self):
        organization_type = ContentType.objects.get_for_model(self)
        try:
            last_visit = StatisitcAccess.objects.filter(content_type__pk=organization_type.id, object_id=self.id).latest('created').created
        except StatisitcAccess.DoesNotExist:
            last_visit = self.created

        return last_visit

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


    def save(self, not_changed=False, *args, **kwargs):

        # Logic make from "test_uptodate_status (domain.tests.test_model.TestStatement)"

        if not self.id and not self.created_raw:
            self.created_raw = timezone.now()


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
        if not self.id:
            super(Organization, self).save(*args, **kwargs)
            instance = Organization.objects.get(id=self.id)

            instance.save(not_changed=True)

        else:

            self.ordering = int('%s%s' % (('0'*2 + '%s' % self.priority)[-2:], ('0'*8 + '%s' % self.id)[-8:]))
            super(Organization, self).save(*args, **kwargs)




class Job(CommonModel, CachedModel, PriorityModel):

    POSITION_DEFAULT = 'full-time'
    POSITION_CHOICES = (
        (POSITION_DEFAULT, 'Full Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('cofounder', 'Cofounder')
    )
    ROLE_CHOICES = (
        ('administration', 'Administration'),
        ('analyst-scientist', 'Analyst/Scientist'),
        ('designer', 'Designer'),
        ('finance-accounting', 'Finance/Accounting'),
        ('hardware-engineer', 'Hardware Engineer'),
        ('hr', 'HR'),
        ('legal', 'Legal'),
        ('management', 'Management'),
        ('marketing-and-pr', 'Marketing and PR'),
        ('operations', 'Operations'),
        ('others', 'Others'),
        ('product-manager', 'Product Manager'),
        ('sales', 'Sales'),
        ('software-engineer', 'Software Engineer'),
    )

    # Deprecate
    # organization = models.ForeignKey(Organization, related_name='job_organization', null=True, blank=True) # denormalize

    STATUS_CHOICES = (
        (STATUS_PUBLISHED, 'Active'),
        (STATUS_PENDING, 'Close'),
    )
    REMOTE_CHOICES = (
        (False, 'No'),
        (True, 'Yes'),
    )

    title = models.CharField(max_length=255)
    contact_information = RichTextField()
    description = RichTextField(null=True, blank=True)

    role = models.CharField(null=True, blank=True, max_length=128, choices=ROLE_CHOICES)

    position = models.CharField(null=True, blank=True, max_length=128, choices=POSITION_CHOICES, default=POSITION_DEFAULT)

    salary_min = models.PositiveIntegerField(null=True, blank=True) # USD
    salary_max = models.PositiveIntegerField(null=True, blank=True) # USD

    equity_min = BetterDecimalField(null=True, blank=True, max_digits=19, decimal_places=2) # %
    equity_max = BetterDecimalField(null=True, blank=True, max_digits=19, decimal_places=2) # %

    remote = models.NullBooleanField(null=True, blank=True, default=False)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)

    country = models.ForeignKey('taxonomy.Country', null=True, blank=True, related_name='job_country')
    location = models.CharField(max_length=255, null=True, blank=True)

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

        if self.position:
            summary.append(self.get_position_display())

        if self.role:
            summary.append(self.get_role_display())

        if self.salary_min or self.salary_max:
            if self.salary_max:
                summary.append('%s%s - %s%s' % (settings.CURRENCY_SHORT, self.salary_min, settings.CURRENCY_SHORT, self.salary_max))
            else:
                summary.append('%s%s' % (settings.CURRENCY_SHORT, self.salary_min))

        return ', '.join(summary)

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
        super(Job, self).save()


tagging.register(Job, tag_descriptor_attr='skill_set')