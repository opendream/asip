from organization.models import Organization

PROMOTE_LIST_CONFIG = {}
TAB_LIST_CONFIG = {}

PROMOTE_LIST_CONFIG['social-enterprise'] = {
    'title': 'Featured Social Enterprise',
    'api': {
        'data': '/api/v1/organization/',
        'default_params': {'type_of_organization': Organization.TYPE_SOCIAL_ENTERPRISE, 'order_by_role': 'social-enterprise' }
    }
}
TAB_LIST_CONFIG['social-enterprise'] = [
    {
        'title': 'Issue',
        'api': {
            'options': '/api/v1/topic/?level=0',
            'data': '/api/v1/organization/',
            'filter': 'topics',
            'default_params': {'type_of_organization': Organization.TYPE_SOCIAL_ENTERPRISE}
        }
    },
    {
        'title': 'Country',
        'api': {
            'options': '/api/v1/country/',
            'data': '/api/v1/organization/',
            'filter': 'country',
            'default_params': {'type_of_organization': Organization.TYPE_SOCIAL_ENTERPRISE}
        }
    },
    {
        'title': 'Need',
        'api': {
            'options': '/api/v1/type_of_need/',
            'data': '/api/v1/organization/',
            'filter': 'type_of_needs',
            'default_params': {'type_of_organization': Organization.TYPE_SOCIAL_ENTERPRISE}
        }
    }
]

PROMOTE_LIST_CONFIG['startup'] = {
    'title': 'Featured Startup',
    'api': {
        'data': '/api/v1/organization/',
        'default_params': {'type_of_organization': Organization.TYPE_STARTUP, 'order_by_role': 'startup' }
    }
}
TAB_LIST_CONFIG['startup'] = [
    {
        'title': 'Issue',
        'api': {
            'options': '/api/v1/topic/?level=0',
            'data': '/api/v1/organization/',
            'filter': 'topics',
            'default_params': {'type_of_organization': Organization.TYPE_STARTUP}
        }
    },
    {
        'title': 'Country',
        'api': {
            'options': '/api/v1/country/',
            'data': '/api/v1/organization/',
            'filter': 'country',
            'default_params': {'type_of_organization': Organization.TYPE_STARTUP}
        }
    },
    {
        'title': 'Need',
        'api': {
            'options': '/api/v1/type_of_need/',
            'data': '/api/v1/organization/',
            'filter': 'type_of_needs',
            'default_params': {'type_of_organization': Organization.TYPE_STARTUP}
        }
    }
]

PROMOTE_LIST_CONFIG['supporter'] = {
    'title': 'Featured Supporters',
    'api': {
        'data': '/api/v1/organization/',
        'default_params': {'type_of_organization': Organization.TYPE_SUPPORTING_ORGANIZATION, 'order_by_role': 'supporter'}
    }
}
TAB_LIST_CONFIG['supporter'] = [
    {
        'title': 'Issue',
        'api': {
            'options': '/api/v1/topic/',
            'data': '/api/v1/organization/',
            'filter': 'topics',
            'default_params': {'type_of_organization': Organization.TYPE_SUPPORTING_ORGANIZATION}
        }
    },
    {
        'title': 'Country',
        'api': {
            'options': '/api/v1/country/',
            'data': '/api/v1/organization/',
            'filter': 'country',
            'default_params': {'type_of_organization': Organization.TYPE_SUPPORTING_ORGANIZATION}
        }
    },
    {
        'title': 'Support',
        'api': {
            'options': '/api/v1/type_of_support/?level=0&priority__lt=4',
            'data': '/api/v1/organization/',
            'filter': 'type_of_supports',
            'default_params': {'type_of_organization': Organization.TYPE_SUPPORTING_ORGANIZATION}
        }
    }
]

PROMOTE_LIST_CONFIG['investor'] = {
    'title': 'Featured Investor',
    'api': {
        'data': '/api/v1/organization/',
        'default_params': {'organization_roles__permalink': 'investor', 'order_by_role': 'investor'}
    }
}
TAB_LIST_CONFIG['investor'] = [
    {
        'title': 'Issue',
        'api': {
            'options': '/api/v1/topic/',
            'data': '/api/v1/organization/',
            'filter': 'topics',
            'default_params': {'organization_roles__permalink': 'investor', 'order_by_role': 'investor'}
        }
    },
    {
        'title': 'Country',
        'api': {
            'options': '/api/v1/country/',
            'data': '/api/v1/organization/',
            'filter': 'country',
            'default_params': {'organization_roles__permalink': 'investor', 'order_by_role': 'investor'}
        }
    },
    {
        'title': 'Invest',
        'api': {
            'options': '/api/v1/type_of_support/?level=0',
            'data': '/api/v1/organization/',
            'filter': 'type_of_supports',
            'default_params': {'organization_roles__permalink': 'investor', 'order_by_role': 'investor'}
        }
    }
]
