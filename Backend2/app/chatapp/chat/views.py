from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Message
from django.contrib import messages
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'chat/signup.html', {'form': form})


@login_required
def chat_list(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude self
    return render(request, 'chat/chat_list.html', {'users': users})

@csrf_exempt
@login_required
def chat_room(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user], receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get("message")
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
        return redirect('chat_room', username=username)

    return render(request, 'chat/chat_room.html', {
        'other_user': other_user,
        'messages': messages
    })
