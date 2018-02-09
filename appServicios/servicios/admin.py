from django.contrib import admin
from django.db.models.base import ModelBase
from django.contrib.admin.sites import AlreadyRegistered
# Register your models here.
import servicios.models


for model_name in dir(servicios.models):
    model = getattr(servicios.models, model_name)
    if isinstance(model, ModelBase):
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            pass
