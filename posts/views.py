from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from comments.models import Comment
from braces.views import SelectRelatedMixin
from django.http import Http404
from . import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

#what is SelectRelatedMixin:A simple mixin which allows you to specify a list or
# tuple of foreign key fields to perform a select_related on
class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'group')

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))

        except User.DoesNotExist:
            raise Http404

        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post_user']= self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related  = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = models.Post
    fields = ['message', 'group']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)
        # form.instance.created_by = self.request.user
        # return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        print(f"is from post gorup delete {queryset.filter(user_id=self.request.user.id)} &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request,'Post Delete')
        print(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ is messages delete {messages.success(self.request,'Post Delete')}")
        print(f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ is the result of delet function {super().delete(*args, **kwargs)}")
        return super().delete(*args, **kwargs)



'''Personal Posts Here'''
class PorsonalPostList(generic.ListView):
    model = models.PersonalPost

    def get_queryset(self):
        return models.PersonalPost.objects.filter(create_date__lte= timezone.now()).order_by('-create_date')

class PersonalPostCreate(LoginRequiredMixin, generic.CreateView):
    model = models.PersonalPost
    fields = ['title', 'text']

    #Here I have fields call 'author' but I don't want user enter this field. here by this funtion ↓
    # I let 'author' get 'username' by defualt 

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class PersonalPostDetail(generic.DetailView):
    model=models.PersonalPost

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['personalpost_list']= models.PersonalPost.objects.all()
        # context['comment_list'] = Comment.objects.all()
        # context['comment_list'] = Comment.comments_set.order_by('-create_date')

        
        return context
    

class PersonalPostDelete(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.PersonalPost
    success_url = reverse_lazy('posts:personalpost')
    select_related = ("author",)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     print(f"this is queryset ************************{queryset}")

    #     print(f"this is queryset filter ************************{queryset.filter(author_id=self.request.user.id)}")
    #     return queryset.filter(author_id=self.request.user.id)

    # def delete(self, *args, **kwargs):
    #     messages.success(self.request,'Post Delete')
    #     return super().delete(*args, **kwargs)