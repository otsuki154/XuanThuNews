from typing import Any
from django.forms.widgets import RadioSelect
from django.db import models

class CustomBooleanField(models.BooleanField):
    def formfield(self, **kwargs: Any) -> Any:
        kwargs['widget'] = RadioSelect(choices=((True,'Có'),(False,'Không')))
        kwargs['initial'] = False
        return super().formfield(**kwargs)