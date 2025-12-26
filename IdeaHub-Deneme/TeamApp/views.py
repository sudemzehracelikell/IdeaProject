from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamMemberSerializer
from django.http import Http404

class TeamList(APIView):

    def get(self, request, format= None):
        # Get user_id parameter for filtering
        user_id = request.GET.get('user_id', None)
        
        if user_id:
            # Filter teams where user is a member
            team_members = TeamMember.objects.filter(user__id=user_id)
            team_ids = [tm.id for tm in team_members]
            teams = Team.objects.filter(teamMember__id__in=team_ids).distinct()
        else:
            teams = Team.objects.all()
            
        serializer = TeamSerializer(teams, many = True)
        return Response(serializer.data)

    def post(self, request, format= None):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.save()
            
            # Automatically add creator as team member if creator_id is provided
            creator_id = request.data.get('creator_id')
            if creator_id:
                from UserApp.models import User
                try:
                    user = User.objects.get(id=creator_id)
                    # Create TeamMember
                    member = TeamMember.objects.create(user=user)
                    # Add to team's many-to-many field
                    team.teamMember.add(member)
                except Exception as e:
                    print(f"Error adding creator as member: {e}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamDetail(APIView):

    def getObject(self, pk):
        try:
            return Team.objects.get(pk = pk)
        except Team.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format= None):
        team = self.getObject(pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)
    
    def put(self, request, pk, format = None):
        team = self.getObject(pk)
        serializer = TeamSerializer(team, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        team = self.getObject(pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamMemberList(APIView):

    def get(self, request, format= None):
        teamMembers = TeamMember.objects.all()
        serializer = TeamMemberSerializer(teamMembers, many = True)
        return Response(serializer.data)

    def post(self, request, format= None):
        # Extract team_id before validation
        team_id = request.data.get('team')
        user_id = request.data.get('user')
        
        # Check if user is already a member of the team
        if team_id and user_id:
            try:
                team = Team.objects.get(id=team_id)
                if team.teamMember.filter(user__id=user_id).exists():
                    return Response({"error": "User is already a member of this team"}, status=status.HTTP_400_BAD_REQUEST)
            except Team.DoesNotExist:
                return Response({"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeamMemberSerializer(data = request.data)
        if serializer.is_valid():
            team_member = serializer.save()
            
            # Add to team if ID is provided
            if team_id:
                try:
                    team = Team.objects.get(id=team_id)
                    team.teamMember.add(team_member)
                except Team.DoesNotExist:
                    pass
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamMemberDetail(APIView):

    def getObject(self, pk):
        try:
            return TeamMember.objects.get(pk = pk)
        except TeamMember.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format= None):
        teamMember = self.getObject(pk)
        serializer = TeamMemberSerializer(teamMember)
        return Response(serializer.data)
    
    def put(self, request, pk, format = None):
        teamMember = self.getObject(pk)
        serializer = TeamMemberSerializer(teamMember, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        teamMember = self.getObject(pk)
        teamMember.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)