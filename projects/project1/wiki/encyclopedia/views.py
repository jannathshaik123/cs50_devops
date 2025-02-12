from django.shortcuts import render
from markdown2 import markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint

class NewPageForm(forms.Form): 
    title = forms.CharField(widget=forms.TextInput, label="Title",required=True)

def index(request):
    return render(request, "encyclopedia\index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    content = util.get_entry(title)
    notFound = "False"
    if content == None:
        content = "## Page was not found"
        notFound = "True"
    content = markdown(content)
    return render(request, "encyclopedia\entry.html", {
        "title": title,
        "content": content,
        "notFound": notFound
    })

def edit(request,title):
    content = util.get_entry(title)
    if request.method == "POST":
        try:
            content = request.POST.get('content', None).strip()
            if not content:
                raise ValueError("Content cannot be empty")
        except (AttributeError, ValueError) as e:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": "Content cannot be empty",
                "isEmpty": "True"
            })
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
    if content == None:
        return render(request, "encyclopedia\edit.html", {
        "title": title,
        "content": "404: Page was not found",
        "isEmpty": "True"})
    return render(request, "encyclopedia\edit.html", {
        "title": title,
        "content": content,
        "isEmpty": "False"})
    
def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            util.save_entry(title,f"#{title}")
            # request.method = "GET"
            # return edit(request,title)
            return HttpResponseRedirect(reverse("encyclopedia:edit", args=[title]))
        # check if the form is not valid
        else:
            return render(request,r"encyclopedia\new.html", {
                "form" : form})
    return render(request,r"encyclopedia\new.html", {
                "form" : NewPageForm()})

def random_page(request):
    if len(util.list_entries())!=0:
        num = randint(0,len(util.list_entries())-1)
        page = util.list_entries()[num]
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[page]))

def search(request):
    if request.method == 'GET':
        try:
            name = request.GET.get('q').strip()
            if not name:
                raise ValueError("Content cannot be empty")
        except (AttributeError, ValueError):
            return render(request, "encyclopedia/entry.html", {
                "title": name,
                "content": markdown("##Search cannot be empty"),
                "isEmpty": "True"
            })
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[name]))