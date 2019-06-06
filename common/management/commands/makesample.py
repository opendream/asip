import random
from django.utils import timezone

from django.core.management import BaseCommand
from django.utils.text import slugify
import names
import loremipsum

from account.models import User
from cms.models import News, Event
from common.constants import STATUS_PUBLISHED, STATUS_CHOICES
from common.functions import instance_save_image_from_url
from organization.models import Organization, Job
from party.models import Party
from random import randint
from relation.models import *
from taxonomy.models import *
from party.models import Portfolio


class Command(BaseCommand):

    help = 'Make example data'

    user_role_list = []
    organization_role_list = []
    interest_list = []
    country_list = []
    type_of_need_list = []
    topic_list = []
    type_of_support_list = []
    user_list = []
    organization_list = []
    relation_list = []
    love_list = []
    portfolio_list = []
    news_list = []
    event_list = []
    job_list = []


    def handle(self, *args, **options):

        self.sample_taxonomy_organization_role()
        self.update_organization_role()
        #self.sample_taxonomy()
        #self.sample_people()
        #self.sample_organization(Organization.TYPE_SOCIAL_ENTERPRISE)
        #self.sample_organization(Organization.TYPE_SUPPORTING_ORGANIZATION)
        #self.sample_job()
        #self.sample_job_organization()

        [party.build_total() for party in Party.objects.all()]

        #self.sample_relation(Organization, User, OrganizationHasPeople)
        #self.sample_relation(Organization, Party, PartyPartnerParty)
        #self.sample_relation(Party, Organization, PartySupportParty)

        #self.sample_relation(Party, Party, PartyFollowParty)
        #self.sample_relation(Party, Party, PartyTestifyParty, True, True)
        #self.sample_relation(Party, Party, PartyContactParty)
        #self.sample_love()

        #self.sample_portfolio()
        #self.sample_portfolio_party()
        #self.sample_relation(User, Organization, UserExperienceOrganization, False, False, True, True)
        #self.sample_news()
        #self.sample_event()
        pass

    def sample_taxonomy(self):

        user_role_title_list = ['Social Entrepreneur', 'Supporting Organisation', 'Investor / Philanthropist']
        for title in user_role_title_list:
            permalink = slugify(unicode(title))
            user_role, created = UserRole.objects.get_or_create(permalink=permalink, defaults={
                'title': title,
                'permalink': permalink
            })
            self.user_role_list.append(user_role)


        interest_title_list = ['Nature', 'Creative', 'Technology', 'Observational', 'Health', 'Lifestyle']
        for title in interest_title_list:
            permalink = slugify(unicode(title))
            interest, created = Interest.objects.get_or_create(permalink=permalink, defaults={
                'title': title,
                'permalink': permalink
            })
            self.interest_list.append(interest)


        country_title_list = ['- Global -', 'Hong Kong', 'Indonesia', 'Japan', 'Korea', 'Thailand', 'Vietnam']

        for title in country_title_list:
            permalink = slugify(unicode(title))
            country, created = Country.objects.get_or_create(permalink=permalink, defaults={
                'title': title,
                'permalink': permalink
            })
            self.country_list.append(country)


        type_of_need_title_list = ['Grant / Donation', 'Loan', 'Equity', 'Strategic Planning', 'Financial Management',
                                   'PR', 'HR', 'Legal', 'Market Access', 'External Relations', 'Technical Expertise', 'Fundraising', 'Operational Management', 'Others']
        for title in type_of_need_title_list:
            permalink = slugify(unicode(title))
            need, created = TypeOfNeed.objects.get_or_create(permalink=permalink, defaults={
                'title': title,
                'permalink': permalink,
            })
            self.type_of_need_list.append(need)



        type_of_support_title_list = ['Grant / Donation', 'Investment', 'Incubation', 'Consulting Service', 'Others']
        for title in type_of_support_title_list:
            permalink = slugify(unicode(title))
            support, created = TypeOfSupport.objects.get_or_create(permalink=permalink, defaults={
                'title': title,
                'permalink': permalink,
            })
            self.type_of_support_list.append(support)

        topic_title_list = [
            ('Agriculture', [
                'Agricultural Equipment Provision',
                'Agriculture Inputs (Fertilizers, Seeds etc.)',
                'Agriculture Transportation/Distribution Services',
                'Agriculture Wholesale Services',
                'Crops',
                'Crops Processing',
                'Industrial Crops (Cotton, Jute, Biofuel etc.)'
            ]),
            ('Artisanal', [
                'Artisanal Goods Retail',
                'Artisanal Transportation/Distribution Services',
                'Artisanal Wholesale Services',
                'Artisanal Goods Production',
                'Artisanal Technical Assistance',
                'Other Artisanal'
            ]),
            ('Culture', [
                'Media',
                'Music',
                'Performing Arts',
                'Sports',
                'Cultural Technical Assistance',
                'Other Culture'
            ]),
            ('Creative Industry', [
            ]),
            ('Disability', [
            ]),
            ('Education', [
                'Co-Curricular/Extra Curricular Activities',
                'Educational Facilities',
                'Educational Materials/Equipment',
                'Educator Development/Training',
                'Early Childhood Academic Education',
                'Primary Academic Education',
                'Secondary Academic Education',
                'Post-school Education'
            ]),
            ('Energy', [
                'Biofuel/Biomass Production',
                'Energy Efficient Products (Stoves, Heaters, Cold Storage etc.)',
                'Energy Efficient Storage and Distribution Services',
                'Self-Powered Devices (Solar Lanterns, Windup Radios, etc)',
                'Renewable Energy Generation'
            ]),
            ('Environment', [
                'Biodiversity Monitoring Services',
                'Carbon Offset Products',
                'Environmentally-friendly Consumer Products',
                'Greenhouse Gas Reduction Services',
                'Land preservation/conservation',
                'Reforestation',
                'Waste Management and Recycling Services'
            ]),
            ('Food and Beverages', [
            ]),
            ('Financial Services', [
                'Business Financing (Large Enterprises, Corporate)',
                'Business Financing (SME)',
                'Agriculture Financing',
                'Microenterprise Financing',
                'Education Financing',
                'Household Needs/Consumption Financing',
                'Household Mortgage Financing',
                'Community Social Enterprise'
            ]),
            ('Health', [
                'Health Related Transportation Services (ambulance, etc.)',
                'Health Education Services',
                'Health Telecommunication Services (helplines, remote diagnostics, mobile health, etc.)',
                'Healthcare Products (eye glasses, bed nets, etc.)',
                'Hospitals'
            ]),
            ('Housing Development', [
                'Housing',
                'Green Building Housing'
            ]),
            ('Housing Technical Assistance', [
            ]),
            ('Information and Communication Technologies', [
                'Business Process Outsourcing',
                'Mobile Phone Financial Services',
                'Other Mobile Phone Services',
                'Mobile Phones',
                'Computer and Mobile Phone Applications/Software',
                'Computers and Laptops',
                'Technical Equipment',
                'Internet Access'
            ]),
            ('Infrastructure/Facilities Development', [
                'Building Materials',
                'Facilities/Infrastructure - New',
                'Green Building Facilities/Infrastructure - New',
                'Facilities/Infrastructure - Renovations/Improvements',
                'Green Building Facilities/Infrastructure - Renovations/Improvements',
                'Mass Transit'
            ]),
            ('Supply Chain Services', [
                'Retail Services',
                'Transportation/Distribution Services',
                'Wholesale Services',
                'Other Supply Chain Services'
            ]),
            ('Tourism', [
                'Properties',
                'Travel Packages',
                'Tourism Technical Assistance',
                'Other Tourism'
            ]),
            ('Water', [
                'Rainwater Harvesting and Water Recycling Services',
                'Sanitation Services',
                'Water Purification/Production Systems (Community Water Systems)',
                'Point of Use Water Purification Solutions',
                'Water Treatment (Community/Individual Sewage Systems)'
            ]),
            ('Others', [])
        ]

        for title, children_list in topic_title_list:
            permalink = slugify(unicode(title))
            topic, created = Topic.objects.get_or_create(permalink=permalink, defaults={
                'title': title,
                'permalink': permalink
            })
            for children in children_list:
                permalink_children = slugify(unicode(children))
                topic_children, created = Topic.objects.get_or_create(permalink=permalink_children, defaults={
                    'title': children,
                    'permalink': permalink_children,
                    'parent': topic
                })


            self.topic_list.append(topic)


    def sample_taxonomy_organization_role(self):

        organization_role_title_list = ['Social Enterprise', 'Supporter', 'Investor']
        for title in organization_role_title_list:
            permalink = slugify(unicode(title))
            organization_role, created = OrganizationRole.objects.get_or_create(permalink=permalink, defaults={
                'title': title,
                'permalink': permalink
            })
            self.organization_role_list.append(organization_role)


    def update_organization_role(self):

        for organization in Organization.objects.filter(type_of_organization='social-enterprise'):

            organization.organization_primary_role_id = 1
            organization.save()

            if organization.organization_roles.all().count() == 0:
                organization.organization_roles.add(self.organization_role_list[0])


        for organization in Organization.objects.filter(type_of_organization='supporter'):

            organization.organization_primary_role_id = 2
            organization.save()

            if organization.organization_roles.all().count() == 0:
                organization.organization_roles.add(self.organization_role_list[1], self.organization_role_list[2])


    def sample_people(self):

        # Generate 60 users with lorempixel
        for i in range(0, 60):
            user_role = random.choice(self.user_role_list)
            user, created = User.objects.get_or_create(email='user%s@example.com' % i, defaults={
                'email': 'user%s@example.com' % i,
                'priority': randint(0, 10),
                'username': 'username%s' % i,
                'first_name': names.get_first_name(),
                'last_name': names.get_last_name(),
                'occupation': ' '.join(loremipsum.get_sentence(False).split(' ')[0:3]),
                'summary': ' '.join(loremipsum.get_sentence(False).split(' ')[0:15]),
                'description': loremipsum.get_paragraph(),
                'facebook_url': 'https://www.facebook.com/username%s' %i,
                'twitter_url': 'https://www.twitter.com/username%s' %i,
                'linkedin_url': 'https://www.linkedin.com/username%s' %i,
                'homepage_url': 'https://www.homepage.com/username%s' %i,

            })

            if created:
                user.set_password('password')

                user.country = random.choice(self.country_list)

                user.user_roles.add(user_role)
                user.save()
                instance_save_image_from_url(user, 'http://lorempixel.com/430/320/people/', rand=True)
                print 'Generated user : %s (%s)' % (user.get_display_name(), user.email)

            self.user_list.append(user)


    def sample_organization(self, type_of_organization=Organization.TYPE_SOCIAL_ENTERPRISE):

        # Generate 30 se with lorempixel
        for i in range(0, 60):

            # randdom short or long name
            if random.randrange(0, 2):
                name = ''.join(loremipsum.get_sentence(False).split(' ')[0:random.randrange(2,5)])
            else:
                name = ' '.join(loremipsum.get_sentence(False).split(' ')[0:random.randrange(3, 10)])

            name = name.replace('.', '')

            permalink = 'example-%s-%s' % (type_of_organization, i)
            organization, created = Organization.objects.get_or_create(permalink=permalink, defaults={
                'type_of_organization': type_of_organization,
                'created_by': random.choice(self.user_list),
                'name': name,
                'summary': loremipsum.get_sentence(False),
                'description': ''.join(['<p>%s</p>' % loremipsum.get_paragraph(False) for ignore in range(0, random.randrange(0, 5))]),
                'facebook_url': 'https://www.facebook.com/%s/' % permalink,
                'twitter_url': 'https://www.twitter.com/%s/' % permalink,
                'linkedin_url': 'https://www.linkedin.com/%s/' % permalink,
                'homepage_url': 'https://www.homepage.com/%s/' % permalink,
                'status': STATUS_PUBLISHED
            })

            if created:

                random.shuffle(self.user_list)
                for user in self.user_list[0:random.randrange(0, 4)]:
                    organization.admins.add(user)

                organization.country = random.choice(self.country_list)

                random.shuffle(self.type_of_need_list)
                for type_of_need in self.type_of_need_list[0:random.randrange(0, 4)]:
                    organization.type_of_needs.add(type_of_need)

                random.shuffle(self.topic_list)
                for topic in self.topic_list[0:random.randrange(0, 4)]:
                    organization.topics.add(topic)

                random.shuffle(self.type_of_support_list)
                for type_of_support in self.type_of_support_list[0:random.randrange(0, 4)]:
                    organization.type_of_supports.add(type_of_support)

                instance_save_image_from_url(organization, 'http://lorempixel.com/430/320/abstract/', rand=True)

                print 'Generated %s : %s' % (organization.get_type_of_organization_display(), organization.name)

            self.organization_list.append(organization)


    def sample_relation(self, EntitySrcClass, EntityDstClass, RelationClass, is_point=False, is_data=False, is_title=False, is_description=False):

        entity_src_list = EntitySrcClass.objects.all()
        entity_dst_list = EntityDstClass.objects.all()

        # Loop from source
        sample_dst_list = []
        for i in range(15):
            sample_dst_list.append(0)

        index = 0
        for src in entity_src_list:
            for j in range(15):
                sample_dst_list[j] = entity_dst_list[index]
                if index == len(entity_dst_list)-1:
                    index = 0
                else:
                    index += 1
            #sample_dst_list = random.sample(entity_dst_list,5)
            for dst in sample_dst_list:
                default = {
                    'src_id': src.id,
                    'dst_id': dst.id,
                    'status': random.choice(STATUS_CHOICES)[0]
                }
                if is_point:
                    default['point'] = randint(0, 5)
                if is_data:
                    default['data'] = 'example ' + ' '.join([loremipsum.get_sentence(False) for ignore in range(random.randrange(1, 5))])
                else:
                    default['data'] = 'example'

                if is_title:
                    default['title'] = 'example  '.join(loremipsum.get_sentence(False).split(' ')[0:3])
                if is_description:
                    default['description'] = 'example  '.join([loremipsum.get_sentence(False) for i in range(random.randrange(1, 5))])

                if src.id != dst.id:
                    relation, created = RelationClass.objects.get_or_create(src_id=src.id, dst_id=dst.id, defaults=default)
                    if created:
                        print 'Generated: %s %s to %s' % (
                            src.get_display_name(), RelationClass.__name__.replace('Party', ''), dst.get_display_name())


    def sample_love(self):

        user_list = User.objects.all()
        organization_list = Organization.objects.all()


        # User love Organization
        for i, src in enumerate(list(user_list)):

            for dst in organization_list.filter(status=STATUS_PUBLISHED)[i+1:i+10]:
                love, created = PartyLove.objects.get_or_create(
                    src=src.party_ptr,
                    dst_content_type=ContentType.objects.get_for_model(Party),
                    dst_id=dst.id
                )
                if created:
                    print 'Generated : %s love %s' % (src.get_display_name(), dst.get_display_name())
                self.love_list.append(love)

        # Organization love User
        for i, src in enumerate(list(organization_list)):

            for dst in user_list.filter(is_active=True)[i+1:i+10]:

                love, created = PartyLove.objects.get_or_create(
                    src=src.party_ptr,
                    dst_content_type=ContentType.objects.get_for_model(Party),
                    dst_id=dst.id
                )

                if created:
                    print 'Generated : %s love %s' % (src.get_display_name(), dst.get_display_name())
                self.love_list.append(love)

        # User love User
        for i, src in enumerate(list(user_list)):
            for dst in user_list.filter(is_active=True)[i+1:i + 10]:
                love, created = PartyLove.objects.get_or_create(
                    src=src.party_ptr,
                    dst_content_type=ContentType.objects.get_for_model(Party),
                    dst_id=dst.id
                )
                if created:
                    print 'Generated : %s love %s' % (src.get_display_name(), dst.get_display_name())
                self.love_list.append(love)

        # Organization love Organization
        for i, src in enumerate(list(organization_list)):
            for dst in organization_list.filter(status=STATUS_PUBLISHED)[i+1:i + 10]:
                love, created = PartyLove.objects.get_or_create(
                    src=src.party_ptr,
                    dst_content_type=ContentType.objects.get_for_model(Party),
                    dst_id=dst.id
                )
                if created:
                    print 'Generated : %s love %s' % (src.get_display_name(), dst.get_display_name())
                self.love_list.append(love)



    def sample_portfolio(self):

        # Create portfolio
        for i in range(1, 500):
            default = {
                'title': ' '.join(loremipsum.get_sentence(False).split(' ')[0:3]),
                'description': loremipsum.get_paragraph(),
                'id': i,
                'url': 'http://portfolio%s.com' % i
            }
            portfolio, created = Portfolio.objects.get_or_create(id=i, defaults=default)
            if created:
                total_image = randint(2, 4)
                for j in range(total_image):
                     instance_save_image_from_url(portfolio, 'http://lorempixel.com/430/320/technics/', field_name='images', append=True,rand=True)
                     print 'Generated %s : %s' % ('portfolio', portfolio.title)
            self.portfolio_list.append(portfolio)

    def sample_portfolio_party(self):

        index = 0
        for org in self.organization_list:
            total_portfolio = 2
            for i in range(total_portfolio):
                if index < len(self.portfolio_list)-1:
                    portfolio = self.portfolio_list[index]
                    try:
                        org.portfolios.get(id=portfolio.id)
                    except:
                        org.portfolios.add(portfolio)
                        print 'add portfolio : %s to organization : %s' % (portfolio.title, org.name)

                index += 1

        for user in self.user_list:
            total_portfolio = 3
            for i in range(total_portfolio):
                if index < len(self.portfolio_list)-1:
                    portfolio = self.portfolio_list[index]
                    try:
                        user.portfolios.get(id=portfolio.id)
                    except:
                        user.portfolios.add(portfolio)
                        print 'add portfolio : %s to user : %s' % (portfolio.title, user.email)

                index += 1

    def sample_news(self):

        admin = User.objects.get(id=1)

        for i in range(20):
            permalink = 'example-news-%s' %i
            news, created = News.objects.get_or_create(permalink=permalink, defaults={
                'title': ' '.join(loremipsum.get_sentence(False).split(' ')[0:5]),
                'summary': ' '.join(loremipsum.get_sentence(False).split(' ')[0:15]),
                'description': loremipsum.get_paragraph(),
                'permalink': permalink,
                'status': STATUS_PUBLISHED,
                'created_by': admin,
                })

            if created:
                instance_save_image_from_url(news, 'http://lorempixel.com/430/320/nature/', rand=True)
                print 'Generated news: %s' % news.permalink

                random.shuffle(self.topic_list)
                for topic in self.topic_list[0:random.randrange(0, 4)]:
                    news.topics.add(topic)

            self.news_list.append(news)

    def sample_event(self):

        admin = User.objects.get(id=1)

        for i in range(20):
            permalink = 'example-event-%s' %i
            event, created = Event.objects.get_or_create(permalink=permalink, defaults={
                'title': ' '.join(loremipsum.get_sentence(False).split(' ')[0:5]),
                'summary': ' '.join(loremipsum.get_sentence(False).split(' ')[0:15]),
                'description': loremipsum.get_paragraph(),
                'permalink': permalink,
                'status': STATUS_PUBLISHED,
                'created_by': admin,
                'start_date': timezone.now(),
                'end_date': timezone.now(),
                'phone': '08123456789',
                'email': 'admin@admin.com',
                'facebook_url': 'http://facebook.com/%s' %permalink,
                'twitter_url': 'http://twitter.com/%s' %permalink,
                'homepage_url': 'http://homepage.com/%s' %permalink,
                'location': ' '.join(loremipsum.get_sentence(False).split(' ')[0:20]),
                })

            if created:
                instance_save_image_from_url(event, 'http://lorempixel.com/430/320/nature/', rand=True)
                print 'Generated event: %s' % event.permalink

                random.shuffle(self.topic_list)
                for topic in self.topic_list[0:random.randrange(0, 4)]:
                    event.topics.add(topic)

            self.event_list.append(event)

    def sample_job(self):

        # Create portfolio
        skills_list = ['Farmer', 'Carpenter', 'PHP', 'Javascript', 'Designer', 'Css']
        for i in range(1, 1000):
            title = 'job-example%s' % i
            default = {
                'title': title,
                'contact_information': loremipsum.get_paragraph(),
                'description': loremipsum.get_paragraph(),
                'role': random.choice(Job.ROLE_CHOICES)[0],
                'position': random.choice(Job.POSITION_CHOICES)[0],
                'salary_min': randint(500, 5000),
                'salary_max': randint(6000, 50000),
                'equity_min': randint(0, 100),
                'equity_max': randint(0, 100),
                'years_of_experience': randint(0, 10),
                'location': ' '.join(loremipsum.get_sentence(False).split(' ')[0:5]),
                'skills': random.choice(skills_list),
                'created': timezone.now(),
                'changed': timezone.now(),
                'status': STATUS_PUBLISHED,
            }
            job, created = Job.objects.get_or_create(title=title, defaults=default)
            if created:
                job.country = random.choice(self.country_list)
                job.save()

                print 'Generated %s : %s' % ('Job', job.title)
            self.job_list.append(job)

    def sample_job_organization(self):

        index = 0
        for org in self.organization_list:
            total_job = 5
            for i in range(total_job):
                if index < len(self.job_list)-1:
                    job = self.job_list[index]
                    try:
                        org.jobs.get(id=job.id)
                    except:
                        org.jobs.add(job)
                        print 'add job : %s to organization : %s' % (job.title, org.name)

                index += 1
