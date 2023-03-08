from django.urls import path
from .views import (MemberListView, AssociationListView, 
                    MemberRetrieveUpdateView, AssociationRetrieveUpdateView)

urlpatterns = [
    path('api/members/', MemberListView.as_view(), name='all_members'),
    path('api/sign up/', MemberListView.as_view(), name="register_member"),
    path('api/<slug:slug>/', MemberRetrieveUpdateView.as_view(), name="get_member"),
    path('api/all/associations/', AssociationListView.as_view(), name="all_associations"),
    path('api/sign-up-association/', AssociationListView.as_view(), name="register_association"),
    path('api/association/<slug:slug>/', AssociationRetrieveUpdateView.as_view(), name="get_association")
]
