from django.shortcuts import render

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def subject(request, title):
    if util.get_entry(title):
        body_entry = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/subject.html", {
            "title": title.capitalize(),
            "entry": body_entry,
            "success": True
        })
    else:
        title_error = "Page Not Found"
        body_entry_error = "The requested page was not found."
        return render(request, "encyclopedia/subject.html", {
            "title": title_error, 
            "entry": body_entry_error,
            "success": False
        })
