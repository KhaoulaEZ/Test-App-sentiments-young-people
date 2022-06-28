from django.shortcuts import render
from django.http import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from . import serializers
from .utils import *
from rest_pandas import PandasSimpleView
from django_pandas.io import read_frame
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics, filters
import spacy
from spacy import displacy
from spacy.matcher import Matcher 
from spacy.tokens import Span 

# Create your views here.

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {
            'Endpoint': 'entities/sentence/frame',
            'method': 'GET',
            'body': None,
            'description': 'Returns etities by key words  data frame'
        },
        {
            'Endpoint': 'entities-keywords/',
            'method': 'GET',
            'body': None,
            'description': 'Pivots etities by key words  '
        },
        {
            'Endpoint': 'all/sentiment-sentence/',
            'method': 'list',
            'body': None,
            'description': 'Fetch all sentance sentement in GenZ file (sentimentSentence Model) '
        },
        {
            'Endpoint': 'all/sentiment-young/',
            'method': 'list',
            'body': None,
            'description': 'Fetch all sentance sentement in Young Model '
        },
        
    ]
    return Response(routes)

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

# this fnct is for pagination in our Api
class ResultsSetPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            # can not set default = self.page
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })

class SentimentSentence(generics.ListAPIView):
    queryset = sentimentSentence.objects.all().order_by('id')
    search_fields = ['sentence_short', 'sentence_keywords', 'category']
    filter_backends = (filters.SearchFilter,)
    serializer_class = GenZSerializer
    pagination_class = ResultsSetPagination


class AllYoung(generics.ListAPIView):
    queryset = young.objects.all().order_by('id')
    search_fields = ['net_sent', 'logits']
    filter_backends = (filters.SearchFilter,)
    serializer_class = YoungSerializer
    pagination_class = ResultsSetPagination


class OrgEntities(generics.ListAPIView):
    queryset = sentimentSentence.objects.all().order_by('id')
    serializer_class = SentenceSentimentSerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        QueryOrg=sentimentSentence.objects.filter(sentence_entities__contains='ORG')
        source_org=[]
        target_org=[]
        for element in QueryOrg:
             #print(element.sentence_entities)
             List=list(element.sentence_entities.strip('][').split(', '))
             #print(List)
             for i in List:
                if i == 'Org':
                    #print(i)
                    source_org.append(i)
                else :
                    target_org.append(i)

            
        print("source",source_org)
        print("target",target_org)
        return QueryOrg

class AllSentenceEntities(generics.ListAPIView):
    queryset = sentimentSentence.objects.all().order_by('id')
    serializer_class = SentenceSentimentSerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        queryset = sentimentSentence.objects.exclude(sentence_entities=[])
        QueryOrg=sentimentSentence.objects.filter(sentence_entities__contains='ORG').values_list('sentence_entities')
        QueryMisc=sentimentSentence.objects.filter(sentence_entities__contains='Misc').values_list('sentence_entities')
        QueryPer=sentimentSentence.objects.filter(sentence_entities__contains='Per').values_list('sentence_entities')
        QueryPerson=sentimentSentence.objects.filter(sentence_entities__contains='Person').values_list('sentence_entities')
        QueryCardinal=sentimentSentence.objects.filter(sentence_entities__contains='Cardinal').values_list('sentence_entities')
        QueryOrdinal=sentimentSentence.objects.filter(sentence_entities__contains='Ordinal').values_list('sentence_entities')
        QueryDate=sentimentSentence.objects.filter(sentence_entities__contains='Date').values_list('sentence_entities')
        QueryNorp=sentimentSentence.objects.filter(sentence_entities__contains='NORP').values_list('sentence_entities')
        QueryGpe=sentimentSentence.objects.filter(sentence_entities__contains='GPE').values_list('sentence_entities')
        QueryMoney=sentimentSentence.objects.filter(sentence_entities__contains='MONEY').values_list('sentence_entities')
        QueryWork=sentimentSentence.objects.filter(sentence_entities__contains='WORK_OF_ART').values_list('sentence_entities')
        QueryLoc=sentimentSentence.objects.filter(sentence_entities__contains='LOC').values_list('sentence_entities')
        print('-------------')
        print('QueryOrg',QueryOrg)
        source_org=[]
        target_org=[]
        print('QueryWork',len(QueryWork))
        print('QueryLoc',len(QueryLoc))
        print('QueryDate',len(QueryDate))
        # for element in QueryMoney:
        #     print(element[0])
        #     List=list(element[0].strip('][').split(', '))
        #     print(List)
            #for i in List :
                    #print(i)
            
        print(source_org)
        print(target_org)
        return queryset

#class MyCustomPandasSerializer(PandasSerializer):
#    def transform_dataframe(self, dataframe):
#        dataframe.some_pivot_function(in_place=True)
#        return dataframe

#    pandas_serializer_class = MyCustomPandasSerializer


def transform_dataframe(self, dataframe):
    dataframe.some_pivot_function(in_place=True)
    return dataframe


class TimeSeriesView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return TimeSeries.objects.to_timeseries(
            index='date',
        )

@api_view(['GET'])
def EntitiesByKeywords(request):
    qs = sentimentSentence.objects.all()
    df = read_frame(qs, fieldnames=['sentence_keywords', 'category','sentence_entities'])
    return Response(df)

@api_view(['GET'])
def FramesentenceAndEntites(request):
    qs = sentimentSentence.objects.all()
    qs.to_dataframe(['sentence_keywords', 'sentence_entities'], index_col=['category'])
    return Response(qs)

@api_view(['GET'])
def sentenceAndEntites(request):
    qs = sentimentSentence.objects.all()
    df = read_frame(qs, fieldnames=['sentence_keywords', 'sentence_entities'])
    return Response(df)

@api_view(['GET'])
def PivotEntitiesByKeywords(request):
    qs = sentimentSentence.objects.all()
    rows = ['sentence_keywords']
    cols = ['sentence_entities']
    pt = qs.to_pivot_table(values='category', rows=rows, cols=cols)
    return Response(pt)

@api_view(['GET'])
def BuildGraph(request):
    category = sentimentSentence.objects.values_list('category')
    sentences = sentimentSentence.objects.values_list('sentence')
    #print(candidate_sentences['sentence'].sample(5))
    return Response(category)