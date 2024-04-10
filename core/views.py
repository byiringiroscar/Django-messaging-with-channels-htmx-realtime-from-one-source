from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from core.models import UserMessage
from django.http import HttpResponse
from faker import Faker
fake = Faker()
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    user_list = User.objects.all()
    if request.htmx:
        user_id = int(request.POST.get("user_id"))
        user = get_object_or_404(User, pk=user_id)
        message = fake.sentence()
        msg = UserMessage(message=message, user=user)
        msg.save()
        return HttpResponse(f'<p style="color: green; font-size: 16px;">message sent to {user.username}</p>')
    context = {"users": user_list}
    return render(request, "index.html", context)


@login_required
def user_message(request, id):
    user = request.user
    if user.id != id:
        return redirect('index')
    single_user = get_object_or_404(User, pk=id)
    messages = UserMessage.objects.filter(user=single_user)
    context = {
        "user": single_user,
        "messages": messages
        }
    return render(request, "user_message.html", context)


def auth_message(request):
    return HttpResponse("You are not authenticated you need to authenticate with admin in django normal ways this is test project. that's why there's no decorated login space")
