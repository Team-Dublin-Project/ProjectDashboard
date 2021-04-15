from django import forms
from .models import UserFile

class FileForm(forms.ModelForm):
  files = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
          'multiple': True,
          'class': 'd-inline mt-3',
          'style': 'cursor: pointer;overflow: auto;'
          }
    ))

  class Meta:
    model = UserFile
    fields = ['files']