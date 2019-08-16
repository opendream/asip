# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards_func(apps, schema_editor):
    #JobRole = apps.get_model('taxonomy', 'JobRole')

    from taxonomy.models import JobRole

    roles = [
        ('developer', 'Software Engineer'),
        ('mobile-developer', '    Mobile Developer'),
        ('frontend-developer', '    Frontend Developer'),
        ('backend-developer', '    Backend Developer'),
        ('full-stack-developer', '    Full-Stack Developer'),
        ('engineering-manager', '    Engineering Manager'),
        ('qa-engineer', '    QA Engineer'),
        ('devops', '    DevOps'),
        ('software-architect', '    Software Architect'),
        ('designer', 'Designer'),
        ('ui-ux-designer', '    UI/UX Designer'),
        ('user-researcher', '    User Researcher'),
        ('visual-designer', '    Visual Designer'),
        ('creative-director', '    Creative Director'),
        ('operations', 'Operations'),
        ('finance', '    Finance/Accounting'),
        ('human-resources', '    H.R.'),
        ('office-manager', '    Office Manager'),
        ('recruiter', '    Recruiter'),
        ('customer-service', '    Customer Service'),
        ('operations-manager', '    Operations Manager'),
        ('sales', 'Sales'),
        ('business-development', '    Business Development'),
        ('manager-business-development', '    BD Manager'),
        ('account-manager', '    Account Manager'),
        ('sales-manager', '    Sales Manager'),
        ('marketing', 'Marketing'),
        ('growth-hacking', '    Growth Hacker'),
        ('marketing-manager', '    Marketing Manager'),
        ('content-creator', '    Content Creator'),
        ('management', 'Management'),
        ('ceo', '    CEO'),
        ('cfo', '    CFO'),
        ('cmo', '    CMO'),
        ('coo', '    COO'),
        ('cto', '    CTO'),
        ('engineer', 'Other Engineering'),
        ('hardware-engineer', '    Hardware Engineer'),
        ('mechanical-engineer', '    Mechanical Engineer'),
        ('systems-engineer', '    Systems Engineer'),
        ('other', 'Other'),
        ('attorney', '    Attorney'),
        ('business-analyst', '    Business Analyst'),
        ('data-scientist', '    Data Scientist'),
        ('product-manager', '    Product Manager'),
        ('project-manager', '    Project Manager'),
    ]

    parent = None

    for permalink, title in roles:
        if not title.startswith('    '):
            parent = None

        role, created = JobRole.objects.get_or_create(permalink=permalink, defaults={
            'permalink': permalink,
            'title': title.strip(),
            'parent': parent,
        })

        if not title.startswith('    ') and not parent:
            parent = role

    Location = apps.get_model('taxonomy', 'Location')

    provinces = [
        'Bangkok',
        'Chonburi',
        'Songkhla',
        'Khon Kaen',
        'Chiang Mai',
        'Nakhon Pathom',
        'Nonthaburi',
        'Pathum Thani',
        'Samut Prakan',
        'Samut Sakhon',
        'Nakhon Ratchasima',
        'Ubon Ratchathani',
        'Buriram',
        'Udon Thani',
        'Nakhon Si Thammarat',
        'Sisaket',
        'Surin',
        'Roi Et',
        'Chiang Rai',
        'Sakon Nakhon',
        'Chaiyaphum',
        'Nakhon Sawan',
        'Surat Thani',
        'Phetchabun',
        'Kalasin',
        'Maha Sarakham',
        'Phitsanulok',
        'Ratchaburi',
        'Suphan Buri',
        'Kanchanaburi',
        'Phra Nakhon Si Ayutthaya',
        'Narathiwat',
        'Lopburi',
        'Khelang Nakhon',
        'Kamphaeng Phet',
        'Nakhon Phanom',
        'Chachoengsao',
        'Pattani',
        'Rayong',
        'Trang',
        'Loei',
        'Saraburi',
        'Sukhothai',
        'Sa Kaeo',
        'Phichit',
        'Yasothon',
        'Tak',
        'Chanthaburi',
        'Prachuap Khiri Khan',
        'Phatthalung',
        'Nong Khai',
        'Yala',
        'Nong Bua Lam Phu',
        'Chumphon',
        'Phayao',
        'Prachinburi',
        'Nan',
        'Phetchaburi',
        'Uttaradit',
        'Krabi',
        'Phrae',
        'Bueng Kan',
        'Lamphun',
        'Phuket',
        'Non Nam Thaeng',
        'Mukdahan',
        'Chai Nat',
        'Uthai Thani',
        'Satun',
        'Ang Thong',
        'Phang Nga',
        'Nakhon Nayok',
        'Mae Hong Son',
        'Trat',
        'Sing Buri',
        'Samut Songkhram',
        'Ranong',
    ]

    for province in provinces:
        permalink = province.strip().replace(' ', '-').lower()
        Location.objects.get_or_create(permalink=permalink, defaults={
            'permalink': permalink,
            'title': province
        })


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0010_jobrole_location'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]