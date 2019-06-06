from common.forms import CommonModelForm
from forum.models import Forum, ForumBoard, ForumTopic, ForumPost, ForumReply


class BaseForumForm(CommonModelForm):
    PERMALINK_FIELDS = ['permalink']


class ForumForm(BaseForumForm):
    class Meta:
        model = Forum
        fields = ['parent', 'title', 'permalink', 'description']

class ForumBoardForm(BaseForumForm):
    class Meta:
        model = ForumBoard
        fields = ['title', 'permalink', 'description', 'priority', 'children_ordering', 'css_class']

class ForumTopicForm(BaseForumForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'permalink', 'prefix', 'link', 'description']

class ForumPostForm(CommonModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'description', 'files']


class ForumReplyForm(CommonModelForm):
    class Meta:
        model = ForumReply
        fields = ['description', 'files']