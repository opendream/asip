# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import common.forms


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '__first__'),
        ('organization', '0004_auto_20150112_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='client_locations',
            field=models.ManyToManyField(related_name='client_locations', to='taxonomy.Country', blank=True, help_text=b'Type of product or service provided by the organization', null=True, verbose_name=b'Product/Service Type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='equity_max',
            field=common.forms.BetterDecimalField(null=True, max_digits=19, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='equity_min',
            field=common.forms.BetterDecimalField(null=True, max_digits=19, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='accounts_payable',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value, at the end of the reporting period, of all outstanding debts that must be paid within a given period of time in order to avoid default.', null=True, verbose_name=b'Accounts Payable'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='accounts_receivable',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value, at the end of the reporting period, of outstanding debts from clients who received goods or services on credit.', null=True, verbose_name=b'Accounts Receivable'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='board_of_directors',
            field=common.forms.BetterPositiveIntegerField(help_text=b"Number of members of organization's Board of Directors or other governing body, as of the end of the reporting period.", null=True, verbose_name=b'Board of Directors', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='cash_and_cash_equivalents_period_end',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value of the organizations cash equivalents at the end of the reporting period.', null=True, verbose_name=b'Cash and Cash Equivalents- Period End'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='cash_and_cash_equivalents_period_start',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Value of the organization's cash equivalents at the beginning of the reporting period.", null=True, verbose_name=b'Cash and Cash Equivalents- Period Start'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='cash_flow_from_financing_activities',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value of cash flows during the reporting period related to financing activities by the organization. Financing activities are activities that result in changes in the size and composition of the contributed equity and borrowings of the organization.', null=True, verbose_name=b'Cash Flow from Financing Activities'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='cash_flow_from_investing_activities',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value of cash flows during the reporting period related to investing activities by the organization. Investing activities are the acquisition and disposal of long-term assets and other investments that are not considered to be cash equivalents.', null=True, verbose_name=b'Cash Flow from Investing Activities'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='cash_flow_from_operating_activities',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value of cash flows during the reporting period related to operating activities. Operating activities are the principal revenue-producing activities of the entity and other activities that are not investing or financing activities.', null=True, verbose_name=b'Cash Flow from Operating Activities'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='client_individuals',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Number of individuals or households who were clients during the reporting period.For microfinance clients, this refers to active clients.For healthcare providers, this refers to patients.Note: Organizations tracking households should report num', null=True, verbose_name=b'Client Individuals'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='community_service_donations',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value of all charitable donations made by the organization', null=True, verbose_name=b'Community Service Donations'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='contributed_revenue',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Contributed revenue during the reporting period. Includes both unrestricted and restricted operating grants and donations and in-kind contributions. Does NOT include equity grants for capital, grants that are intended for future operating periods, or gra', null=True, verbose_name=b'Contributed Revenue'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='cost_of_goods_sold',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Direct costs attributable to the production of the goods sold by the organization during the reporting period.  The cost should include all costs of purchase, costs of conversion, and other direct costs incurred in producing and selling the organization's", null=True, verbose_name=b'Cost of Goods Sold'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='current_assets',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value, at the end of the reporting period, of all assets that are reasonably expected to be converted into cash within one year in the normal course of business. Current assets can include cash, accounts receivable, inventory, marketable securities, prepa.', null=True, verbose_name=b'Current Assets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='current_liabilities',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value, at the end of the reporting period, of all liabilities that are expected to be settled with one year in the normal course of business. Current liabilities can include accounts payable, lines of credit, or other short term debts.', null=True, verbose_name=b'Current Liabilities'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='depreciation_and_amortization_expense',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value of expenses recorded by the organization during the reporting period for depreciation and amortization.', null=True, verbose_name=b'Depreciation and Amortization Expense'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='earned_revenue',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Revenue resulting from all business activities during the reporting period. Earned revenue is total revenues less "Contributed Revenue" (Grants and Donations).', null=True, verbose_name=b'Earned Revenue'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='ebitda',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Organization's earnings, excluding contributed revenues, before interest, taxes, depreciation and amortization during the reporting period.", null=True, verbose_name=b'EBITDA'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='entrepreneur_investment',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value of the equity and/or other financial contribution in the organization provided by the entrepreneur/s at the time of investment.', null=True, verbose_name=b'Entrepreneur Investment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='equity_or_net_assets',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'The residual interest, at the end of the reporting period, in the assets of the organization after deducting all its liabilities.', null=True, verbose_name=b'Equity or Net Assets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='female_ownership',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Percentage of the company that is female-owned as of the end of the reporting period.Calculation: number of total shares owned by females/number of total shares.Note: Where regional or local laws apply for calculating ownership by previously excluded', null=True, verbose_name=b'Female Ownership'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='financial_assets',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value, at the end of the reporting period, of all assets that represent debt, equity, and cash assets such as: stocks, bonds, mutual funds, cash, and cash management accounts.  Values of assets should be based upon fair market value where efficient second.', null=True, verbose_name=b'Financial Assets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='financial_liabilities',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Value, at the end of the reporting period, of an organization's financial liabilities. Financial liabilities include all borrowed funds, deposits held, or other contractual obligations to deliver cash.", null=True, verbose_name=b'Financial Liabilities'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='fixed_assets',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value, at the end of the reporting period, of all long-term tangible assets  that are not expected to be converted into cash in the current or upcoming fiscal year, e.g., buildings, real estate, production equipment, and furniture. Sometimes called PLANT.', null=True, verbose_name=b'Fixed Assets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='fixed_costs',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Costs that do not vary based on production or sales levels.', null=True, verbose_name=b'Fixed Costs'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='gross_margin',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Percent of earned revenues that the organization retains after incurring the direct costs associated with producing the goods and services sold by the company.Calculation: 'Cost of Goods Sold' / 'Earned Revenue'", null=True, verbose_name=b'Gross Margin'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='gross_profit',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"The organization's residual profit after selling a product or service and deducting the costs directly associated with its production. Gross Profit is 'Earned Revenue' less 'Cost of Goods Sold'.", null=True, verbose_name=b'Gross Profit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='income_growth',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Growth in value of the organization's Net income Before Donations from one reporting period to another.Calculation: (Net Income Before Donations in reporting period 2 - Net Income Before Donations in reporting period 1) / Net Income Before Donations", null=True, verbose_name=b'Income Growth'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='interest_expense',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Interest incurred during the reporting period on all liabilities, including any client deposit accounts held by the organization, borrowings, subordinated debt, and other liabilities.', null=True, verbose_name=b'Interest Expense'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='legal_structure',
            field=models.CharField(choices=[(b'1', b'Corporation'), (b'2', b'Limited Liability Company'), (b'3', b'Non-Profit/Foundation/Association'), (b'4', b'Partnership'), (b'5', b'Sole-proprietorship'), (b'6', b'Cooperative'), (b'Other', b'Other')], max_length=255, blank=True, help_text=b'Current legal structure of the organization.', null=True, verbose_name=b'Legal Structure'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='loans_payable',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"The remaining balance, at the end of the reporting period, on all the organization's outstanding debt obligations carried on the balance sheet.", null=True, verbose_name=b'Loans Payable'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='net_cash_flow',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'The net cash flow of the organization during the reporting period. Net cash flow equals inflows less outflows of cash and cash equivalents.', null=True, verbose_name=b'Net Cash Flow'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='net_income',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Net Income or change in unrestricted net assets resulting from all business activities during the reporting period and all Contributed Revenue. The organization's net profit.", null=True, verbose_name=b'Net Income'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='net_income_before_donations',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Net Income or change in unrestricted net assets resulting from all business activities during the reporting period, excluding donations. The organization's net profit before donations.", null=True, verbose_name=b'Net Income Before Donations'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='new_investment_capital',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Value of cash flows from the organization's financing activities (both loans and investments) during the reporting period.", null=True, verbose_name=b'New Investment Capital'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='operating_expense',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Expenditures incurred by the organization as a result of performing its normal business operations. NOTE: For financial services companies this does not include Financial Expenses or provisions for loan losses (impairment losses).', null=True, verbose_name=b'Operating Expense'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='operating_profit_margin',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Organization's effectiveness at managing costs and turning earned revenues into income.Calculation: (Net Income Before Donations + Taxes) / Earned Revenue", null=True, verbose_name=b'Operating Profit Margin'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='personnel_expense',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Expenses related to personnel, including wages, benefits, trainings, and payroll taxes incurred by the organization during the reporting period.', null=True, verbose_name=b'Personnel Expense'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='possible_form_of_non_financial_support',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(b'1', b'Strategy Planning'), (b'2', b'Financial Management'), (b'4', b'PR'), (b'5', b'HR'), (b'6', b'Legal'), (b'7', b'Market Access'), (b'8', b'External Relations'), (b'9', b'Techinical Expertise'), (b'10', b'Fundraising'), (b'3', b'Operational Management'), (b'Other', b'Others')], max_length=255, blank=True, help_text=b'Strategy, PR, Marketing, Legal, Operation Management, Financial Management', null=True, verbose_name=b'Possible form of non-financial support'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='potential_size_of_investment',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Potential size of investment in USD', null=True, verbose_name=b'Potential size of investment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='retained_earnings',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"The sum of the organization's profits, cumulative from inception to the end of the reporting period, not paid out as dividends, but retained by the company to be reinvested in its core business or to pay debt. Also referred to as retained capital, accumul.", null=True, verbose_name=b'Retained Earnings'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='return_on_assets_roa',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Measurement of how well the organization uses assets to generate returns.Calculation: Net Income Before Donations / Average Total Assets Average Total Assets: (Total Assets at the beginning of the period + Total Assets at the end of the period) / 2', null=True, verbose_name=b'Return on Assets (ROA)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='return_on_equity_roe',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Measurement of commercial profitability.Calculation: Net Income Before Donations / Average Equity or Net Assets Average Equity or Net Assets: (Average Equity or Net Assets at the beginning of the period + Average Equity or Net Assets at the end of', null=True, verbose_name=b'Return on Equity (ROE)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='revenue_growth',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Growth in value of the organization's revenue from one reporting period to another.Calculation: (Earned Revenue in reporting period 2 - Earned Revenue in reporting period 1) / Earned Revenue in reporting period 1", null=True, verbose_name=b'Revenue Growth'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='selling_general_and_administration_expense',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Sum of all direct and indirect selling expenses and all general and administrative expenses incurred by the organization during the reporting period.', null=True, verbose_name=b'Selling, General, and Administration Expense'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='taxes',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value of corporate income taxes expensed by the organization during the reporting period.', null=True, verbose_name=b'Taxes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='total_assets',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value, at the end of the reporting period, of all assets.', null=True, verbose_name=b'Total Assets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='total_liabilities',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Value of organization's liabilities at the end of the reporting period.", null=True, verbose_name=b'Total Liabilities'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='total_value_of_loans_and_investments',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Value, at the end of the reporting period, of financial portfolio products including loans and investments in investees.', null=True, verbose_name=b'Total Value of Loans and Investments'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='volunteer_hours_worked',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Total number of hours worked by volunteers that supported the organization during the reporting period.', null=True, verbose_name=b'Volunteer Hours Worked'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='working_capital',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b"Organization's operating liquidity.Calculation: Current Assets - Current Liabilities", null=True, verbose_name=b'Working Capital'),
            preserve_default=True,
        ),
    ]
