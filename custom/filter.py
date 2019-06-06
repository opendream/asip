from django.utils.translation import ugettext_lazy as _

FILTER = {
    'startup': {
        'TITLE': _('Startup'),
        'RESULT_TITLE': _('companies'),
        'HEAD_TITLE': _('Company'),

        'CREATE_URL': '/organization/startup/create/',
        'CREATE_URL_PARAMS': (),

        'HEADER_BANNER': '/static/images/header-startup.jpg',
        'PROMOTE_LIST': '',

        'API_URL': '/api/v1/party/search/',
        'HAPPENING_EXTRA_PARAMS': {
            'limit': 10,
            'offset': 0,
            'receiver_or_actor__role_permalink': 'startup'
        },

        'EXTRA_PARAMS': {
            'organization_roles': 'startup',
            'limit': 10,
            'resource': 'PartyLiteResource',
            'none_to_all': 1
        },
        'ORDER_BY_FIELDS': ['topics'],
        'FILTERS': [
            {
                'api_url': '/api/v1/topic/?level=0',
                'label': _('Focus on'),
                'field_name': 'topics__permalink'
            },
            {
                'api_url': '/api/v1/type_of_need/',
                'label': _('Type of Need'),
                'field_name': 'type_of_needs__permalink'
            },
            {
                'api_url': '/api/v1/organization_product_launch/',
                'label': _('Product Launch'),
                'field_name': 'product_launch__permalink'
            },
            {
                'api_url': '/api/v1/organization_funding/',
                'label': _('Funded'),
                'field_name': 'funding__permalink'
            },
            {
                'api_url': '/api/v1/organization_funding/',
                'label': _('Request Funding'),
                'field_name': 'request_funding__permalink'
            }
        ],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [
            {
                'label': _('Focus on'),
                'field_name': 'topics',
                'is_m2m': True
            },
            {
                'label': _('Product Launch'),
                'field_name': 'product_launch'
            },
            {
                'label': _('Funded'),
                'field_name': 'funding'
            },
            {
                'label': _('Request Funding'),
                'field_name': 'request_funding'
            }
        ]
    },
    'investor': {
        'TITLE': _('Investor'),
        'RESULT_TITLE': _('investor'),
        'HEAD_TITLE': _('Investor'),

        'CREATE_URL': '/organization/supporter/create/',
        'CREATE_URL_PARAMS': (('organization_primary_role', 'investor'), ),

        'HEADER_BANNER': '/static/images/header-investor.jpg',
        'PROMOTE_LIST': '',

        'API_URL': '/api/v1/party/search/',
        'HAPPENING_EXTRA_PARAMS': {
            'limit': 10,
            'offset': 0,
            'receiver_or_actor__role_permalink': 'investor'
        },
        'EXTRA_PARAMS': {
            'roles': 'investor',
            'limit': 10,
            'resource': 'PartyLiteResource',
            'none_to_all': 1
        },
        'ORDER_BY_FIELDS': ['topics', 'investor_types'],
        'FILTERS': [
            {
                'api_url': '/api/v1/topic/?level=0',
                'label': _('Focus on'),
                'field_name': 'topics__permalink'
            },
            {
                'api_url': '/api/v1/type_of_support/',
                'label': _('Type of Investment'),
                'field_name': 'type_of_supports__permalink'
            },
            {
               'api_url': '/api/v1/organization_growth_stage/',
               'label': _('Investment Growth Stage'),
               'field_name': 'growth_stage__permalink'
            },
            {
               'api_url': '/api/v1/investor_type/',
               'label': _('Type'),
               'field_name': 'investor_types__permalink'
            }
        ],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [
            {
                'label': _('Focus on'),
                'field_name': 'topics',
                'is_m2m': True
            },
            {
               'label': _('Investment Stage'),
               'field_name': 'growth_stage',
                'is_m2m': True
            },
            {
               'label': _('Deal size'),
               'field_name': 'deal_size'
            }
        ]
    },
    'supporter': {
        'TITLE': _('Supporting Organization'),
        'RESULT_TITLE': _('organizations'),
        'HEAD_TITLE': _('Organization'),

        'CREATE_URL': '/organization/supporter/create/',
        'CREATE_URL_PARAMS': (('organization_primary_role', 'supporter'),),

        'HEADER_BANNER': '/static/images/header-supporter.jpg',
        'PROMOTE_LIST': '',

        'API_URL': '/api/v1/party/search/',
        'HAPPENING_EXTRA_PARAMS': {
            'limit': 10,
            'offset': 0,
            'receiver_or_actor__role_permalink': 'supporter'
        },
        'EXTRA_PARAMS': {
            'organization_roles': 'supporter',
            'limit': 10,
            'resource': 'PartyLiteResource',
            'none_to_all': 1
        },
        'ORDER_BY_FIELDS': ['topics', 'organization_types'],
        'FILTERS': [
            {
                'api_url': '/api/v1/topic/?level=0',
                'label': _('Focus on'),
                'field_name': 'topics__permalink'
            },
            {
                'api_url': '/api/v1/type_of_support/',
                'label': _('Type of Support'),
                'field_name': 'type_of_supports__permalink'
            },
            {
                'api_url': '/api/v1/organization_type/',
                'label': _('Type or Organization'),
                'field_name': 'organization_types__permalink'
            }
        ],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [

            {
                'label': _('Focus on'),
                'field_name': 'topics',
                'is_m2m': True
            },
            #{
            #    'label': _('Suppor Stage'),
            #    'field_name': 'growth_stage'
            #},
            {
                'label': _('Type'),
                'field_name': 'organization_types',
                'is_m2m':  True
            },
        ]
    },
    'people': {
        'TITLE': _('People'),
        'RESULT_TITLE': _('people'),
        'HEAD_TITLE': _('People'),

        'CREATE_URL': '',
        'CREATE_URL_PARAMS': (),

        'HEADER_BANNER': '',
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
            {
                'api_url': '/api/v1/topic/?level=0',
                'label': _('Interests'),
                'field_name': 'interests__permalink'
            },
            # {
            #     'api_url': '/api/v1/user_role/',
            #     'label': _('Role'),
            #     'field_name': 'user_roles__permalink'
            # }
        ],
        'LIST_TEMPLATE': 'party/_table.html',
        'COLUMNS': [

            {
                'label': _('Interests'),
                'field_name': 'interests',
                'is_m2m': True
            },
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
            'include_unpublished': 1
        },

        'ORDER_BY_FIELDS': [],

        'HAPPENING_EXTRA_PARAMS': {
        },

        'FILTERS': [
            {
                'query': True
            },
            {
                'api_url': '/api/v1/job_tag/',
                'label': _('skill'),
                'field_name': 'jobs_skill_set',
                'autocomplete': True
            },
            {
                'api_url': '/api/v1/job/schema/?route=fields.role.choices&dict_map=permalink,title',
                'route': 'fields.role.choices',
                'label': _('Job Role'),
                'field_name': 'jobs_role'
            },
            {
                'api_url': '/api/v1/job/schema/?route=fields.position.choices&dict_map=permalink,title',
                'route': 'fields.position.choices',
                'label': _('Working Pattern'),
                'field_name': 'jobs_position'
            }
        ],
        'LIST_TEMPLATE': 'organization/job/_list.html',
        'COLUMNS': [
            # Not use
        ]
    },
}