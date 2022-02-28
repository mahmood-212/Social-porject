import imp
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from . import models
# Create your views here.
class CreateGroup(LoginRequiredMixin, generic.CreateView):
    model = models.Group
    fields = ['name', 'description']


class SingleGroup(generic.DetailView):
    model = models.Group
    


class ListGroup(generic.ListView):
    model = models.Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self,*args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    '''make checks if user in group or not '''
    def get(self, request, *args, **kwargs):
        #Try to get the exactly group or give 404 page
        group = get_object_or_404(models.Group, slug=self.kwargs.get('slug'))

        try:
            models.GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            messages.warning(self.request,'Warning already a member!')

        else:
            messages.success(self.request,'You are now a member!')

        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.get.objects.filter(user=self.request.user, group__slug=self.kwargs.get('slug')).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group !')

        else:
            membership.delete()
            messages.success(self.request,'You have left the group !')

        return super().get(request,*args,**kwargs)