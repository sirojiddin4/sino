from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import ReadingPassage, Question, PracticeSession, UserAnswer, Test
import random
import datetime

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import ChatConversation, ChatMessage
import json

# Update the practice_landing view to include chat conversations
def practice_landing(request):
    # Get the user's selected coach if authenticated
    if request.user.is_authenticated:
        selected_coach = request.user.profile.selected_coach
        # Get user's chat conversations
        chat_conversations = ChatConversation.objects.filter(user=request.user)
    else:
        selected_coach = None
        chat_conversations = []
    
    context = {
        'selected_coach': selected_coach,
        'chat_conversations': chat_conversations,
    }
    
    return render(request, 'practice/landing.html', context)

@login_required
def start_practice(request, is_short=False):
    if is_short:
        # For short practice: select a single passage
        passages = ReadingPassage.objects.filter(is_short=is_short)
        if not passages.exists():
            # Fallback to any passage if none match the criteria
            passages = ReadingPassage.objects.all()
        
        # Select a random passage
        passage = random.choice(passages)
        
        # Create a new practice session for individual passage
        session = PracticeSession.objects.create(
            user=request.user,
            passage=passage,
            test=None,
            current_passage_number=1
        )
        
        # Pre-create UserAnswer objects for each question
        for question in passage.questions.all().order_by('order_number'):
            UserAnswer.objects.create(
                session=session,
                question=question,
                answer='',
                is_correct=None
            )
            
        return redirect('practice_passage', session_id=session.id)
    else:
        # For full practice: select a complete test with 3 passages
        tests = Test.objects.all()
        if not tests.exists():
            # If no tests exist, fallback to short practice
            return start_practice(request, is_short=True)
            
        test = random.choice(tests)
        
        # Get the first passage (passage_number=1)
        first_passage = test.passages.filter(passage_number=1).first()
        if not first_passage:
            # If test structure is incomplete, fallback to short practice
            return start_practice(request, is_short=True)
            
        # Create a new session for the full test
        session = PracticeSession.objects.create(
            user=request.user,
            passage=first_passage,
            test=test,
            current_passage_number=1
        )
        
        # Pre-create UserAnswer objects for ALL test questions
        for passage in test.passages.all():
            for question in passage.questions.all().order_by('order_number'):
                UserAnswer.objects.create(
                    session=session,
                    question=question,
                    answer='',
                    is_correct=None
                )
        
        return redirect('practice_test', session_id=session.id)

@login_required
def practice_test(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id, user=request.user, test__isnull=False)
    
    # If the session is already completed, redirect to the result
    if session.end_time:
        return redirect('practice_results', session_id=session.id)
    
    # Check if a specific passage is requested via query parameters
    requested_passage = request.GET.get('passage')
    if requested_passage and requested_passage.isdigit():
        requested_passage_number = int(requested_passage)
        # Find the requested passage
        requested_passage_obj = session.test.passages.filter(passage_number=requested_passage_number).first()
        if requested_passage_obj:
            # Update the current passage in the session
            session.passage = requested_passage_obj
            session.current_passage_number = requested_passage_number
            session.save()
    
    # Get all test passages
    test_passages = session.test.passages.all().order_by('passage_number')
    
    # Get the current passage
    current_passage = session.passage
    
    # Prepare all user answers for the complete test
    all_user_answers = session.user_answers.all()
    
    # Create a dictionary mapping question IDs to user answers for easy lookup
    user_answers_dict = {answer.question.id: answer for answer in all_user_answers}
    
    # Calculate remaining time (60 minutes for full test)
    start_time = session.start_time
    end_time = start_time + datetime.timedelta(minutes=60)
    remaining_seconds = max(0, (end_time - timezone.now()).total_seconds())
    
    context = {
        'session': session,
        'passage': current_passage,
        'test': session.test,
        'test_passages': test_passages,
        'current_passage_number': session.current_passage_number,
        'user_answers': user_answers_dict,
        'remaining_seconds': int(remaining_seconds),
        'has_next_passage': session.current_passage_number < test_passages.count(),
        'has_prev_passage': session.current_passage_number > 1,
    }
    
    return render(request, 'practice/test.html', context)

