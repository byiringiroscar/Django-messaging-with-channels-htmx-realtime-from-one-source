from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    user_list = User.objects.all()
    context = {"users": user_list}
    return render(request, "index.html", context)
