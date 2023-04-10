from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# class 쓰면 내부적으로 기능을 사용하고, 간단해지는게 장점
class PostList(ListView):  # 모델명_list.html 찾도록 강제로 세팅되어있음..따라서 index.html 를 post.html 로 바꾸거나 templates 이름을 변경하면됌
    model = Post
    ordering = '-pk'
    # template_name = 'blog/post_list.html'


# def index(request) :
#    posts = Post.objects.all().order_by('-pk')
#
#    return render(
#        request, 'blog/post_list.html',
#        {
#            'posts': posts,
#        }
#    )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    return render(
        request, 'blog/single_post_page.html',
        {
            'post': post,
        }
    )
