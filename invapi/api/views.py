from django.shortcuts import render
from .models import Member, Association, Membership, Account
from .serializers import MemberSerializer, AssociationSerializer, MembershipSerializer, AccountSerializer
from rest_framework import generics


# Create your views here.
class MemberListView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
class MemberRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'slug'
    
class MemberDeleteView(generics.RetrieveDestroyAPIView):
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
    
class AssociationDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer
    lookup_field = 'slug'
    
class MembershipListView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    
class MembershipRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    lookup_field = 'slug'
    
class AccountListView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    