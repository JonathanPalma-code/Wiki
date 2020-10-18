from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import markdown2

body_entry_error = "The requested page was not found."

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    if query in entries:
        content = markdown2.markdown(util.get_entry(query))
        return render(request, "encyclopedia/subject.html", {
            "title": query, 
            "body": content,
            "success": True
        })
    else:
        matched_entry = []
        for entry in entries:
            if query.lower() in entry.lower():
                matched_entry.append(entry)
        return render(request, "encyclopedia/search.html", {
            "query": query, 
            "match": matched_entry,
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
        title_error = "Page Not Found"
        body_entry_error = "The requested page was not found."
        return render(request, "encyclopedia/subject.html", {
            "title": title_error, 
            "body": body_entry_error,
            "success": False
        })
