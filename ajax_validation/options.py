# -*- coding: utf-8 -*-
from django.conf.urls.defaults import url as django_url
from django.shortcuts import get_object_or_404

from django.core.exceptions import ImproperlyConfigured
from django.forms.models import modelform_factory
from ajax_validation.views import validate as validate_form



class ModelValidationView(object):
    model = None
    form_class = None
    save_if_valid = False


    def __init__(self, model=None, form_class=None, save_if_valid=False):
        self.model = model or self.__class__.model
        self.form_class = form_class or self.__class__.form_class
        self.save_if_valid = save_if_valid or self.__class__.save_if_valid


    def get_model(self):
        if not self.model:
            raise ImproperlyConfigured('`model` have to be setup on ModelValidationView instance')
        return self.model


    def get_form_class(self):
        model = self.get_model()
        if not self.form_class:
            self.form_class = modelform_factory(model)
        return self.form_class


    def _get_app_and_model_names(self):
        model = self.get_model()
        return {
            'app_name': model._meta.app_label.lower(),
            'model_name': model._meta.object_name.lower(),
            }


    def get_url_pattern(self, url_prefix=''):
        ctx = self._get_app_and_model_names()
        ctx.update(url_prefix=url_prefix)
        return r'^%(url_prefix)s%(app_name)s/%(model_name)s/(?P<object_pk>\d+)?$' % ctx


    def get_url_pattern_name(self):
        ctx = self._get_app_and_model_names()
        return 'validate-%(app_name)s-%(model_name)s' % ctx


    def get_url(self, url_prefix=''):
        return django_url(
            self.get_url_pattern(url_prefix=url_prefix),
            self.validate,
            name=self.get_url_pattern_name())
    url = property(lambda s: s.get_url())


    def get_instance(self, request, *args, **kwargs):
        object_pk = kwargs.get('object_pk', None)
        model = self.get_model()
        instance = model()
        if object_pk:
            instance = get_object_or_404(model, pk=object_pk)
        return instance


    def form_extra_kwargs(self, request, *args, **kwargs):
        instance = self.get_instance(request, *args, **kwargs)
        kwargs.update(instance=instance)
        kwargs.pop('object_pk', None)
        return kwargs


    def save(self, request, form):
        form.save()
        return {}


    def validate(self, request, *args, **kwargs):
        if 'callback' not in kwargs:
            kwargs.update(callback=self.form_extra_kwargs)

        if 'form_class' not in kwargs:
            form_class = self.get_form_class()
            if not form_class:
                raise ImproperlyConfigured('form_class param have to be provided.')
            kwargs.update(form_class=form_class)

        if 'save_if_valid' not in kwargs:
            kwargs.update(save_if_valid=self.save_if_valid,
                          save=self.save)

        return validate_form(request, *args, **kwargs)
