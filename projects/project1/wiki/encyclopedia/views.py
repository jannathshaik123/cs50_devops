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
        "content": content,
    })

def edit(request,title):
    if util.get_entry(title) == None:
        content = "## Page was not found"
    if request.method == "POST":
        content = request.POST.get(util.get_entry(title))
        if content == "":
            return render(request, "encyclopedia\edit.html", {
                "content": markdown("## Content cannot be empty")}),
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("wiki:entry", args=(title,)))
    content = util.get_entry(title)
    return render(request, "encyclopedia\edit.html", {
        "content": markdown(content)})