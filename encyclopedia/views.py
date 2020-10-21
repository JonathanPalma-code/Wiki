from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import markdown2

entries = util.list_entries()
body_entry_error = "The requested page was not found."

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def search(request):
    query = request.GET.get('q')
    for entry in entries:
        if query.lower() == entry.lower():
            content = markdown2.markdown(util.get_entry(query))
            return render(request, "encyclopedia/subject.html", {
                "title": query, 
                "body": content,
                "success": True
        })
        matched_entry = []
        if query.lower() in entry.lower():
            matched_entry.append(entry)
            return render(request, "encyclopedia/search.html", {
                "query": query, 
                "match": matched_entry,
            })
    return render(request, "encyclopedia/subject.html", {
                "title": query, 
                "body": body_entry_error,
                "success": False
        })

def subject(request, title):
    if util.get_entry(title):
        body_entry = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/subject.html", {
            "title": title.capitalize(),
            "body": body_entry,
            "success": True
        })
    else:
        body_entry_error = "The requested page was not found."
        return render(request, "encyclopedia/subject.html", {
            "title": title, 
            "body": body_entry_error,
            "success": False
        })
