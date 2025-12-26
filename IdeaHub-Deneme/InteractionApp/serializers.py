from rest_framework import serializers
from .models import Comment
from .models import Vote

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # username gösterir

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'created_at']
