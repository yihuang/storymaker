from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from .models import Story, StoryNode
from .forms import LoginForm, RegisterForm


def index(request):
    stories = Story.objects.all()
    return render(request, 'story/index.html', {'stories': stories})

@login_required
def createstory(request):
    if request.method=='POST':
        story = Story(title=request.POST['title'], created_by=request.user)
        story.save()
        storynode = StoryNode(story=story, title='', content=request.POST['content'], parent=None, created_by=request.user)
        storynode.save()
        story.root = storynode
        story.save()
        return redirect('story:createnode', id=storynode.id)
    return render(request, 'story/createstory.html', {})

@login_required
def createnode(request, id):
    id = int(id)
    parent = StoryNode.objects.get(pk=id)
    story = parent.story
    if request.method=='POST':
        node = StoryNode(title=request.POST['title'], content=request.POST['content'], created_by=request.user, story=story, parent=parent)
        node.save()
        return redirect('story:node', id=node.id)
    return render(request, 'story/createnode.html', {'story': story, 'parent': parent})

def node(request, id):
    node = StoryNode.objects.get(pk=int(id))
    return render(request, 'story/node.html', {'node': node})

def nodelist(request, parentid, id=None):
    parent = StoryNode.objects.get(pk=int(parentid))
    nodes = StoryNode.objects.filter(parent_id=parent.id)
    return render(request, 'story/nodelist.html', {'nodes': nodes, 'parent': parent, 'id': id})


def login(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                auth_login(request, user)
                return redirect('index')
            else:
                error.append('Please input the correct password')
        else:
            error.append('Please input both username and password')
    else:
        form = LoginForm()
    return render(request, 'story/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
    else:
        form = RegisterForm()
    return render(request, 'story/register.html', {'form': form})
