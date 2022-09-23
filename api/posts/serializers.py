from rest_framework import serializers

from domain.models import Post


class PostOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'created_at',
            'likes_counter'
        ]

    author = serializers.SerializerMethodField()
    likes_counter = serializers.SerializerMethodField()

    @classmethod
    def get_author(cls, obj: Post) -> dict:
        return {
            'author_id': obj.creator.id,
            'username': obj.creator.username
        }

    @classmethod
    def get_likes_counter(cls, obj: Post) -> int:
        return obj.likes.all().count()


class PostInputSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255, required=True, allow_blank=False, allow_null=False
    )
    content = serializers.CharField(max_length=1000, allow_blank=True, allow_null=False)


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255, required=False, allow_blank=False, allow_null=False
    )
    content = serializers.CharField(max_length=1000, allow_blank=True, allow_null=True)
