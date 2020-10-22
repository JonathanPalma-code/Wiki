from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

from markdown2 import markdown

entries = util.list_entries()
body_entry_error = "The requested page was not found."
convert_HTML = markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(label="File Name", max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control col-md-6 col-lg-6'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-6 col-lg-6', 'rows' : 10}))

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-6 col-lg-6', 'rows' : 10}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def subject(request, title):
    if util.get_entry(title):
        body_entry = convert_HTML(util.get_entry(title))
        return render(request, "encyclopedia/subject.html", {
            "title": title.capitalize(),
            "body": body_entry,
            "success": True
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "query": title, 
            "error": body_entry_error,
            "success": False
        })

def search(request):
    query = request.GET.get('q').lower()
    matched_entry = []
    for entry in entries:
        entry = entry.lower()
        if query == entry:
            content = convert_HTML(util.get_entry(query))
            return render(request, "encyclopedia/subject.html", {
                "title": query, 
                "body": content,
                "success": True
        })
        if query in entry:
            matched_entry.append(entry)
    return render(request, "encyclopedia/search.html", {
        "query": query, 
        "match": matched_entry,
        "error": body_entry_error
    })
    
def add(request):
    if request.method == 'POST':
        # Take in the data the user submitted and save it as form 
        form = NewEntryForm(request.POST) 
        # Check if form data is valid (server-side) 
        if form.is_valid():
            # gives access of all the data that user submitted, in this case 'title' & 'content'
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title not in entries:
                entry = util.save_entry(title, content)
                convert_HTML(util.get_entry(title))
                # URL accepting arguments, passing them in args.
                return HttpResponseRedirect(reverse('encyclopedia:subject', args=[title]))
            else:
                return render(request, 'encyclopedia/subject.html', {
                    "title": "Could not save the file", 
                    "body": "The file already exists.",
                    "success": False
                })
        else:
            return render(request, 'encyclopedia/add.html', {
                'form': form
            })

    return render(request, 'encyclopedia/add.html', {
        'form': NewEntryForm()
    })

def edit(request, title): 
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            body = util.get_entry(title)
            body_converted = convert_HTML(body)
            return render(request, 'encyclopedia/subject.html', {
                "title": title, 
                "body": body_converted,
                "success": True
            })
    else:
        body = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
        'title': title,
        'form': EditEntryForm(initial={'content':body})
    })
