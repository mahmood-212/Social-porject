from cgi import print_arguments
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from posts.models import PersonalPost
from comments.foms import CommentForm
# Create your views here.

@login_required
def add_comment_personalpost(request, pk):
    
    form = CommentForm()
    personalpost = get_object_or_404(PersonalPost, pk=pk)
    print(f'$$$$$$$$$$$$$$$$$$$$$$$$$$ psot in {personalpost}')
    if request.method == 'POST':
        form = CommentForm(request.POST)
         
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = personalpost
            print(f'####################### from view is comment.post {comment.post}')
            print(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%% is pk{personalpost.pk}")
            comment.comment_author = request.user
            comment.save()

            return redirect('posts:post_detail', pk=personalpost.pk)
        
    else:
        form = CommentForm()
    return render(request, 'comments/comments_form.html', {'form':form})

@login_required
def comment_delete(request, pk):
    # get_object_or_404():
    # This function calls the given model and get object from that if that object or model doesn’t exist it raise 404 error.
    comment = get_object_or_404(models.Comment, pk=pk)
    personalpost_pk = comment.post.pk
    print(f'************************************* is-personalpost_pk {personalpost_pk}')
    comment = comment.delete()
    return redirect('posts:post_detail', pk=personalpost_pk)




