from rest_framework import serializers

from contents.models import Content


class ContentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Content
        exclude = ['is_removed']

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method in ['PUT', 'PATCH']:
            if request.user != self.instance.author:
                raise serializers.ValidationError("Requested user is not the author of the content!")

        return super().validate(attrs)
