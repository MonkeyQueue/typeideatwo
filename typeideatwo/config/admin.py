from django.contrib import admin
from .models import Link, SideBar
from typeideatwo.base_admin import BaseOwnerAdmin


@admin.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = (
        'title',
        'href',
        'status',
        'weight',
        'created_time'
    )
    fields = ('title', 'weight', 'href', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
