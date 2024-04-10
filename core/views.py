from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from core.models import UserMessage
from django.http import HttpResponse
from faker import Faker
fake = Faker()

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


def user_message(request, id):
    single_user = get_object_or_404(User, pk=id)
    messages = UserMessage.objects.filter(user=single_user)
    context = {
        "user": single_user,
        "messages": messages
        }
    return render(request, "user_message.html", context)
