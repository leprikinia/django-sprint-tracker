from django.contrib import admin

from tracker.models import Project, Sprint, Task


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


class SprintAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project", "start_date", "end_date", "status")
    list_filter = ("status", "project")
    search_fields = ("name",)
    ordering = ("-start_date",)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "project",
        "sprint",
        "assignee",
        "status",
        "priority",
        "created_at",
        "due_date",
    )
    list_filter = ("status", "priority", "project", "sprint")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Sprint, SprintAdmin)
admin.site.register(Task, TaskAdmin)
