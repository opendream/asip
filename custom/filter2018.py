# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

FILTER = {
    'startup': {
        'TITLE': _('Startup'),
        'RESULT_TITLE': _('companies'),
        'HEAD_TITLE': _('Company'),

        'CREATE_URL': '/organization/startup/create/',
        'CREATE_URL_PARAMS': (),

        'HEADER_BANNER': '/static/images/bg-startup@2x.png',
        'PROMOTE_LIST': '',

        'API_URL': '/api/v1/organization/search/',
        'HAPPENING_EXTRA_PARAMS': {
            'limit': 10,
            'offset': 0,
            'receiver_or_actor__type_of_organization': 'startup'
        },

        'EXTRA_PARAMS': {
            'type_of_organization': 'startup',
            'limit': 10,
            'resource': 'PartyLiteResource',
            'none_to_all': 1
        },
        'ORDER_BY_FIELDS': ['focus_sector'],
        'FILTERS': [
            {
                'api_url': '/api/v1/type_of_focus_sector/',
                'label': _('Focus Sectors'),
                'field_name': 'focus_sector__permalink'
            },
            {
                'api_url': '/api/v1/type_of_stage_of_participant/',
                'label': _('Stage'),
                'field_name': 'stage_of_participants__permalink'
            },
            {
                'api_url': '/api/v1/type_of_financial_source/',
                'label': _('Received Investment'),
                'field_name': 'financial_source__permalink'
            },
            {
                'api_url': '/api/v1/type_of_assistantship/',
                'label': _('Assistance Required'),
                'field_name': 'assistance_organization__permalink'
            }
        ],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [
            {
                'label': _('Focus Sectors'),
                'field_name': 'focus_sector',
                'is_m2m': True
            },
            {
                'label': _('Stage'),
                'field_name': 'stage_of_participants',
                'is_m2m': True
            },
            {
                'label': _('Received Investment'),
                'field_name': 'financial_source',
                'is_m2m': True
            },
            {
                'label': _('Assistance Required'),
                'field_name': 'assistance_organization',
                'field_attribute': '.assistance',
                'is_m2m': True
            }
        ]
    },
    'investor': {
        'TITLE': _('Investor'),
        'RESULT_TITLE': _('investor'),
        'HEAD_TITLE': _('Investor'),

        'CREATE_URL': '/organization/investor/create/',
        'CREATE_URL_PARAMS': (),

        'HEADER_BANNER': '/static/images/bg-investor@2x.png',
        'PROMOTE_LIST': '',

        'API_URL': '/api/v1/organization/search/',
        'HAPPENING_EXTRA_PARAMS': {
            'limit': 10,
            'offset': 0,
            'receiver_or_actor__type_of_organization': 'investor'
        },
        'EXTRA_PARAMS': {
            'type_of_organization': 'investor',
            'limit': 10,
            'resource': 'PartyLiteResource',
            'none_to_all': 1
        },
        'ORDER_BY_FIELDS': ['focus_sector'],
        'FILTERS': [
            {
                'api_url': '/api/v1/investor_type/',
                'label': _('Investor Type'),
                'field_name': 'investor_type__permalink'
            },
            {
                'api_url': '/api/v1/type_of_focus_sector/',
                'label': _('Focus Sectors'),
                'field_name': 'focus_sector__permalink'
            },
            {
               'api_url': '/api/v1/type_of_funding/',
               'label': _('Funding Type'),
               'field_name': 'funding_type__permalink'
            },
        ],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [
            {
                'label': _('Investor Type'),
                'field_name': 'investor_type',
                'is_m2m': False
            },
            {
                'label': _('Focus Sectors'),
                'field_name': 'focus_sector',
                'is_m2m': True
            },
            {
                'label': _('Funding Type'),
                'field_name': 'funding_type',
                'is_m2m': True
            },
        ]
    },
    'supporter': {
        'TITLE': _('Supporter'),
        'RESULT_TITLE': _('organizations'),
        'HEAD_TITLE': _('Organization'),

        'CREATE_URL': '/organization/supporter/create/',
        'CREATE_URL_PARAMS': (),

        'HEADER_BANNER': '/static/images/bg-supporter@2x.png',
        'PROMOTE_LIST': '',

        'API_URL': '/api/v1/organization/search/',
        'HAPPENING_EXTRA_PARAMS': {
            'limit': 10,
            'offset': 0,
            'receiver_or_actor__type_of_organization': 'supporter'
        },
        'EXTRA_PARAMS': {
            'type_of_organization': 'supporter,program',
            'limit': 10,
            'resource': 'PartyLiteResource',
            'none_to_all': 1
        },
        'ORDER_BY_FIELDS': ['organization_types', 'focus_sector', 'focus_industry', 'investment_stage_type'],
        'FILTERS': [
            {
                'api_url': '/api/v1/organization_type/',
                'label': _('Supporter Type'),
                'field_name': 'organization_types__permalink'
            },
            {
                'api_url': '/api/v1/type_of_focus_sector/',
                'label': _('Focus Sectors'),
                'field_name': 'focus_sector__permalink'
            },
            {
                'api_url': '/api/v1/type_of_focus_industry/',
                'label': _('Focus Industry'),
                'field_name': 'focus_industry__permalink'
            },
            {
                'api_url': '/api/v1/type_of_investment_stage/',
                'label': _('Stage'),
                'field_name': 'investment_stage_type__permalink'
            }
        ],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [
            {
                'label': _('Supporter Types'),
                'field_name': 'organization_types',
                'is_m2m': True
            },
            {
                'label': _('Focus Sectors'),
                'field_name': 'focus_sector',
                'is_m2m': True
            },
            {
                'label': _('Focus Industry'),
                'field_name': 'focus_industry',
                'is_m2m': True
            },
            {
                'label': _('Stage'),
                'field_name': 'program.investment_stage_type',
                'field_filter': 'investment_stage_type',
                # 'field_attribute': '.title',
                'is_m2m': True
            },
        ]
    },
    'people': {
        'TITLE': _('People'),
        'RESULT_TITLE': _('people'),
        'HEAD_TITLE': _('People'),

        'CREATE_URL': '',
        'CREATE_URL_PARAMS': (),

        'HEADER_BANNER': '/static/images/bg-people@2x.png',
        'PROMOTE_LIST': '',

        'API_URL': '/api/v1/user/search/',
        'HAPPENING_EXTRA_PARAMS': {
            'limit': 10,
            'offset': 0,
            'receiver_or_actor__is_user': 1
        },
        'EXTRA_PARAMS': {
            #'organization_roles': 'supporter',
            'limit': 10,
            'resource': 'PartyLiteResource',
            'none_to_all': 1,
            'has_relation': 1
        },
        'ORDER_BY_FIELDS': ['interests'],
        'FILTERS': [
            # {
            #     'api_url': '/api/v1/topic/?level=0',
            #     'label': _('Interests'),
            #     'field_name': 'interests__permalink'
            # },
            # {
            #     'api_url': '/api/v1/user_role/',
            #     'label': _('Role'),
            #     'field_name': 'user_roles__permalink'
            # }
        ],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [
            #
            # {
            #     'label': _('Interests'),
            #     'field_name': 'interests',
            #     'is_m2m': True
            # },
            # {
            #    'label': _('Suppor Stage'),
            #    'field_name': 'growth_stage'
            # },
            # {
            #     'label': _('Role'),
            #     'field_name': 'user_roles',
            #     'is_m2m': True
            # },
            {
                'label': '',
                'field_name': 'action'
            },
        ]
    },

    'job': {
        'TITLE': _('Job'),
        'RESULT_TITLE': _('jobs'),
        'HEAD_TITLE': _('Jobs'),

        'API_URL': '/api/v1/organization_jobs/search/',

        'EXTRA_PARAMS': {
            'limit': 10,
            'none_to_all': 1,
            'has_jobs': 1,
            # 'include_unpublished': 1
        },

        'ORDER_BY_FIELDS': [],

        'HAPPENING_EXTRA_PARAMS': {
        },

        'FILTERS': [
            {
                'api_url': '/api/v1/job_role/',
                'label': _('Role'),
                'field_name': 'jobs_job_primary_role__permalink',
                'multi_level': True
            },
            {
                'api_url': '/api/v1/location/',
                'label': _('Location'),
                'field_name': 'jobs_locations__permalink'
            },
            {
                'api_url': '/api/v1/job/schema/?route=fields.position.choices&dict_map=permalink,title',
                'route': 'fields.position.choices',
                'label': _('Job Type'),
                'field_name': 'jobs_position'
            },
            {
                'label': _('Compensation'),
                'field_name': 'Salary:jobs_money_salary_max_thb,jobs_money_salary_min_thb|Equity:jobs_equity_max,jobs_equity_min',
                'range': u'0-500000,1000,฿,|0-2,0.1,,%'
            },
            {
                'api_url': '/api/v1/job_tag/',
                'label': _('skill'),
                'field_name': 'jobs_skill_set',
                'autocomplete': True
            },
            {
                'query': True
            },
        ],
        'LIST_TEMPLATE': 'organization/job/_list.html',
        'COLUMNS': [
            # Not use
        ]
    },
    'job_applying': {
        'TITLE': _('Applying Jobs'),
        'RESULT_TITLE': _('applying jobs'),
        'HEAD_TITLE': _('Name'),

        'API_URL': '/api/v1/user_apply_job/',

        'EXTRA_PARAMS': {
            'limit': 10,
            'none_to_all': 1,
            'has_jobs': 1,
            'include_unpublished': 1
        },

        'ORDER_BY_FIELDS': [],

        'HAPPENING_EXTRA_PARAMS': {
        },

        'FILTERS': [],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [
            {
               'label': _('Apply to'),
               'field_name': 'job.title',
                'link': 'job.absolute_url'
            },
            {
                'label': _('Organization'),
                'field_name': 'dst.get_display_name',
                'link': 'dst.absolute_url'
            },
            {
                'label': _('On'),
                'field_name': 'created',
                'date_format': 'YYYY-MM-DD'
            },
            {
                'label': 'Detail',
                'field_name': 'Detail',
                'link': 'absolute_url'
            },
        ]
    }
}
