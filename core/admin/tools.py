# coding=utf-8
__author__ = 'sergio'


class StatusAdminMixin(object):
    status_map = {
        'E': 'error',
        'W': 'wip',
        'OK': 'ok',
        'A': 'act'
    }

    def get_status_name(self, e):
        return "<span class='status %s'>%s</span>" % (self.status_map[e.status], e.get_status_display())

    get_status_name.admin_order_field = 'status'
    get_status_name.short_description = u'Состояние'
    get_status_name.allow_tags = True

    def mark_as_checked(self, request, queryset):
        for object in queryset:
            object.status = 'OK'
            object.save()

    mark_as_checked.short_description = u'Отметить как проверенные'

    actions = ['mark_as_checked']