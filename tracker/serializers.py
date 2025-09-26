from rest_framework import serializers

from tracker.models import Project, Sprint, SprintStatusChoices, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, attrs):
        sprint = attrs.get("sprint")
        if sprint and sprint.status == SprintStatusChoices.COMPLETED:
            raise serializers.ValidationError(
                "Cannot add or move tasks to a closed sprint."
            )
        return super().validate(attrs)


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = "__all__"

    tasks = TaskSerializer(many=True, read_only=True)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
