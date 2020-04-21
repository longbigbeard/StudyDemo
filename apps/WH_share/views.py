from django.shortcuts import render
from django.views import View
from .forms import PublicCommentForm
from .models import Comment
from django.conf import settings
from .serializer import CommentSerializer
import re
from apps.utils import restful


class ShareIndexView(View):
    def get(self, request):
        count = settings.ONE_PAGE_SCENE_COMMENT_COUNT
        comment = Comment.objects.select_related('author').all()[0:count]

        context = {
            "comments": comment,
        }

        return render(request, 'share-info/share-index.html', context=context)

    def post(self, request):
        form = PublicCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            content = re.sub(r'(<|&lt;)script.*script(>|&gt;)?', '', content)

            Comment.objects.create(content=content, author=request.user)
            return restful.ok()
        else:
            print("fail")
            return restful.params_error(message=form.get_errors())


def write_comment_view(request):
    page = int(request.GET.get('p', 1))
    start = (page - 1) * settings.ONE_PAGE_SCENE_COMMENT_COUNT
    ends = start + settings.ONE_PAGE_SCENE_COMMENT_COUNT

    comments = Comment.objects.select_related('author').all()[start:ends]
    serializer = CommentSerializer(comments, many=True)
    data = serializer.data

    return restful.result(data=data)
