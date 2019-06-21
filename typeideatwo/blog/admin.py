from django.contrib import admin
from .models import Post, Category, Tag
from typeideatwo.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry
from django.core.urlresolvers import reverse
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(
            CategoryAdmin, self
        ).save_model(
            request,
            obj,
            form,
            change
        )

    # 展示自定义字段，显示该类包含的文章数量
    def post_count(self, obj):
        # 使用逆向查询 obj.post_set 得到一个新的对象
        return obj.post_set.count()
    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(
    #         CategoryAdmin, self
    #     ).save_model(
    #         request, obj, form, change
    #     )

# 自定义过滤器，通过查看文档得到的这个方法，可以通用
# SimpleListFilter 提供的2个属性和2个方法供重写，title展示标题，
# parameter_name指查询时URL参数名字


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'Owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(
            owner=request.user
        ).values_list(
            'id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())  # self.value()得到的就是URL传递的参数
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'operator']
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    # search_fields作用是什么，category__name书上为什么用双下划线
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True

    fields = (
        ('category', 'title'),  # 外键字段
        'desc',
        'status',
        'content',
        'tag',
    )

    # 展示自定义字段，字段显示“操作”，内容显示“编辑”，作用是通过点击编辑进入文章编辑界面
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(
    #         CategoryAdmin,
    #         self
    #     ).save_model(
    #         request,
    #         obj,
    #         form,
    #         change
    #     )

    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id',
                    'action_flag', 'user',
                    'change_message']
