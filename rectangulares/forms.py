from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

class datos(forms.Form):
  a = forms.CharField(label="Introducr el valor de a", required=True)
  Xo = forms.CharField(label="Introduce el valor de Xo", required=True)
  C = forms.CharField(label="Introduce el valor de C", required=True)
  m = forms.CharField(label="Introduce el valot de m", required=True)

  def __init__(self, *args, **kwargs):
    super(datos, self).__init__(*args, **kwargs)  
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'