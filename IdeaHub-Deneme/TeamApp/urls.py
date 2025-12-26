from django.urls import path
from TeamApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('teams/', views.TeamList.as_view()),
    path('team/<int:pk>', views.TeamDetail.as_view()),
    path('teamMembers/', views.TeamMemberList.as_view()),
    path('teamMember/<int:pk>', views.TeamMemberDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)