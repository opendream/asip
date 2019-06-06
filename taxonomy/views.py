from django.shortcuts import render, get_object_or_404
from taxonomy.models import OrganizationType


def organization_type_detail(request, permalink):
    instance = get_object_or_404(OrganizationType, permalink=permalink)

    return render(request, 'taxonomy/detail.html', {'instance': instance})