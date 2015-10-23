# coding: utf-8
from django import forms
from django.contrib.auth.models import User
from .models import Story, StoryNode


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label=u'帐号')
    first_name = forms.CharField(label=u'昵称')
    password1 = forms.CharField(widget=forms.PasswordInput, label=u'密码')
    password2 = forms.CharField(widget=forms.PasswordInput, label=u'确认')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                u'输入密码不匹配',
                code='password_mismatch',
            )
        return password2

    class Meta:
        model = User
        fields = ('username', 'first_name')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label=u'帐号')
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)


class StoryForm(forms.ModelForm):
    title = forms.CharField(label=u'标题')
    content = forms.CharField(label=u'简介', widget=forms.Textarea)

    def save(self, user, commit=True):
        story = super(StoryForm, self).save(commit=False)
        story.created_by = user
        story.save()
        node = StoryNode(
            story=story,
            title='',
            content=self.cleaned_data['content'],
            parent=None,
            created_by=user)
        node.save()
        story.root = node
        story.save()
        return story

    class Meta:
        model = Story
        fields = ('title',)


class NodeForm(forms.ModelForm):
    title = forms.CharField(label=u'章节名')
    content = forms.CharField(label=u'内容', widget=forms.Textarea)

    def save(self, story, parent, user, commit=True):
        node = super(NodeForm, self).save(commit=False)
        node.created_by = user
        node.story = story
        node.parent = parent
        if commit:
            node.save()
        return node

    class Meta:
        model = StoryNode
        fields = ('title', 'content')
