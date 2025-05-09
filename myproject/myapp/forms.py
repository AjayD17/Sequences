from django import forms

class SequenceForm(forms.Form):
    sequence = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter DNA, RNA, or Protein sequence...'}),
        label="Sequence Input",
        required=True
    )
