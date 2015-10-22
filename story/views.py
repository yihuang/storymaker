from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Story, StoryNode

def index(request):
    stories = Story.objects.all()
    return render(request, 'story/index.html', {'stories': stories})

@login_required
def createstory(request):
    if request.method=='POST':
        story = Story(title=request.POST['title'], created_by=request.user)
        story.save()
        storynode = StoryNode(story=story, title='root', content=request.POST['content'], parent=None, created_by=request.user)
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
