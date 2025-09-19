from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import Evaluation, Teacher
from .forms import EvaluationForm

@login_required
def submit_evaluation(request):
    if request.method == 'POST':
        form = EvaluationForm(request.POST, user=request.user)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.student = request.user
            evaluation.save()
            messages.success(request, '¡Gracias por tu evaluación!')
            return redirect('evaluation_thanks')
    else:
        form = EvaluationForm(user=request.user)
    
    return render(request, 'evaluations/submit_evaluation.html', {'form': form})

def evaluation_thanks(request):
    return render(request, 'evaluations/thanks.html')

class TeacherListView(ListView):
    model = Teacher
    template_name = 'evaluations/teacher_list.html'
    context_object_name = 'teachers'