from django import forms
from .models import ComHospital
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'placeholder' : '제목'
            }),
        required=True,
    )

    body = SummernoteTextField()

    field_order = [
        'title',
        'body'
    ]

    class Meta:
        model = ComHospital
        fields = ['title', 'body']
        widgets = {
            'body' : SummernoteWidget()
        }
    
    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title', '')
        body = cleaned_data.get('body', '')

        if title == '':
            self.add_error('title', '제목을 입력해 주세요.')
        elif body == '':
            self.add_error('body', '내용을 입력해 주세요.')
        else:
            self.title = title
            self.body = body

class SearchForm(forms.Form):
    check_values = forms.BooleanField(required=False)
