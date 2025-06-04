from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatGroup, ChatMessage
from .forms import ChatmessageCreateForm

@login_required
def chat_view(request, group_name='public-chat'):
    # Get selected group (default to 'public-chat')
    chat_group = get_object_or_404(ChatGroup, group_name=group_name)
    
    # Get all groups for sidebar
    user_groups = ChatGroup.objects.all()

    # Fetch chat messages in the group
    chat_messages = chat_group.chat_messages.all().order_by('created_at')

    # Instantiate form
    form = ChatmessageCreateForm()

    # Handle message POST
    if request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = chat_group
            message.author = request.user
            message.save()
            return redirect('chat', group_name=group_name)

    return render(request, 'chat_app/chat.html', {
        'chat_group': chat_group,
        'chat_messages': chat_messages,
        'form': form,
        'user_groups': user_groups,
        'show_navbar': True,
    })
