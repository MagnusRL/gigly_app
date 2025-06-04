from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatGroup, ChatMessage
from .forms import ChatmessageCreateForm
import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def chat_view(request, group_name=None):
    # Fetch all groups
    user_groups = ChatGroup.objects.all()

    # Case: user has no groups yet
    if not user_groups.exists():
        return render(request, 'chat_app/chat.html', {
            'user_groups': [],
            'chat_group': None,
            'chat_messages': [],
            'form': ChatmessageCreateForm(),
            'show_navbar': True,
        })

    # If group name is not specified, default to the first group
    if not group_name:
        return redirect('chat', group_name=user_groups.first().group_name)

    # Else, get the requested group
    chat_group = get_object_or_404(ChatGroup, group_name=group_name)
    chat_messages = chat_group.chat_messages.all().order_by('created_at')

    form = ChatmessageCreateForm()
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

@csrf_exempt
def create_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_name = data.get('groupName')
        group_users = data.get('groupUsers')

        if not group_name or not group_users:
            return JsonResponse({'error': 'Group name and users are required.'}, status=400)

        # Create the group
        group = ChatGroup.objects.create(group_name=group_name)

        # Add users to the group
        usernames = group_users.split(',')
        invalid_usernames = []
        valid_users = []
        User = get_user_model()  # Get the correct user model

        for username in usernames:
            try:
                user = User.objects.get(name=username.strip())  # Use 'name' instead of 'username'
                valid_users.append(user)
            except User.DoesNotExist:
                invalid_usernames.append(username.strip())

        if not valid_users:
            group.delete()  # Delete the group if no valid users are provided
            return JsonResponse({'error': 'No valid users provided. Group creation failed.'}, status=400)

        group.participants.set(valid_users)  # Add valid users to the group

        if invalid_usernames:
            return JsonResponse({'error': f"Invalid names: {', '.join(invalid_usernames)}"}, status=400)

        return JsonResponse({'message': 'Group created successfully!', 'group_name': group_name})
    return JsonResponse({'error': 'Invalid request method'}, status=405)