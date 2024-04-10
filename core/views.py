from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    user_list = User.objects.all()
    context = {"users": user_list}
    return render(request, "index.html", context)


def user_message(request, id):
    single_user = get_object_or_404(User, pk=id)
    context = {"user": single_user}
    return render(request, "user_message.html", context)
