

PROMOTE_LIST_CONFIG = {
    'title': 'Meeting Interesting People',
    'api': {
        'data': '/api/v1/user/',
    }
}
TAB_LIST_CONFIG = [
    {
        'title': 'Interest',
        'api': {
            'options': '/api/v1/topic/',
            'data': '/api/v1/user/',
            'filter': 'interests',
        }
    },
    {
        'title': 'Country',
        'api': {
            'options': '/api/v1/country/',
            'data': '/api/v1/user/',
            'filter': 'country',
        }
    },
    {
        'title': 'Role',
        'api': {
            'options': '/api/v1/user_role/',
            'data': '/api/v1/user/',
            'filter': 'user_roles',
        }
    }
]


PROMOTE_LIST_ROLE_CONFIG = {}
TAB_LIST_ROLE_CONFIG = {}

PROMOTE_LIST_ROLE_CONFIG['social-enterprise'] = {
    'title': 'Meeting Interesting People',
    'api': {
        'data': '/api/v1/user/',
        'default_params': {'user_roles': 1}
    }
}
TAB_LIST_ROLE_CONFIG['social-enterprise'] = [
    {
        'title': 'Interest',
        'api': {
            'options': '/api/v1/topic/',
            'data': '/api/v1/user/',
            'filter': 'interests',
            'default_params': {'user_roles': 1}
        }
    },
    {
        'title': 'Country',
        'api': {
            'options': '/api/v1/country/',
            'data': '/api/v1/user/',
            'filter': 'country',
            'default_params': {'user_roles': 1}
        }
    },
]

PROMOTE_LIST_ROLE_CONFIG['supporter'] = {
    'title': 'Meeting Interesting People',
    'api': {
        'data': '/api/v1/user/',
        'default_params': {'user_roles': 2}
    }
}
TAB_LIST_ROLE_CONFIG['supporter'] = [
    {
        'title': 'Interest',
        'api': {
            'options': '/api/v1/topic/',
            'data': '/api/v1/user/',
            'filter': 'interests',
            'default_params': {'user_roles': 2}
        }
    },
    {
        'title': 'Country',
        'api': {
            'options': '/api/v1/country/',
            'data': '/api/v1/user/',
            'filter': 'country',
            'default_params': {'user_roles': 2}
        }
    },
]

PROMOTE_LIST_ROLE_CONFIG['investor'] = {
    'title': 'Meeting Interesting People',
    'api': {
        'data': '/api/v1/user/',
        'default_params': {'user_roles': 3}
    }
}
TAB_LIST_ROLE_CONFIG['investor'] = [
    {
        'title': 'Interest',
        'api': {
            'options': '/api/v1/topic/',
            'data': '/api/v1/user/',
            'filter': 'interests',
            'default_params': {'user_roles': 3}
        }
    },
    {
        'title': 'Country',
        'api': {
            'options': '/api/v1/country/',
            'data': '/api/v1/user/',
            'filter': 'country',
            'default_params': {'user_roles': 3}
        }
    },
]
