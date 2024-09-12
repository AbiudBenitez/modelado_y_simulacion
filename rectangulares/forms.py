from typing import Any
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

class datos(forms.Form):
  a = forms.IntegerField(
    label="Introduce el valor de a",
    required=True
  )
  
  Xo = forms.IntegerField(
    label="Introduce el valor de Xo", 
    required=True
  )
  
  C = forms.IntegerField(
    label="Introduce el valor de C", 
    required=True
  )
  
  m = forms.IntegerField(
    label="Introduce el valor de m", 
    required=True
  )

  def __init__(self, *args, **kwargs):
    super(datos, self).__init__(*args, **kwargs)  
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'