# coding=utf-8
"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'lmdb.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.Group(
            _(u"Реестр медицинских учреждений"),
            column=1,
            collapsible=False,
            css_classes=('grp-collapse',),
            children=[
                modules.ModelList(
                    u'Основные объекты',
                    collapsible=False,
                    column=1,
                    models=('core.models.LegalEntity', 'core.models.HealingObject', 'core.models.Service')
                ),
                modules.ModelList(
                    u'Справочники',
                    collapsible=True,
                    collapsed=True,
                    column=1,
                    css_classes=('opaque',),
                    models=('core.models.*', ),
                    exclude=('core.models.LegalEntity', 'core.models.HealingObject', 'core.models.Service')
                ),
            ]
        ))

        self.children.append(modules.Group(
            _(u"Администрирование"),
            column=1,
            collapsible=True,
            css_classes=('grp-collapse grp-closed',),
            children=[
                modules.ModelList(
                    u'Управление доступом',
                    collapsible=False,
                    column=1,
                    models=('django.contrib.*',),
                    exclude=('django.contrib.sites.*',)
                ),
                modules.ModelList(
                    u'Сайты',
                    collapsible=True,
                    collapsed=True,
                    column=1,
                    models=('django.contrib.*',),
                    exclude=('django.contrib.auth.*',)
                ),
            ]
        ))


