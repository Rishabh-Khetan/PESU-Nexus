import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.urls import reverse

BASE = Path(settings.BASE_DIR)
FY = "All subjects (both cycles)"
ALLOWED = {FY, "Sem 3"}   # top-level folders the site may serve

GROUPS = [
    {
        "title": "1st Year Materials",
        "direct": False,
        "sections": [
            {"slug": "chemistry-cycle", "title": "Chemistry Cycle",
             "parent": f"{FY}/CHEMISTRY CYCLE", "extra": []},
            {"slug": "physics-cycle", "title": "Physics Cycle",
             "parent": f"{FY}/PHYSICS CYCLE", "extra": []},
            {"slug": "common", "title": "Common Subjects", "parent": None,
             "extra": [f"{FY}/Engineering Mathematics - II",
                       f"{FY}/Problem Solving with C"]},
        ],
    },
    {
        "title": "Sem 3 Materials",
        "direct": True,   # each subject gets its own card on the home page
        "sections": [
            {"slug": "sem3", "title": "Semester 3", "parent": "Sem 3", "extra": []},
        ],
    },
]

SEMESTERS = [s for g in GROUPS for s in g["sections"]]
DIRECT = {s["slug"] for g in GROUPS if g["direct"] for s in g["sections"]}


def _safe(sub):
    base = BASE.resolve()
    target = (BASE / sub).resolve()
    if base not in target.parents:
        raise Http404("Not found")
    if target.relative_to(base).parts[0] not in ALLOWED:
        raise Http404("Not found")
    return target


def _subjects(sem):
    rels = []
    if sem["parent"]:
        base = _safe(sem["parent"])
        if base.is_dir():
            rels += [
                f"{sem['parent']}/{d.name}"
                for d in sorted(base.iterdir(), key=lambda p: p.name.lower())
                if d.is_dir()
            ]
    rels += [r for r in sem["extra"] if _safe(r).is_dir()]
    return rels


def _subject_to_sem():
    return {rel: s["slug"] for s in SEMESTERS for rel in _subjects(s)}


def _size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def _count_files(rel):
    return sum(1 for p in _safe(rel).rglob("*") if p.is_file())


def home(request):
    groups = []
    for g in GROUPS:
        cards = []
        for s in g["sections"]:
            rels = _subjects(s)
            if g["direct"]:
                for rel in rels:
                    path = _safe(rel)
                    subs = [d.name for d in sorted(path.iterdir(), key=lambda p: p.name.lower())
                            if d.is_dir()][:4]
                    n = _count_files(rel)
                    cards.append({
                        "title": rel.split("/")[-1],
                        "meta": f"{n} file{'s' if n != 1 else ''}",
                        "items": subs,
                        "url": reverse("library:browse", args=[rel]),
                    })
            else:
                n = len(rels)
                cards.append({
                    "title": s["title"],
                    "meta": f"{n} subject{'s' if n != 1 else ''}",
                    "items": [r.split("/")[-1] for r in rels],
                    "url": reverse("library:semester", args=[s["slug"]]),
                })
        groups.append({"title": g["title"], "cards": cards})
    return render(request, "materials/lib_home.html", {"groups": groups})


def semester(request, slug):
    sem = next((s for s in SEMESTERS if s["slug"] == slug), None)
    if not sem:
        raise Http404("Unknown semester")
    folders = [
        {"name": r.split("/")[-1], "url": reverse("library:browse", args=[r])}
        for r in _subjects(sem)
    ]
    return render(request, "materials/lib_browse.html", {
        "title": sem["title"],
        "crumb": "Study Materials",
        "folders": folders,
        "files": [],
        "back_url": reverse("library:home"),
        "back_label": "Back to Semesters",
    })


def browse(request, subpath):
    target = _safe(subpath)
    if not target.is_dir():
        raise Http404("Not a folder")
    rel = target.relative_to(BASE.resolve()).as_posix()

    folders, files = [], []
    for item in sorted(target.iterdir(), key=lambda p: p.name.lower()):
        child = f"{rel}/{item.name}"
        if item.is_dir():
            folders.append({"name": item.name, "url": reverse("library:browse", args=[child])})
        else:
            files.append({
                "name": item.name,
                "ext": item.suffix.lstrip(".").upper() or "FILE",
                "size": _size(item.stat().st_size),
                "url": reverse("library:file", args=[child]),
            })

    sem_map = _subject_to_sem()
    if rel in sem_map:
        slug = sem_map[rel]
        if slug in DIRECT:
            back_url = reverse("library:home")
            back_label = "Back to Materials"
        else:
            back_url = reverse("library:semester", args=[slug])
            back_label = "Back to Subjects"
    else:
        parent = rel.rsplit("/", 1)[0]
        back_url = reverse("library:browse", args=[parent])
        back_label = "Back"

    crumb_rel = rel[len(FY) + 1:] if rel.startswith(FY + "/") else rel
    return render(request, "materials/lib_browse.html", {
        "title": target.name,
        "crumb": " / ".join(crumb_rel.split("/")),
        "folders": folders,
        "files": files,
        "back_url": back_url,
        "back_label": back_label,
    })


def serve_file(request, subpath):
    target = _safe(subpath)
    if not target.is_file():
        raise Http404("File not found")
    ctype, _ = mimetypes.guess_type(target.name)
    ctype = ctype or "application/octet-stream"
    inline = ctype == "application/pdf" or ctype.startswith(("text/", "image/"))
    return FileResponse(
        open(target, "rb"),
        content_type=ctype,
        as_attachment=not inline,
        filename=target.name,
    )
