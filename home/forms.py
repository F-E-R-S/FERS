from django import forms
from .models import ReportBug

class ReportBug(forms.ModelForm):
        
    class Meta:
        model = ReportBug
        fields = ('title','bug','description')
    
