from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from polls.models import Poll, Question, QuestionVote, Choice


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = "__all__"


class QuestionVoteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = QuestionVote
        fields = ["id", "question", "text"]


class QuestionSerializer(serializers.ModelSerializer):
    questionvotes = QuestionVoteSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ["id", "text", "questionvotes", "question_type"]


class QuestionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = "__all__"
        depth = 2


class PollListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = "__all__"


class PollCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = "__all__"


class PollUpdateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Poll
        fields = "__all__"

    def update(self, instance, validated_data):
        qs = validated_data.pop("questions", [])
        date_start = validated_data.get('date_start', None)        
        if date_start is not None:
            if date_start != instance.date_start and instance.date_start is not None:
                raise serializers.ValidationError(_("Cannot change start date"))
        else:
            instance.date_start = date_start
        instance.name = validated_data.pop("name", instance.name)
        instance.text = validated_data.pop("text", instance.text)
        instance.is_active = validated_data.pop("is_active", instance.is_active)
        instance.save()
        return instance
