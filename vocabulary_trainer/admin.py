from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from .models import Vokabel, VokabelList, ListAccess
# Register your models here.

@register(VokabelList)
class VocabularyListAdmin(ModelAdmin):
    pass


@register(Vokabel)
class VocabularyAdmin(ModelAdmin):
    pass


@register(ListAccess)
class ListAccessAdmin(ModelAdmin):
    pass

