from django.db import models


class Semester(models.Model):
    number = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Semester {self.number}"


class Course(models.Model):
    """Branches like CSE/AIML, ECE."""
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to show 'Coming soon' for this course."
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Subject(models.Model):
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name


class SubjectLink(models.Model):
    CATEGORY_CHOICES = [
        ('slides', 'Slides'),
        ('lab', 'Lab'),
        ('extra', 'Extra'),
        ('papers', 'Papers'),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='links'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    drive_link = models.URLField()

    class Meta:
        unique_together = ('subject', 'category')
        ordering = ['category']

    def __str__(self):
        return f"{self.subject.name} — {self.get_category_display()}"