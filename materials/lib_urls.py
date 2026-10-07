from django.urls import path
from . import library

app_name = "library"

urlpatterns = [
    path("", library.home, name="home"),
    path("sem/<slug:slug>/", library.semester, name="semester"),
    path("browse/<path:subpath>", library.browse, name="browse"),
    path("file/<path:subpath>", library.serve_file, name="file"),
]
