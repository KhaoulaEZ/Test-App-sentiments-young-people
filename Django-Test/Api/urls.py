from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('data/', TimeSeriesView.as_view()),
    path('entities/', EntitiesByKeywords),
    path('entities-keywords/', PivotEntitiesByKeywords),
    path('entities/sentence/frame', sentenceAndEntites),
    path('all/sentiment-sentence/', SentimentSentence.as_view(), name='sentiment-young'),
    path('all/sentiment-young/', AllYoung.as_view(), name='sentiment-young'),
    path('graph/', BuildGraph),
    path('all/sentence-entities', AllSentenceEntities.as_view(), name='All Sentence-Entities '),
    path('org/sentence-entities', OrgEntities.as_view(), name='Allorg  Sentence-Entities '),

]
