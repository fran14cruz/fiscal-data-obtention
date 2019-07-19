from django import forms
from receipts.models import Receipt

class ReceiptForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form=control',
            'placeholder': 'Type number...'
        }
    ))

    class Meta:
        model = Receipt
        fields = ('post',)