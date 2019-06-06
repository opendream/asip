DEFAULT_POINT = {
    'name': 1,
    'image': 8,
    'summary': 1,
    'description': 1,
    'images': 5,


    'topics': 1,

    'facebook_url': 2,
    'twitter_url': 2,
    #'linkedin_url': 1,
    'homepage_url': 5,

    'name_of_representative': 2,
    'email_of_contact_person': 5,
    #'formset__phone_number': 5, # TODO: detect with formset
    'location_of_organizations_headquarters': 2,

    'peoples': 3,
    'partners': 3,
    'jobs': 3,
    'portfolios': 3
}

START_UP_POINT = {
    'product_launch': 1,
    'funding': 1,

    'type_of_needs': 1,

    'supporters': 3,
    'received_fundings': 3,

    'investors': 3,
    'received_investings': 3,
}

SUPPORTER_POINT = {
    'type_of_supports': 1,

    'recipients': 3,
    'gived_fundings': 3,
}

INVESTOR_POINT = {
    'growth_stage': 2,

    'type_of_supports': 1,

    'invest_recipients': 3,
    'gived_investings': 3,
}

POINT = {
    1: dict(DEFAULT_POINT.items() + START_UP_POINT.items()),
    2: dict(DEFAULT_POINT.items() + SUPPORTER_POINT.items()),
    3: dict(DEFAULT_POINT.items() + INVESTOR_POINT.items())
}