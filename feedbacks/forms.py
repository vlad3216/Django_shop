from django import forms

from feedbacks.models import Feedback
from shop1.utils import cleaner


class FeedbackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('text', 'user', 'rating')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user

    def clean_text(self):
        text = self.cleaned_data['text']
        return cleaner(text)
Footer
