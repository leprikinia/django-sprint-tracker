from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SprintStatusChoices(models.IntegerChoices):
    PLANNED = 0, _("Planned")
    ACTIVE = 1, _("Active")
    COMPLETED = 2, _("Completed")


class TaskStatusChoices(models.IntegerChoices):
    TO_DO = 0, _("To Do")
    IN_PROGRESS = 1, _("In Progress")
    DONE = 2, _("Done")


class TaskPriorityChoices(models.IntegerChoices):
    LOW = 0, _("Low")
    MEDIUM = 1, _("Medium")
    HIGH = 2, _("High")
    HOTFIX = 3, _("Hotfix")


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project id:{self.pk} - {self.name}"


class Sprint(models.Model):
    project = models.ForeignKey(
        Project, related_name="sprints", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.IntegerField(
        choices=SprintStatusChoices.choices, default=SprintStatusChoices.PLANNED
    )

    def __str__(self):
        return f"Spring id:{self.pk} - {self.name}"


class Task(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="tasks",
        on_delete=models.CASCADE,
    )
    sprint = models.ForeignKey(
        Sprint,
        null=True,
        blank=True,
        related_name="tasks",
        on_delete=models.CASCADE,
    )
    assignee = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    status = models.IntegerField(
        choices=TaskStatusChoices.choices, default=TaskStatusChoices.TO_DO
    )
    priority = models.IntegerField(
        choices=TaskPriorityChoices.choices, default=TaskPriorityChoices.MEDIUM
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Task id:{self.pk} - {self.title}"
