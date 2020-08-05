from django.db import models
from django.utils.translation import ugettext_lazy as _


class Poll(models.Model):

    name = models.CharField(_("Poll Name"), max_length=255)
    text = models.TextField(_("Poll description"))
    is_active = models.BooleanField(_("Is Active"), default=False)
    date_created = models.DateTimeField(_("Date created"), auto_now=True)
    date_changed = models.DateTimeField(
            _("Date changed"), auto_now=False, auto_now_add=True,
            blank=True, null=True
        )
    date_start = models.DateField(_("Date Start"), null=True, blank=True)

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")

    def __str__(self):
        return self.name


class Question(models.Model):

    TEXT = "Answer with text"
    SINGLE = "Single vote"
    MANY = "Many votes"

    VARIANTS = (
        ("TEXT", TEXT),
        ("SINGLE", SINGLE),
        ("MANY", MANY)
    )

    poll = models.ForeignKey(
            "polls.Poll", verbose_name=_("Poll"),
            on_delete=models.CASCADE, related_name="questions"
        )
    text = models.TextField(_("Text"), blank=True, null=True)
    question_type = models.CharField(
            _("Question Type"), max_length=10,
            choices=VARIANTS
        )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.text


class QuestionVote(models.Model):

    question = models.ForeignKey(
            "polls.Question", verbose_name=_("Question"),
            on_delete=models.CASCADE, related_name="questionvotes"
        )
    text = models.CharField(
            _("Question Vote Text"), max_length=255,
            blank=True, null=True
        )

    def __str__(self):
        return self.text


class Choice(models.Model):

    author = models.PositiveIntegerField(_("USER ID"), blank=True, null=True)
    questionvote = models.ForeignKey(
            "polls.QuestionVote", verbose_name=_("QuestionVote"),
            on_delete=models.CASCADE, related_name="choices",
            blank=True, null=True)
    vote = models.BooleanField(
            _("Vote"), default=False
        )
    answer_text = models.TextField(
            _("Question Text Answer"),
            blank=True, null=True
        )

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    def __str__(self):
        return f"{self.author}"
