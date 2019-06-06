from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import FieldDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from common.decorators import statistic
from common.functions import get_success_message
from forum.forms import ForumForm, ForumBoardForm, ForumTopicForm, ForumPostForm, ForumReplyForm
from forum.models import Forum, ForumBoard, ForumTopic, ForumPost, ForumReply


def base_form(request, parent_pk=None, pk=None, form_class=None, success_detail_redirect=None, return_context=False):

    print form_class

    model_class = form_class._meta.model
    parent = None

    # Prepare parent and instance create or edit
    if pk:
        instance = get_object_or_404(model_class, pk=pk)

        if hasattr(instance, 'parent'):
            parent = instance.parent

    else:
        instance = model_class()

    if parent_pk:
        parent = get_object_or_404(instance.get_parent_model_class(), pk=parent_pk)


    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():

            instance = form.save(commit=False)

            try:
                instance_files = instance._meta.get_field('files')
                if instance_files:
                    instance_files.save_form_data(instance, form.cleaned_data['files'])
            except FieldDoesNotExist:
                pass

            instance.created_by = request.user

            if parent:
                instance.parent = parent

            instance.save()

            message_success = get_success_message(instance, not bool(pk))
            messages.success(request, message_success)

            if success_detail_redirect:
                return redirect(instance.get_absolute_url())

            return redirect(instance.get_edit_url())

    else:
        form = form_class(instance=instance)

    context = {'form': form, 'instance': instance, 'parent': parent}

    if return_context:
        return context

    return render(request, 'forum/form.html', context)

# Form
@staff_member_required
def forum_form(request, pk=None):
    return base_form(request, pk=pk, form_class=ForumForm)

@staff_member_required
def forum_board_form(request, parent_pk=None, pk=None):
    return base_form(request, parent_pk=parent_pk, pk=pk, form_class=ForumBoardForm)

@staff_member_required
def forum_topic_form(request, parent_pk=None, pk=None):
    return base_form(request, parent_pk=parent_pk, pk=pk, form_class=ForumTopicForm)

@login_required
def forum_post_form(request, parent_pk=None, pk=None):
    return base_form(request, parent_pk=parent_pk, pk=pk, form_class=ForumPostForm)

@login_required
def forum_reply_form(request, parent_pk=None, pk=None):
    return base_form(request, parent_pk=parent_pk, pk=pk, form_class=ForumReplyForm)


# Detail
def forum_detail(request, permalink):
    instance = get_object_or_404(Forum, permalink=permalink)
    return render(request, 'forum/forum_detail.html', {'instance': instance, 'child_model': ForumBoard})

@statistic
def forum_board_detail(request, permalink):
    instance = get_object_or_404(ForumBoard, permalink=permalink)
    return render(request, 'forum/forum_board_detail.html', {'instance': instance, 'child_model': ForumTopic})

@statistic
def forum_topic_detail(request, permalink):
    instance = get_object_or_404(ForumTopic, permalink=permalink)
    return render(request, 'forum/forum_topic_detail.html', {'instance': instance, 'child_model': ForumPost})

@statistic
def forum_post_detail(request, pk):
    instance = get_object_or_404(ForumPost, pk=pk)
    context = {'instance': instance, 'child_model': ForumReply}

    form_context_or_response = base_form(request,
        parent_pk=instance.pk,
        form_class=ForumReplyForm,
        success_detail_redirect=True,
        return_context=True
    )

    if type(form_context_or_response) is dict:
        for key, value in form_context_or_response.iteritems():
            context['reply_%s' % key] = value
    else:
        return form_context_or_response

    return render(request, 'forum/forum_post_detail.html', context)

def forum_reply_detail(request, pk):
    instance = get_object_or_404(ForumReply, pk=pk)
    return redirect(reverse('forum_post_detail', args=[instance.parent.pk]) + '##reply-%s' % instance.pk)





















