from django.shortcuts import render
from markdown2 import markdown
from . import util
from django import forms

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
        "content": content,
    })

def edit(request,title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title,content)
        return render(request, "encyclopedia\edit.html", {
            "content": markdown(content),
        })
    content = util.get_entry(title)
    return render(request, "encyclopedia\edit.html", {
        "content": markdown(content)})