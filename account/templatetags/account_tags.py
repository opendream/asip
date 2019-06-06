from django import template
from account.functions import user_render_reference
from account.models import User

register = template.Library()

@register.filter(name='user_render_reference')
def do_user_render_reference(user_id, escape=False):

    user = User.objects.get(id=int(user_id))
    output = user_render_reference(user)

    if escape:
        output = output.replace("'", "\\'")

    return output