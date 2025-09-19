from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['teacher', 'rating', 'comments', 'is_anonymous']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = self.fields['teacher'].queryset.filter(is_active=True)
        self.fields['teacher'].label = 'Profesor'
        self.fields['rating'].label = 'Calificación'
        self.fields['comments'].label = 'Comentarios (opcional)'
        self.fields['is_anonymous'].label = 'Evaluación anónima'