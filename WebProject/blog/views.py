from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category
from django.core.exceptions import PermissionDenied

def crsf_failure(request, reason=""):
    return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    # template_name = post_form.html 자동으로 호출됨
    # default template_name => "post_form"
    template_name = "blog/post_update_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
# class 쓰면 내부적으로 기능을 사용하고, 간단해지는게 장점

class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):  # Form 을 지원
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user

            return super(PostCreate, self).form_valid(form)

        else:
            return redirect('/blog/')


class PostList(ListView):  # 모델명_list.html 찾도록 강제로 세팅되어있음..따라서 index.html 를 post.html 로 바꾸거나 templates 이름을 변경하면됌
    model = Post  # post_list 라는 변수로 자동으로 넘어감
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context  # -> post_blog.html {post_list, categories, no_category_post_count}
    # template_name = 'blog/post_list.html'

    # 추가 Category에 대한 context를 넘겨야함 detail page도 마찬가지


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context  # -> post_detail.html {post, categories, no_category_post_count}


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )
# def index(request) :
#    posts = Post.objects.all().order_by('-pk')  모든 Post를 가져옴 / 역순으로
#
#    return render(
#        request, 'blog/post_list.html',
#        {
#            'posts': posts,
#        }
#    )


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(
#         request, 'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )
