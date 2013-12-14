from django import forms

from links.models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url', 'is_public', 'auto_update']


class LinkSearchForm(forms.Form):
    q = forms.CharField(max_length=1024, required=True,
                        label=u'Search', help_text=u'Search by URLs and title')
