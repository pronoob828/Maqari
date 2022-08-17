from django import forms
from maqari.models import Stats

class StatForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput)
    class Meta:
        model = Stats
        fields = ('account','halaqa','date','attendance','dars','dars_pages','taqdeer_dars','murajia','murajia_pages','taqdeer_murajia',)