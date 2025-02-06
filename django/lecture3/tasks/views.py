from django.shortcuts import render

tasks = [
    "Task 1",
    "Task 2",
    "Task 3"
]

# Create your views here.
def index(request):
    return render(request, "tasks/index.html",{
        "tasks": tasks # tasks is a list of strings
    }
)