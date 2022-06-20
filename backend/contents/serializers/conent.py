from rest_framework import serializers

from contents.models import Content


class ContentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Content
        exclude = ['is_removed']

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method in ['PUT', 'PATCH']:
            if request.user != self.instance.author:
                raise serializers.ValidationError("Requested user is not the author of the content!")

        return super().validate(attrs)

    def get_is_owner(self, instance):
        request = self.context.get('request')
        if request.user == instance.author:
            return True
        else:
            return False
