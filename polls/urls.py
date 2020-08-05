from rest_framework.routers import DefaultRouter
from polls.views import PollViewSet, ChoiceViewSet, Hello
from django.urls import path

router = DefaultRouter()
app_name = 'polls'

router.register(r'polls/choices/?', ChoiceViewSet)
router.register(r'polls/?', PollViewSet)

urlpatterns = [
    path('hello/', Hello.as_view()),
] + router.urls
