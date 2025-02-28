from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Coach
from practice.models import PracticeSession

def homepage(request):
    # Get all coaches for the selection modal
    coaches = Coach.objects.all()
    default_coach = Coach.objects.filter(is_default=True).first() or coaches.first()
    
    # Set the selected coach for a logged-in user
    if request.user.is_authenticated:
        user_profile = request.user.profile
        selected_coach = user_profile.selected_coach or default_coach
    else:
        selected_coach = default_coach
    
    context = {
        'coaches': coaches,
        'selected_coach': selected_coach,
    }
    
    return render(request, 'core/homepage.html', context)

@login_required
def select_coach(request, coach_id):
    coach = Coach.objects.get(id=coach_id)
    request.user.profile.selected_coach = coach
    request.user.profile.save()
    return redirect('homepage')

def about(request):
    """View for the About page"""
    return render(request, 'core/about.html')

def support(request):
    """View for the Support page"""
    return render(request, 'core/support.html')