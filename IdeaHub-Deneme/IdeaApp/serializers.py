from rest_framework import serializers
from .models import Category, Idea, Media, Status, Tag
from .models import Update

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class UpdateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Update
        fields = ['id', 'user', 'update_text', 'created_at']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__' 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class IdeaSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Idea
        fields = '__all__' 

