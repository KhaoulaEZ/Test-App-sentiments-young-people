from django.contrib import admin
from .models import *
# Register your models here.
class sentiment(admin.ModelAdmin):
    list_display = ('sentence_short', 'sentence_keywords', 'category','sentence_entities','sentence_non_entities')
    search_fields = ['sentence_short', 'sentence_keywords', 'category','sentence_entities','sentence_non_entities']

class youngAdmin(admin.ModelAdmin):
    list_display = ('net_sent', 'logits')
    search_fields = ['net_sent', 'logits']

admin.site.register(sentimentSentence, sentiment)
admin.site.register(young, youngAdmin)