from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from mocktests.models import Test_Attempt, Answer


@login_required
def index(request):
    completed_attempts = (
        Test_Attempt.objects
        .filter(user=request.user, completed_at__isnull=False)
        .select_related('test')
    )

    # --- Tests Attempted: unique tests (latest attempt per test counts once) ---
    seen_tests = set()
    for a in completed_attempts:
        seen_tests.add(a.test_id)

    tests_attempted = len(seen_tests)

    # --- Overall Accuracy: average of (score / total_marks) * 100 per test ---
    # One entry per test — the user's latest attempt on that test
    latest_per_test = {}
    for a in completed_attempts.order_by('-completed_at'):
        if a.test_id not in latest_per_test:
            latest_per_test[a.test_id] = a

    percentages = []
    for a in latest_per_test.values():
        total_marks = sum(q.marks for q in a.test.questions.all())
        if total_marks > 0:
            percentages.append((a.score / total_marks) * 100)

    overall_accuracy = 0
    if percentages:
        overall_accuracy = round(sum(percentages) / len(percentages), 1)

    return render(
        request,
        'home/home.html',
        {
            'tests_attempted': tests_attempted,
            'overall_accuracy': overall_accuracy,
        }
    )
def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')