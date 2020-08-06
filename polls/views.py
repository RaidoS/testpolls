from rest_framework import permissions, mixins, viewsets, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from polls.serializers import PollSerializer, PollListSerializer, \
        PollUpdateSerializer, PollCreateSerializer, ChoiceSerializer
from polls.models import Poll, Choice
from polls.filters import ChoiceFilterBackend
from polls.permissions import PollsAdmin


class PollViewSet(
            mixins.RetrieveModelMixin,
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            mixins.UpdateModelMixin,
            viewsets.GenericViewSet
        ):
    """
    To get list of Polls http://127.0.0.1:8000/api/polls/
    detail Poll http://127.0.0.1:8000/api/polls/1/

    """

    serializer_classes = {
        'retrieve': PollSerializer,
        'list': PollListSerializer,
        'create': PollCreateSerializer,
        'update': PollUpdateSerializer,
        'partial_update': PollUpdateSerializer,
    }

    permissions_map = {
        'list': [],
        'retrieve': [],
        'create': [permissions.IsAuthenticated, PollsAdmin],
        'update': [permissions.IsAuthenticated, PollsAdmin],
        'partial_update': [permissions.IsAuthenticated, PollsAdmin],
    }

    permission_classes = [permissions.IsAuthenticated]
    queryset = Poll.objects.filter(is_active=True)
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        permissions_ = self.permissions_map.get(
                self.action,
                [permissions.IsAuthenticated]
            )
        return [permission() for permission in permissions_]

    def get_serializer_class(self):
        return self.serializer_classes.get(
                self.action,
                self.serializer_classes['list']
            )


class ChoiceViewSet(
            mixins.RetrieveModelMixin,
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            mixins.UpdateModelMixin,
            viewsets.GenericViewSet
        ):
    """
    Choices author filtering http://127.0.0.1:8000/api/polls/choices/?author=111

    add Choice:
    {
        "author": 111,
        "vote": true,
        "answer_text": "",
        "questionvote": 1
    }
    """

    serializer_classes = {
        'retrieve': ChoiceSerializer,
        'list': ChoiceSerializer,
        'create': ChoiceSerializer,
        'update': ChoiceSerializer,
        'partial_update': ChoiceSerializer,
    }
    filter_backends = [ChoiceFilterBackend]
    queryset = Choice.objects.all()

    def get_serializer_class(self):
        return self.serializer_classes.get(
                self.action,
                self.serializer_classes['list']
            )


class Hello(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return Response("Hi there")
