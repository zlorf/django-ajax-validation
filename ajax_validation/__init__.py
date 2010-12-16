# -*- coding: utf-8 -*-
from ajax_validation.views import ModelValidationView
from ajax_validation.sites import ValidationSite, site



# views can be situalted in views or ajax_validation files
# but user can change this
def autodiscover(app_files=('views', 'ajax_validation')):
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        for file_name in app_files:
            try:
                before_import_registry = copy.copy(site._registry)
                import_module('%s.%s' % (app, file_name))
            except:
                site._registry = before_import_registry
