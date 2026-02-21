# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Course, Lesson, Question, Choice, Submission
from django.db.models import Avg, Count

# ... existing views ...

@login_required
def submit_exam(request, course_id):
    """
    View to handle exam submission
    """
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # Get all selected choices from the form
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('question_'):
                selected_choice_ids.append(int(value))
        
        # Create submission
        submission = Submission.objects.create(
            user=request.user,
            course=course
        )
        
        # Add selected choices to submission
        if selected_choice_ids:
            choices = Choice.objects.filter(id__in=selected_choice_ids)
            submission.choices.set(choices)
            
            # Calculate score
            submission.calculate_score()
        
        # Add success message
        messages.success(request, f'Your exam has been submitted successfully! Score: {submission.score}%')
        
        # Redirect to results page
        return redirect('show_exam_result', submission_id=submission.id)
    
    # GET request - display the exam form
    questions = course.questions.all().prefetch_related('choices')
    total_questions = questions.count()
    
    context = {
        'course': course,
        'questions': questions,
        'total_questions': total_questions,
    }
    return render(request, 'exam_form.html', context)

@login_required
def show_exam_result(request, submission_id):
    """
    View to display exam results
    """
    submission = get_object_or_404(Submission, id=submission_id, user=request.user)
    
    # Get all questions for this course
    questions = submission.course.questions.all().prefetch_related('choices')
    
    # Prepare detailed results
    results = []
    total_correct = 0
    
    for question in questions:
        # Get selected choice for this question
        selected_choice = submission.choices.filter(question=question).first()
        # Get correct choice for this question
        correct_choice = question.choices.filter(is_correct=True).first()
        
        is_correct = selected_choice and selected_choice.is_correct
        if is_correct:
            total_correct += 1
        
        results.append({
            'question': question,
            'selected_choice': selected_choice,
            'correct_choice': correct_choice,
            'is_correct': is_correct
        })
    
    # Determine if passed (70% or higher)
    passed = submission.score >= 70
    
    context = {
        'submission': submission,
        'results': results,
        'total_questions': questions.count(),
        'total_correct': total_correct,
        'passed': passed,
    }
    return render(request, 'exam_result.html', context)

# Additional helper views
def course_detail(request, course_id):
    """
    View to display course details with lessons and exam info
    """
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    
    context = {
        'course': course,
        'lessons': lessons,
        'total_questions': course.questions.count(),
    }
    return render(request, 'course_details_bootstrap.html', context)

def exam_form(request, course_id):
    """
    Display the exam form for a course
    """
    course = get_object_or_404(Course, id=course_id)
    questions = course.questions.all().prefetch_related('choices')
    
    context = {
        'course': course,
        'questions': questions,
    }
    return render(request, 'exam_form.html', context)