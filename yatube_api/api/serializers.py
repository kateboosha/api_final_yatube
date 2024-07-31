from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "text",
            "pub_date",
            "author",
            "image",
            "group",
            "comments",
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            "id",
            "title",
            "slug",
            "description",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "post",
            "text",
            "created",
        )
        read_only_fields = ("post",)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = (
            "user",
            "following",
        )

    def validate_following(self, value):
        request = self.context.get("request")
        if request and request.user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на себя"
            )
        return value

    def validate(self, data):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Требуется ввести запрос.")
        if "following" not in data:
            raise serializers.ValidationError("Требуется имя пользователя")
        if Follow.objects.filter(
            user=request.user, following=data["following"]
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на пользователя"
            )
        return data
