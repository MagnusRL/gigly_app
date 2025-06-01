from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatGroup, GroupMessage
from django.contrib.auth.decorators import login_required
from .forms import ChatmessageCreateForm

# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_group.chat_messages.all().order_by('created_at')
    form = ChatmessageCreateForm()

    if request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = chat_group
            message.author = request.user
            message.save()
            return redirect('chat')
        else:
            form = ChatmessageCreateForm()

    return render(request, 'chat_app/chat.html', {
        'chat_group': chat_group,
        'chat_messages': chat_messages,
        'form': form,
        'show_navbar': True,
    })