from rest_framework import serializers
from .models import Member, Association, Membership, Account
from django.utils.text import slugify


class MemberSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['email', 'name', 'national_id', 
                  'contact', 'location', 'avatar', 'slug']
        
    def get_slug(self, obj):
        return slugify(obj.name)

class AssociationSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, required=True)
    slug = serializers.SerializerMethodField()
    
    class Meta:
        model = Association
        fields = ['title', 'tin_number', 'constitution', 
                  'contact', 'email', 'members', 'slug']

    def get_slug(self, obj):
        return slugify(obj.title)
    
    