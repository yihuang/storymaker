# coding: utf-8
from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, REDIRECT_FIELD_NAME
from .models import Story, StoryNode
from .forms import LoginForm, RegisterForm, StoryForm, NodeForm


def index(request):
    stories = Story.objects.all()
    return render(request, 'story/index.html', {'stories': stories})


@login_required
def createstory(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(request.user)
            return redirect('story:createnode', id=story.root_id)
    else:
        form = StoryForm()
    return render(request, 'story/createstory.html', {'form': form})


@login_required
def createnode(request, id):
    id = int(id)
    parent = StoryNode.objects.get(pk=id)
    story = parent.story
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            node = form.save(story, parent, request.user)
            return redirect('story:node', id=node.id)
    else:
        form = NodeForm()
    return render(request, 'story/createnode.html', {'story': story, 'parent': parent, 'form': form})


def node(request, id):
    node = StoryNode.objects.get(pk=int(id))
    return render(request, 'story/node.html', {'node': node})


def story(request, id):
    story = Story.objects.get(pk=int(id))
    candidates = StoryNode.objects\
        .filter(story=story)\
        .values('id',
                'parent_id',
                'created_by_id',
                'stars',
                'created_at'
                )

    children = defaultdict(list)
    for c in candidates:
        children[c['parent_id']].append(c)

    def sort_key(node):
        return (node['created_by_id'] != story.created_by_id, node['stars'])

    rawnodes = []
    cs = children[story.root_id]
    while cs:
        cs.sort(key=sort_key)
        node = cs[0]
        rawnodes.append(node)
        cs = children[node['id']]

    nodes = StoryNode.objects.filter(id__in=[n['id'] for n in rawnodes])
    return render(request, 'story/story.html', {'story': story, 'nodes': nodes})


def nodelist(request, parentid, id=None):
    parent = StoryNode.objects.get(pk=int(parentid))
    nodes = StoryNode.objects.filter(parent_id=parent.id)
    return render(request, 'story/nodelist.html', {'nodes': nodes, 'parent': parent, 'id': id})


def login(request):
    error = []
    redirect_to = request.GET.get(REDIRECT_FIELD_NAME, '')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                auth_login(request, user)
                return redirect(redirect_to or 'index')
            else:
                error.append('Please input the correct password')
        else:
            error.append('Please input both username and password')
    else:
        form = LoginForm()
    return render(request, 'story/login.html', {
        'form': form,
        'redirect_to': redirect_to,
        'redirect_name': REDIRECT_FIELD_NAME
    })


def register(request):
    redirect_to = request.GET.get(REDIRECT_FIELD_NAME, '')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])
            auth_login(request, user)
            return redirect(redirect_to or 'index')
    else:
        form = RegisterForm()
    return render(request, 'story/register.html', {'form': form})
