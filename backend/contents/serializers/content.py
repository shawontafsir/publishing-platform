from django.db import transaction
from django.db.models import QuerySet
from rest_framework import serializers, fields

from contents.datalayers.content import ContentDataLayer
from contents.models import Content, DynamicTextField


class DynamicTextFieldSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=False, required=False)

    class Meta:
        model = DynamicTextField
        exclude = ['content']


class ContentSerializer(serializers.ModelSerializer):
    dynamic_text_fields = DynamicTextFieldSerializer(many=True, required=False)
    author = serializers.StringRelatedField(read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = '__all__'

    def __init__(self, instance=None, data=fields.empty, **kwargs):
        """
        Do not need 'body' and 'dynamic_text_fields' in content list.
        """
        if isinstance(instance, QuerySet):
            if 'body' in self.fields:
                self.fields.pop('body')
            if 'dynamic_text_fields' in self.fields:
                self.fields.pop('dynamic_text_fields')

        super().__init__(instance, data, **kwargs)

    def validate(self, attrs):
        """
        Validate the author. If requested user is not the author,
        then he/she can not modify content.
        """
        request = self.context.get('request')
        if request.method in ['PUT', 'PATCH']:
            if request.user != self.instance.author:
                raise serializers.ValidationError("Requested user is not the author of the content!")

        return super().validate(attrs)

    def create(self, validated_data):
        """
        Override to customize the model data creation.
        Insert two model data entries for a request
        """
        try:
            return ContentDataLayer.create_content(**validated_data)
        except Exception as exc:
            raise ValueError(str(exc))

    def update(self, instance, validated_data):
        try:
            dynamic_text_fields = validated_data.pop('dynamic_text_fields', [])
            with transaction.atomic():
                ContentDataLayer.update_or_create_dynamic_text_fields(instance, dynamic_text_fields)
                return super().update(instance, validated_data)
        except Exception as exc:
            raise ValueError(str(exc))

    def get_is_owner(self, instance):
        """
        This returns a customized attribute value to find
        if requested user is the owner of the content or not.
        """
        request = self.context.get('request')
        if request.user == instance.author:
            return True
        else:
            return False
