from django.urls import path
from .views import (MemberListView, AssociationListView, 
                    MemberRetrieveUpdateView, AssociationRetrieveUpdateView, 
                    MembershipListView, MembershipRetrieveUpdateView, 
                    MemberDeleteView, AssociationDeleteView, AccountListView)

urlpatterns = [
    path('api/members/', MemberListView.as_view(), name='all_members'),
    path('api/<slug:slug>/', MemberRetrieveUpdateView.as_view(), name="get_member"),
    path('api/remove/<slug:slug>/', MemberDeleteView.as_view(), name="del_member"),
    path('api/all/associations/', AssociationListView.as_view(), name="all_associations"),
    path('api/association/<slug:slug>/', AssociationRetrieveUpdateView.as_view(), name="get_association"),
    path('api/delete/<slug:slug>/', AssociationDeleteView.as_view(), name="del_association"),
    path('api/show/memberships/', MembershipListView.as_view(), name="all_memberships"),
    path('api/membership/<slug:slug>/', MembershipRetrieveUpdateView.as_view(), name="get_membership"),
    path('api/all/accounts/', AccountListView.as_view(), name="all_accounts"),
]
