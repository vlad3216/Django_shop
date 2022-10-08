from django.utils.safestring import mark_safe


class ImageMixins:
    base_fields = ('image_snapshot',)

    def get_readonly_fields(self, request, obj=None):
        if self.readonly_fields:
            return self.readonly_fields + self.base_fields
        else:
            return self.base_fields

    def get_list_display(self, request, obj=None):
        if self.list_display:
            return self.base_fields + self.list_display
        else:
            return self.base_fields

    def image_snapshot(self, instance):
        if instance.image and instance.image.url:
            return mark_safe(
                f'<img src="{instance.image.url}" width="64" height="64"/>'
                )
        return mark_safe('Image missing')