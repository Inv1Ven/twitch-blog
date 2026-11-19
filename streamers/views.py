from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from taggit.models import Tag  # <--- ВАЖНЫЙ ИМПОРТ ДЛЯ ТЕГОВ

from .models import Post, Comment
from .forms import CommentForm, EmailPostForm


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'streamers/post_list.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.published.all()
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = None
        if tag_slug:
            self.tag = get_object_or_404(Tag, name__iexact=tag_slug) # __iexact делает поиск нечувствительным к регистру
            queryset = queryset.filter(tags__in=[self.tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'streamers/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = self.object
            new_comment.save()
            return redirect(self.object.get_absolute_url())
        
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


# --- Лайки (AJAX) ---
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.likes += 1
    post.save(update_fields=['likes'])
    return JsonResponse({'likes': post.likes})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендует прочитать профиль {post.title}"
            message = f"Посмотри профиль стримера {post.title} на Twitch по ссылке: {post_url}\n\n{cd['name']} пишет: {cd['comments']}"
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'streamers/post_share.html', {
        'post': post,
        'form': form,
        'sent': sent,
    })