from contents.models import Content


class ContentDataLayer:

    @classmethod
    def create_content(cls, **kwargs):
        return Content.objects.create(**kwargs)

    @classmethod
    def get_contents(cls, content_id=None):
        contents = Content.objects.filter(is_removed=False).select_related('author')
        return contents.get(id=content_id) if content_id else contents
