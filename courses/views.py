from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Question, Choice, Submission

# الصفحة الرئيسية - عرض كل الكورسات
def home(request):
    courses = Course.objects.all()
    return render(request, 'courses/home.html', {'courses': courses})

# عرض تفاصيل الكورس (باستخدام Bootstrap template)
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    return render(request, 'courses/course_details_bootstrap.html', {
        'course': course,
        'lessons': lessons
    })

# عرض نموذج الامتحان (الأسئلة والاختيارات)
def exam_form(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = course.questions.all().prefetch_related('choices')
    return render(request, 'courses/exam_form.html', {
        'course': course,
        'questions': questions
    })

# تقديم الامتحان وحساب النتيجة
@login_required
def submit_exam(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        selected_choice_ids = []

        # جمع كل الإجابات المختارة من الفورم
        for key, value in request.POST.items():
            if key.startswith('question_'):
                selected_choice_ids.append(int(value))

        # إنشاء submission جديد
        submission = Submission.objects.create(
            user=request.user,
            course=course
        )

        # إضافة الـ choices المختارة للـ submission
        if selected_choice_ids:
            choices = Choice.objects.filter(id__in=selected_choice_ids)
            submission.choices.set(choices)

            # حساب النتيجة
            total_questions = course.questions.count()
            correct_count = choices.filter(is_correct=True).count()
            score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
            submission.score = score
            submission.save()

        messages.success(request, f'✅ Exam submitted! Your score: {submission.score:.1f}%')
        return redirect('show_exam_result', submission_id=submission.id)

    return redirect('exam_form', course_id=course_id)

# عرض نتيجة الامتحان مع تفاصيل الإجابات
@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, user=request.user)
    questions = submission.course.questions.all().prefetch_related('choices')

    results = []
    correct_count = 0

    for question in questions:
        selected_choice = submission.choices.filter(question=question).first()
        correct_choice = question.choices.filter(is_correct=True).first()
        is_correct = selected_choice and selected_choice.is_correct

        if is_correct:
            correct_count += 1

        results.append({
            'question': question,
            'selected_choice': selected_choice,
            'correct_choice': correct_choice,
            'is_correct': is_correct
        })

    passed = submission.score >= 70 if submission.score else False

    return render(request, 'courses/exam_result.html', {
        'submission': submission,
        'results': results,
        'total_questions': questions.count(),
        'correct_count': correct_count,
        'passed': passed
    })

# (اختياري) عرض تفاصيل الدرس - لو محتاجاها
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})