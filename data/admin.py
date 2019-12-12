from django.contrib import admin
from .models import Data, Review, Image
from import_export.admin import ImportExportModelAdmin, ImportMixin
# Register your models here.

# @admin.register(Data)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    

class MyImportMixin(ImportMixin):
    from_encoding = 'utf-8'
        
class DataAdmin(ImportExportModelAdmin,MyImportMixin):
    pass

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    inlines = [
        ImageInline,
    ]


admin.site.register(Data, DataAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Image)