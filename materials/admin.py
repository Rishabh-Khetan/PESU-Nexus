from django.contrib import admin
from .models import Semester, Course, Subject, SubjectLink


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'semester', 'course')
    list_filter = ('semester', 'course')
    search_fields = ('name', 'code')


@admin.register(SubjectLink)
class SubjectLinkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'category', 'drive_link')
    list_filter = ('category', 'subject__semester')
    search_fields = ('subject__name',)