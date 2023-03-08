from django.shortcuts import render
from .models import Member, Association, Membership, Account
from .serializers import MemberSerializer, AssociationSerializer
from rest_framework import generics


# Create your views here.
class MemberListView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
class MemberRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'slug'

class AssociationListView(generics.ListCreateAPIView):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer

class AssociationRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer
    lookup_field = 'slug'