@login_required
def practice_passage(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id, user=request.user, test__isnull=True)
    
    # If the session is already completed, redirect to the result
    if session.end_time:
        return redirect('practice_results', session_id=session.id)
    
    # Get the passage and all its questions
    passage = session.passage
    questions = passage.questions.all().order_by('order_number')
    
    # Prepare user answers
    user_answers = session.user_answers.filter(question__passage=passage)
    
    # Prepare question data for the template
    for question in questions:
        # Attach user answers to questions
        try:
            question.user_answer = user_answers.get(question=question)
        except UserAnswer.DoesNotExist:
            question.user_answer = None
            
        # Make sure options are prefetched for each question
        if question.question_type == 'multiple_choice':
            question.option_list = question.options.all()
    
    # Calculate remaining time (20 minutes for individual passage)
    start_time = session.start_time
    end_time = start_time + datetime.timedelta(minutes=20)
    remaining_seconds = max(0, (end_time - timezone.now()).total_seconds())
    
    context = {
        'session': session,
        'passage': passage,
        'questions': questions,
        'remaining_seconds': int(remaining_seconds),
    }
    
    return render(request, 'practice/practice_passage.html', context)

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
def submit_passage(request, session_id):
    """Function to move to the next passage in a full test (not used in new approach)"""
    session = get_object_or_404(PracticeSession, id=session_id, user=request.user)
    
    # Only allow for full tests
    if not session.test:
        return redirect('practice_passage', session_id=session.id)
    
    # Find the next passage
    next_passage_number = session.current_passage_number + 1
    next_passage = session.test.passages.filter(passage_number=next_passage_number).first()
    
    if next_passage:
        # Update the session to the next passage
        session.passage = next_passage
        session.current_passage_number = next_passage_number
        session.save()
        
        return redirect('practice_test', session_id=session.id)
    else:
        # If no more passages, redirect to submit test
        return redirect('submit_test', session_id=session.id)

def grade_passage_answers(session, passage=None):
    """Helper function to grade all answers for a passage or the entire test"""
    # Get answers to grade - either for specific passage or all
    if passage:
        user_answers = session.user_answers.filter(question__passage=passage)
    else:
        user_answers = session.user_answers.all()
    
    for user_answer in user_answers:
        question = user_answer.question
        
        # Check if the answer is correct based on question type
        if question.question_type == 'multiple_choice':
            correct_option = question.options.filter(is_correct=True).first()
            if correct_option and user_answer.answer == str(correct_option.id):
                user_answer.is_correct = True
            else:
                user_answer.is_correct = False
        elif question.question_type in ['true_false', 'true_false_not_given']:
            if user_answer.answer.upper() == question.correct_answer.upper():
                user_answer.is_correct = True
            else:
                user_answer.is_correct = False
        else:  # fill_blank or short_answer
            # Simple exact match for now
            if user_answer.answer.lower() == question.correct_answer.lower():
                user_answer.is_correct = True
            else:
                user_answer.is_correct = False
        
        user_answer.save()

@login_required
def submit_test(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id, user=request.user)
    
    # Don't allow resubmission
    if session.end_time:
        return redirect('practice_results', session_id=session.id)
    
    # Grade all the answers
    grade_passage_answers(session)
    
    # Mark the session as completed
    session.end_time = timezone.now()
    
    # Calculate overall score
    correct_count = session.user_answers.filter(is_correct=True).count()
    total_questions = session.user_answers.count()
    
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
        if session.test:
            return redirect('practice_test', session_id=session.id)
        else:
            return redirect('practice_passage', session_id=session.id)
    
    # Get overall correct answers count
    correct_count = session.user_answers.filter(is_correct=True).count()
    total_questions = session.user_answers.count()
    
    # Basic context
    context = {
        'session': session,
        'correct_count': correct_count,
        'total_questions': total_questions,
        'score': session.score,
    }
    
    if session.test:
        # For full test results, organize data by passages
        passages_data = []
        
        for passage in session.test.passages.all().order_by('passage_number'):
            # Get answers for this passage
            passage_answers = session.user_answers.filter(question__passage=passage)
            passage_questions = Question.objects.filter(id__in=passage_answers.values_list('question', flat=True))
            
            # Calculate passage-specific score
            passage_correct = passage_answers.filter(is_correct=True).count()
            passage_total = passage_answers.count()
            passage_score = 0
            if passage_total > 0:
                passage_score = round((passage_correct / passage_total) * 9.0, 1)
            
            passages_data.append({
                'passage': passage,
                'answers': passage_answers,
                'questions': passage_questions,
                'correct_count': passage_correct,
                'total_count': passage_total,
                'score': passage_score
            })
        
        context.update({
            'is_full_test': True,
            'test': session.test,
            'passages_data': passages_data,
        })
    else:
        # For single passage results
        user_answers = session.user_answers.all()
        questions = [answer.question for answer in user_answers]
        
        context.update({
            'is_full_test': False,
            'passage': session.passage,
            'user_answers': user_answers,
            'questions': questions,
        })
    
    return render(request, 'practice/results.html', context)

