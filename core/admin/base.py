from django.contrib import admin

__author__ = 'sergio'
class LinkedInline(admin.options.InlineModelAdmin):
    template = "admin/edit_inline/linked.html"
    admin_model_path = None

    def __init__(self, *args):
        super(LinkedInline, self).__init__(*args)
        if self.admin_model_path is None:
            self.admin_model_path = self.model.__name__.lower()