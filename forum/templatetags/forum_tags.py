from django import template

register = template.Library()


@register.filter
def can_edit(instance, user):

    if hasattr(instance, 'user_can_edit'):
        return instance.user_can_edit(user)

    return False


@register.filter
def can_create(model, user):

    if hasattr(model, 'user_can_create'):
        return model.user_can_add_children(user)

    return False


@register.filter
def order_by(queryset, field):
    return queryset.order_by(field)


@register.filter
def filter(queryset, field_value):
    field, value = field_value.split(',')
    return queryset.filter(**{field: value})


@register.filter
def get(queryset, field_value):
    field, value = field_value.split(',')
    return queryset.get(**{field: value})