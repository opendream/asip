from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def notification_list(request):
    return render(request, 'notification/list.html')

@login_required
def request_list(request):
    return render(request, 'notification/request/list.html')