# admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from .models import Course, Lesson, Question, Choice, Submission

# Register built-in models
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Session)
admin.site.register(LogEntry)
admin.site.register(ContentType)

# Inline classes for QuestionAdmin
class ChoiceInline(admin.TabularInline):
    """Inline for displaying choices within a question"""
    model = Choice
    extra = 2
    fields = ['choice_text', 'is_correct']
    classes = ['collapse']

class QuestionInline(admin.TabularInline):
    """Inline for displaying questions within a course"""
    model = Question
    extra = 1
    fields = ['question_text', 'order']
    show_change_link = True
    classes = ['collapse']

# Custom admin classes
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question model"""
    list_display = ['question_text', 'course', 'order', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['question_text']
    inlines = [ChoiceInline]
    fieldsets = (
        ('Question Information', {
            'fields': ('course', 'question_text', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

class LessonAdmin(admin.ModelAdmin):
    """Admin interface for Lesson model"""
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course']
    search_fields = ['title', 'content']
    fieldsets = (
        ('Lesson Information', {
            'fields': ('course', 'title', 'content', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']

# Register models with custom admin classes
admin.site.register(Question, QuestionAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Course)
admin.site.register(Submission)

# Customize admin site header and title
admin.site.site_header = 'Online Course Administration'
admin.site.site_title = 'Online Course Admin'
admin.site.index_title = 'Course Management Dashboard'