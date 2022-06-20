from django.db import transaction
from django.db.models import Prefetch

from backend.settings import CMS
from contents.models import Content, DynamicTextField


class ContentDataLayer:

    @classmethod
    def create_dynamic_text_field(cls, content, **kwargs):
        """
        Created number of a type of dynamic text field should not exceed
        the permitted number of that type of dynamic text field.
        """
        field_type = kwargs.get('type')
        created_count = content.dynamic_text_fields.filter(type=field_type, is_removed=False).count()
        permitted_count = CMS['DEFAULT_DYNAMIC_TEXT_FIELD_NUMBER'].get(field_type, 0)

        if created_count < permitted_count:
            return DynamicTextField.objects.create(content=content, **kwargs)
        else:
            raise ValueError(f"Can not insert {field_type} text field more!")

    @classmethod
    def update_dynamic_text_field(cls, field_id, **kwargs):
        DynamicTextField.objects.filter(id=field_id).update(**kwargs)

    @classmethod
    def get_dynamic_text_fields(cls, field_id=None):
        text_fields = DynamicTextField.objects.filter(is_removed=False)

        return text_fields.get(id=field_id) if field_id else text_fields

    @classmethod
    def create_content(cls, **kwargs):
        """
        Create a content with its fixed input field. If it consists of
        dynamic text field, then store it in respective table.
        """
        with transaction.atomic():
            dynamic_text_fields = kwargs.pop('dynamic_text_fields', [])
            content = Content.objects.create(**kwargs)
            for text_field in dynamic_text_fields:
                cls.create_dynamic_text_field(content, **text_field)

        return content

    @classmethod
    def get_contents(cls, content_id=None):
        contents = Content.objects.filter(is_removed=False).select_related('author').prefetch_related(
            Prefetch('dynamic_text_fields', queryset=DynamicTextField.objects.filter(is_removed=False))
        )

        return contents.get(id=content_id) if content_id else contents

    @classmethod
    def update_or_create_dynamic_text_fields(cls, content, dynamic_text_fields):
        """
        If dynamic text exists in the content, then update by its id.
        Otherwise, insert a new text field by relating to content.
        """
        with transaction.atomic():
            for text_field in dynamic_text_fields:
                field_id = text_field.pop('id', None)
                if field_id:
                    cls.update_dynamic_text_field(field_id, **text_field)
                else:
                    cls.create_dynamic_text_field(content, **text_field)
