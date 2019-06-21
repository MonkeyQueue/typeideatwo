from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from config.models import SideBar
from .models import Post, Category, Tag


class CommentViewMixin:
    # get_context_data 指获取需要传递到模板中的所有上下文
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommentViewMixin, ListView):
    queryset = Post.latest_posts()    # 设定基础数据集
    paginate_by = 5    # 设置每页展示的条数
    context_object_name = 'post_list'    # 如果不设置此项，在模板中需要使用object_list变量
    template_name = 'blog/list.html'    # 模板名称


class CategoryView(IndexView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id")
        # get_object_or_404指获取一个对象实例，若错误则抛出404错误
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return queryset.filter(tag__id=tag_id)


class PostDetailView(CommentViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword','')
            })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
        


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)





















