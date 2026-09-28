from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Semester, Course, Subject, SubjectLink


@login_required
def semester_list_view(request):
    semesters = Semester.objects.all()

    return render(
        request,
        'materials/semester_list.html',
        {'semesters': semesters}
    )


@login_required
def semester_detail_view(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)

    # Only Sem 3 has courses for now
    courses = None
    if semester.number == 3:
        courses = Course.objects.all()

    return render(
        request,
        'materials/semester_detail.html',
        {
            'semester': semester,
            'courses': courses,
        }
    )


@login_required
def course_detail_view(request, semester_id, course_id):
    semester = get_object_or_404(Semester, id=semester_id)
    course = get_object_or_404(Course, id=course_id)

    if not course.is_active:
        return render(
            request,
            'materials/coming_soon.html',
            {'title': f'{course.name} — {semester}'}
        )

    subjects = Subject.objects.filter(
        semester=semester,
        course=course
    )

    return render(
        request,
        'materials/course_detail.html',
        {
            'semester': semester,
            'course': course,
            'subjects': subjects,
        }
    )


@login_required
def subject_detail_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    # Build dict: { 'slides': link, 'lab': link, ... }
    links = {}
    for link in subject.links.all():
        links[link.category] = link

    return render(
        request,
        'materials/subject_detail.html',
        {
            'subject': subject,
            'links': links,
        }
    )


@login_required
def coming_soon_view(request):
    return render(
        request,
        'materials/coming_soon.html',
        {'title': 'Coming Soon'}
    )


@login_required
def slides_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    # Group slides by unit number (unit stored as category in SubjectLink)
    # For now, gather all 'slides' links for this subject
    units = {}
    for link in subject.links.filter(category='slides'):
        units[link.id] = link  # keyed by id until unit field is added
    return render(
        request,
        'materials/slides.html',
        {'subject': subject, 'units': units}
    )


@login_required
def download_view(request, link_id):
    """Redirect the user to the Google Drive link for a SubjectLink."""
    from django.shortcuts import redirect
    link = get_object_or_404(SubjectLink, id=link_id)
    return redirect(link.drive_link)