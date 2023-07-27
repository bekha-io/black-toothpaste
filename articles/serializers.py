from rest_framework import serializers, fields, validators
from django.conf import settings

from .models import *


class PollShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'title', 'options')


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, required=False, slug_field="name",
                                        queryset=Tag.objects.filter())
    created_by = serializers.SlugRelatedField(read_only=True, slug_field="username")
    polls = PollShortInfoSerializer(many=True, read_only=True)
    
    def to_internal_value(self, data):
        """Creates related tags if do not exist"""
        for tag_name in data['tags']:
            Tag.objects.get_or_create(name=tag_name)
        return super().to_internal_value(data)
    
    class Meta:
        depth = 1
        model = Post
        fields = ["id", "article_title", "content", "created_by", "created_at", "tags", "polls"]
        read_only_fields = ["id", "created_by", "polls"]


class PollOptionsListField(serializers.ListSerializer):
    child = fields.CharField(min_length=1, max_length=255)


class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "text"]
        model = PollOption


class PollSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field="id", queryset=Post.objects.all())
    options = PollOptionSerializer(many=True)
    
    class Meta:
        model = Poll
        fields = ["id", "post", "options", "title"]
    
    def save(self, **kwargs):
        options = self.validated_data.pop('options')
        
        if len(options) > settings.APP_MAX_POLL_OPTIONS_AMOUNT:
            raise serializers.ValidationError('Options amount must be 4 or less')
        
        obj = super().save(**kwargs)
        for option in options:
            PollOption.objects.create(poll_id=obj.id, text=option['text'])
        return obj


class UserPollAnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPollAnswer
        fields = ["id", "user", "poll", "answer"]
        read_only_fields = ["user", ]
