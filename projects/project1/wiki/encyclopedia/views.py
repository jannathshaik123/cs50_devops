from django.shortcuts import render
from markdown2 import markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewPageForm(forms.Form): 
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia\index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    content = util.get_entry(title)
    if content == None:
        content = "## Page was not found"
    content = markdown(content)
    return render(request, "encyclopedia\entry.html", {
        "title": title,
        "content": content,
    })

def edit(request,title):
    isEmpty = "False"
    content = util.get_entry(title)
    if request.method == "POST":
        try:
            content = request.POST.get('content', None).strip()
            if not content:
                raise ValueError("Content cannot be empty")
        except (AttributeError, ValueError) as e:
            print(f"entering except block: {e}")
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": "Content cannot be empty",
                "isEmpty": "True"
            })
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
        
    if content == None:
        content = "404: Page was not found"
        isEmpty = "True"
    return render(request, "encyclopedia\edit.html", {
        "title": title,
        "content": content,
        "isEmpty": isEmpty})