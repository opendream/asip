from django.core.urlresolvers import reverse
from account.functions import user_render_reference
from common.functions import instance_get_thumbnail, common_clean
from organization.functions import organization_render_reference
from django.utils.translation import ugettext_lazy as _


def party_render_reference(party, display_edit_link=False, field_name='admins'):

    try:
        return user_render_reference(party.user, display_edit_link, field_name)
    except:
        return organization_render_reference(party.organization, display_edit_link, field_name)


def portfolio_render_reference(portfolio, display_edit_link=True, field_name='portfolios'):

    html = '<span class="reference-span">%s</span>' % portfolio.title

    images = instance_get_thumbnail(portfolio, field_name='images', size='50x50')
    if images:

        html_images = ''
        for image in images[0:3]:
            html_images = html_images + ('<img class="reference-span" src="%s" />' % image)

        html = '%s %s' % (html_images, html)


    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (
            html, field_name, reverse('portfolio_edit', args=[portfolio.id]), _('edit'))

    html = '<span class="portfolio-reference-wrapper reference-wrapper">%s</span>' % html

    return common_clean(html)