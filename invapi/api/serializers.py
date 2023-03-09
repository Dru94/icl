from rest_framework import serializers
from .models import Member, Association, Membership, Account
from django.utils.text import slugify
import random

class MemberSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['id', 'email', 'name', 'national_id', 
                  'contact', 'location', 'avatar', 'slug']
        
    def get_slug(self, obj):
        return slugify(obj.name)

class AssociationSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, required=True)
    slug = serializers.SerializerMethodField()
    
    class Meta:
        model = Association
        fields = ['id', 'title', 'tin_number', 'constitution', 
                  'contact', 'email', 'members', 'slug']

    def get_slug(self, obj):
        return slugify(obj.title)
    

class MembershipSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), required=True)
    association = serializers.PrimaryKeyRelatedField(queryset=Association.objects.all(), required=True)
    member_name = serializers.SerializerMethodField()
    association_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Membership
        fields = ['id', 'date_joined', 'slug', 'member', 'association', 'member_name', 
                  'association_title']
        read_only_fields = ('slug',)

    def get_member_name(self, obj):
        return obj.member.name
    
    def get_association_title(self, obj):
        return obj.association.title

    
class AccountSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    association = AssociationSerializer(required=True)
    
    class Meta:
        model = Account
        fields = ['id', 'bank_name', 'account_name', 'account_number', 
                  'association', 'slug']
        read_only_fields = ('slug',)
        
    def get_slug(self, obj):
        return slugify(obj.account_name)