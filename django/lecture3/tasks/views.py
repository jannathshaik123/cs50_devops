from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

# tasks = [
#     # "Task 1",
#     # "Task 2",
#     # "Task 3"
# ]

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html",{
        "tasks": request.session["tasks"]# tasks is a list of strings
    }
)
    
def add_tasks(request):
    # if the request is a POST request
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        # check if the form is not valid
        else:
            return render(request,"tasks/add.html", {
                "form" : form})
            
    # if the request is a GET request   
    return render(request,"tasks/add.html", {
        "form" : NewTaskForm()
    })