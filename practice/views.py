from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import ReadingPassage, Question, PracticeSession, UserAnswer
import random
import datetime

def practice_landing(request):
    # Get the user's selected coach if authenticated
    if request.user.is_authenticated:
        selected_coach = request.user.profile.selected_coach
    else:
        selected_coach = None
    
    context = {
        'selected_coach': selected_coach,
    }
    
    return render(request, 'practice/landing.html', context)

@login_required
def start_practice(request, is_short=False):
    # Get a random passage based on the practice type
    passages = ReadingPassage.objects.filter(is_short=is_short)
    if not passages.exists():
        # Fallback to any passage if none match the criteria
        passages = ReadingPassage.objects.all()
    
    # Select a random passage
    passage = random.choice(passages)
    
    # Create a new practice session
    session = PracticeSession.objects.create(
        user=request.user,
        passage=passage
    )
    
    # Pre-create UserAnswer objects for each question
    for question in passage.questions.all():
        UserAnswer.objects.create(
            session=session,
            question=question,
            answer='',
            is_correct=None
        )
    
    return redirect('practice_test', session_id=session.id)

@login_required
def practice_test(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id, user=request.user)
    
    # If the session is already completed, redirect to the result
    if session.end_time:
        return redirect('practice_results', session_id=session.id)
    
    # Get the passage and all its questions
    passage = session.passage
    questions = passage.questions.all()
    user_answers = session.user_answers.all()
    
    # Prepare question data for the template
    for question in questions:
        # Make sure options are prefetched for each question
        if question.question_type == 'multiple_choice':
            question.option_list = question.options.all()  # Use a different name to avoid conflicts
    
    # Calculate remaining time (20 minutes from start time)
    start_time = session.start_time
    end_time = start_time + datetime.timedelta(minutes=20)
    remaining_seconds = max(0, (end_time - timezone.now()).total_seconds())
    
    context = {
        'session': session,
        'passage': passage,
        'questions': questions,
        'user_answers': {answer.question.id: answer for answer in user_answers},
        'remaining_seconds': int(remaining_seconds),
    }
    
    return render(request, 'practice/test.html', context)

@login_required
def save_answer(request, session_id, question_id):
    if request.method == 'POST':
        session = get_object_or_404(PracticeSession, id=session_id, user=request.user)
        question = get_object_or_404(Question, id=question_id)
        
        # Don't allow changes if the session is completed
        if session.end_time:
            return JsonResponse({'status': 'error', 'message': 'Session already completed'})
        
        # Get or create user answer
        user_answer, created = UserAnswer.objects.get_or_create(
            session=session,
            question=question,
            defaults={'answer': '', 'is_correct': None}
        )
        
        # Update the answer
        answer_text = request.POST.get('answer', '')
        mark_for_review = request.POST.get('mark_for_review') == 'true'
        
        user_answer.answer = answer_text
        user_answer.marked_for_review = mark_for_review
        user_answer.save()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def submit_test(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id, user=request.user)
    
    # Don't allow resubmission
    if session.end_time:
        return redirect('practice_results', session_id=session.id)
    
    # Mark the session as completed
    session.end_time = timezone.now()
    
    # Grade each answer
    correct_count = 0
    total_questions = 0
    
    for user_answer in session.user_answers.all():
        question = user_answer.question
        total_questions += 1
        
        # Check if the answer is correct
        if question.question_type == 'multiple_choice':
            correct_option = question.options.filter(is_correct=True).first()
            if correct_option and user_answer.answer == str(correct_option.id):
                user_answer.is_correct = True
                correct_count += 1
            else:
                user_answer.is_correct = False
        elif question.question_type == 'true_false':
            if user_answer.answer.lower() == question.correct_answer.lower():
                user_answer.is_correct = True
                correct_count += 1
            else:
                user_answer.is_correct = False
        else:  # fill_blank or short_answer
            # Simple exact match for now
            if user_answer.answer.lower() == question.correct_answer.lower():
                user_answer.is_correct = True
                correct_count += 1
            else:
                user_answer.is_correct = False
        
        user_answer.save()
    
    # Calculate score (on a scale of 9.0)
    if total_questions > 0:
        raw_score = (correct_count / total_questions) * 9.0
        session.score = round(raw_score, 1)
    else:
        session.score = 0.0
    
    session.save()
    
    # Update user profile statistics
    user_profile = request.user.profile
    user_profile.practice_count += 1
    
    # Update average IELTS score
    if user_profile.avg_ielts_score is not None:
        # Convert Decimal to float for calculation
        current_score = float(user_profile.avg_ielts_score)
        new_score = float(session.score)
        
        # Weighted average (30% new score, 70% old score)
        weighted_avg = round((0.7 * current_score) + (0.3 * new_score), 1)
        user_profile.avg_ielts_score = weighted_avg
    else:
        user_profile.avg_ielts_score = session.score
    
    user_profile.save()
    
    return redirect('practice_results', session_id=session.id)

@login_required
def practice_results(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id, user=request.user)
    
    # Ensure the session has been completed
    if not session.end_time:
        return redirect('practice_test', session_id=session.id)
    
    user_answers = session.user_answers.all()
    questions = [answer.question for answer in user_answers]
    
    context = {
        'session': session,
        'passage': session.passage,
        'user_answers': user_answers,
        'questions': questions,
        'score': session.score,
    }
    
    return render(request, 'practice/results.html', context)