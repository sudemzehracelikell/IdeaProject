from rest_framework import serializers
from .models import Team, TeamMember

class TeamSerializer(serializers.ModelSerializer):
    teamMember = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=TeamMember.objects.all(),
        required=False
    )
    
    class Meta:
        model = Team
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'