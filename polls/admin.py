from django.contrib import admin
from polls.models import Poll, Question, QuestionVote, Choice


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(QuestionVote)
admin.site.register(Choice)
