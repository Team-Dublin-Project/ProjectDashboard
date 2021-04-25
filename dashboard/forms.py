from django import forms
from .models import UserFile

class FileForm(forms.ModelForm):
  file = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
          'class': 'd-inline mt-3',
          'style': 'cursor: pointer;overflow: auto;',
          'name': 'file',
          }
    ))

  class Meta:
    model = UserFile
    fields = ['file_name']