from django.contrib import admin
from .models import (
    ReadingPassage, Question, QuestionOption, PracticeSession, UserAnswer,
    QuestionType, QuestionGroup, Test
)

admin.site.register(QuestionOption)
admin.site.register(Test)

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3
    fields = ('text', 'correct_answer', 'question_group', 'order_number')

class QuestionGroupInline(admin.TabularInline):
    model = QuestionGroup
    extra = 1

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'frontend_type')
    search_fields = ('name', 'code', 'instructions')

@admin.register(QuestionGroup)
class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'passage', 'question_type', 'order')
    list_filter = ('question_type', 'passage')
    search_fields = ('title', 'specific_instructions')
    inlines = [QuestionInline]

@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_short', 'passage_number', 'test', 'question_count')
    list_filter = ('is_short', 'test', 'passage_number')
    search_fields = ('title', 'content')
    inlines = [QuestionGroupInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Number of Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'passage', 'get_question_type', 'text_preview', 'order_number')
    list_filter = ('question_group__question_type', 'passage', 'question_group')
    search_fields = ('text', 'correct_answer')
    inlines = [QuestionOptionInline]
    
    def get_question_type(self, obj):
        return obj.question_type.name
    get_question_type.short_description = 'Question Type'
    get_question_type.admin_order_field = 'question_group__question_type'
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question Text'

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'answer', 'is_correct', 'marked_for_review')

@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'passage', 'test', 'start_time', 'end_time', 'score')
    list_filter = ('user', 'passage', 'test', 'score')
    search_fields = ('user__username', 'passage__title', 'test__title')
    inlines = [UserAnswerInline]
    readonly_fields = ('user', 'passage', 'test', 'start_time', 'end_time', 'score')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'question', 'answer_preview', 'is_correct', 'marked_for_review')
    list_filter = ('is_correct', 'marked_for_review', 'session')
    search_fields = ('answer', 'question__text')
    
    def answer_preview(self, obj):
        return obj.answer[:30] + '...' if len(obj.answer) > 30 else obj.answer
    answer_preview.short_description = 'Answer'