# Chat-related views remain unchanged
@login_required
@require_POST
def create_chat_conversation(request):
    """Create a new chat conversation"""
    data = json.loads(request.body)
    first_message = data.get('first_message', '')
    
    # Use the first message as the title, truncate if necessary
    title = first_message[:100]
    
    # Check if a conversation with this title exists
    similar_titles = ChatConversation.objects.filter(user=request.user, title__startswith=title).count()
    
    if similar_titles > 0:
        # Append counter if similar title exists
        title = f"{title} ({similar_titles})"
    
    # Create the conversation
    conversation = ChatConversation.objects.create(
        user=request.user,
        title=title
    )
    
    # Add the first message
    ChatMessage.objects.create(
        conversation=conversation,
        sender='user',
        content=first_message
    )
    
    # Add initial coach message
    coach_response = get_coach_response(first_message)
    ChatMessage.objects.create(
        conversation=conversation,
        sender='coach',
        content=coach_response
    )
    
    return JsonResponse({
        'status': 'success',
        'conversation_id': conversation.id,
        'title': conversation.get_display_title(),
        'coach_response': coach_response
    })

@login_required
@require_POST
def add_chat_message(request, conversation_id):
    """Add a message to an existing conversation"""
    conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
    data = json.loads(request.body)
    message_content = data.get('message', '')
    
    # Add user message
    ChatMessage.objects.create(
        conversation=conversation,
        sender='user',
        content=message_content
    )
    
    # Add coach response
    coach_response = get_coach_response(message_content)
    ChatMessage.objects.create(
        conversation=conversation,
        sender='coach',
        content=coach_response
    )
    
    # Update the conversation timestamp
    conversation.save()  # This will update the 'updated_at' field
    
    return JsonResponse({
        'status': 'success',
        'coach_response': coach_response
    })

@login_required
def get_conversation(request, conversation_id):
    """Get all messages for a conversation"""
    conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
    messages = conversation.messages.all()
    
    messages_data = [{
        'sender': msg.sender,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for msg in messages]
    
    return JsonResponse({
        'status': 'success',
        'title': conversation.title,
        'messages': messages_data
    })

# Helper function to get coach responses
def get_coach_response(message):
    """Generate a coach response to a user message - currently returns a random response"""
    # In a real implementation, this could be connected to an AI model
    # For now, we'll use the same random responses as in the JS
    import random
    responses = [
        "The short practice takes about 10 minutes, while the full practice is 20 minutes.",
        "Focus on understanding the main ideas rather than every single word.",
        "Try to manage your time well. Spend about 2 minutes per question.",
        "Make sure to read the instructions for each question carefully.",
        "It's okay to mark questions for review and come back to them later."
    ]
    return random.choice(responses)

@login_required
@require_POST
def rename_conversation(request, conversation_id):
    """Rename a chat conversation"""
    conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        new_title = data.get('title', '').strip()
        
        if not new_title:
            return JsonResponse({
                'status': 'error',
                'message': 'Title cannot be empty'
            })
        
        # Update the conversation title
        conversation.title = new_title
        conversation.save()
        
        return JsonResponse({
            'status': 'success',
            'title': conversation.get_display_title()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
@require_POST
def delete_conversation(request, conversation_id):
    """Delete a chat conversation"""
    conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
    
    try:
        # Delete the conversation and all related messages
        conversation.delete()
        
        return JsonResponse({
            'status': 'success'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })