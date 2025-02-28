from django.contrib import admin
from .models import ReadingPassage, Question, QuestionOption, PracticeSession, UserAnswer

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3

@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_short', 'question_count')
    list_filter = ('is_short',)
    search_fields = ('title', 'content')
    inlines = [QuestionInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Number of Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'passage', 'question_type', 'text_preview')
    list_filter = ('question_type', 'passage')
    search_fields = ('text', 'correct_answer')
    inlines = [QuestionOptionInline]
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question Text'

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'answer', 'is_correct', 'marked_for_review')

@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'passage', 'start_time', 'end_time', 'score')
    list_filter = ('user', 'score')
    search_fields = ('user__username', 'passage__title')
    inlines = [UserAnswerInline]
    readonly_fields = ('user', 'passage', 'start_time', 'end_time', 'score')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'question', 'answer_preview', 'is_correct', 'marked_for_review')
    list_filter = ('is_correct', 'marked_for_review', 'session')
    search_fields = ('answer', 'question__text')
    
    def answer_preview(self, obj):
        return obj.answer[:30] + '...' if len(obj.answer) > 30 else obj.answer
    answer_preview.short_description = 'Answer'