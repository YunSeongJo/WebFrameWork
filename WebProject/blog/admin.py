from django.contrib import admin
from .models import Post
from .models import Category

admin.site.register(Post)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)

# Register your models here.
