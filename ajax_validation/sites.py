# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from django.db.models.base import ModelBase

from ajax_validation.options import ModelValidationView



class AlreadyRegistered(Exception):
    pass



class NotRegistered(Exception):
    pass



class ValidationSite(object):
    def __init__(self):
        self._registry = {}


    def register(self, model_or_iterable, validation_class=ModelValidationView):
        """
        Registers the given model(s) with the given validation class.

        The model(s) should be Model classes, not instances.

        If an validation class isn't given, it will use ModelValidation.

        If a model is already registered, this will raise AlreadyRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        options = {
            'model': validation_class.model,
            'form_class': validation_class.form_class,
            }

        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)

            options.update(model=model)
            self._registry[model] = validation_class(**options)


    def unregister(self, model_or_iterable):
        """
        Unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model]


    def get_urls(self, url_prefix=''):
        urlpatterns = patterns('')
        for model, modelvalidationview in self._registry.iteritems():
            urlpatterns += patterns('', modelvalidationview.get_url(url_prefix=url_prefix))
        return urlpatterns
    urls = property(lambda s: s.get_urls())



site = ValidationSite()
