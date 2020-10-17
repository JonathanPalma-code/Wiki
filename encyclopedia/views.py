from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def subject(request, title):
    return render(request, "encyclopedia/subject.html", {
        "title": title.capitalize(),
        "entry": util.get_entry(title)
    })
