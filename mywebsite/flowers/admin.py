from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Flower

# 註冊Category模型
admin.site.register(Category)

# 註冊Tag模型
admin.site.register(Tag)

# 自定義Flower模型的Admin界面
class FlowerAdmin(admin.ModelAdmin):
    # 在列表頁顯示的欄位
    list_display = ('title', 'category', 'price', 'slug')
    # 可以搜索的欄位
    search_fields = ('title', 'description')
    # 可以篩選的欄位
    list_filter = ('category', 'tags')
    # 在編輯頁顯示的欄位分組
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'slug')
        }),
        ('分類和標籤', {
            'fields': ('category', 'tags')
        }),
        ('圖片和價格', {
            'fields': ('image', 'price')
        }),
    )
    # 預填充字段，當輸入title時自動填充slug
    prepopulated_fields = {'slug': ('title',)}

# 使用自定義的FlowerAdmin註冊Flower模型
admin.site.register(Flower, FlowerAdmin)

