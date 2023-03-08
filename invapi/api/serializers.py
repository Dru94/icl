from rest_framework import serializers
from .models import Member, Association, Membership, Account
from django.utils.text import slugify


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
    # member = MemberSerializer(required=True)
    # association = AssociationSerializer(required=True)
    slug = serializers.SerializerMethodField()
    
    class Meta:
        model = Membership
        fields = ['id','member', 'association', 'date_joined', 'slug']
        read_only_fields = ('slug',)
        
    def get_slug(self, obj):
        slug_field = f'{obj.member.name} {obj.association.title}'
        return slugify(slug_field)
    
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