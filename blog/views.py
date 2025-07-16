from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from blog.forms import BlogForms, CommentForm
from blog.models import Blog, Like


@login_required
def home(request):
    blogs = Blog.objects.filter(published=True)
    search_published_blog = request.GET.get('search_published_blog')

    if search_published_blog:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_published_blog) | Q(content__icontains=search_published_blog),
            published=True)

    context = {
        "blogs": blogs  # 'SELECT "blog_blog"."id", "blog_blog"."name" FROM "blog_blog"'
    }

    return render(request, 'blog/home.html', context=context)


@login_required
def home_out(request):
    blogs = Blog.objects.filter(published=False, author=request.user)
    search_published_blog = request.GET.get('search_unpublished_blog')

    if search_published_blog:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_published_blog) | Q(content__icontains=search_published_blog),
            published=False, author=request.user)
    context = {
        "blogs": blogs  # 'SELECT "blog_blog"."id", "blog_blog"."name" FROM "blog_blog"'
    }

    return render(request, 'blog/home_out.html', context=context)


def create(request):
    if request.method == 'POST':
        form = BlogForms(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            if blog.published:
                return redirect('home')
            return redirect('home_out')
    else:
        form = BlogForms()
    context = {
        'form': form
    }
    return render(request, 'blog/create.html', context=context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment
from .forms import CommentForm

def detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blog=blog, parent=None).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog

            # check if reply
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    pass

            comment.save()
            return redirect('detail', blog_id=blog.id)
    else:
        form = CommentForm()

    context = {
        'blog': blog,
        'comments': comments,
        'comment_form': form,
        'user_likes_count': blog.comment_set.count(),  # example
        'request_user_is_liked': False,  # false by default
    }
    return render(request, 'blog/detail.html', context)


def like_dislike(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    user_like = Like.objects.filter(user=request.user, blog=blog).first()
    if not user_like:
        user_like = Like.objects.create(user=request.user, blog=blog)
    if user_like.is_liked:
        user_like.is_liked = False
    else:
        user_like.is_liked = True
    user_like.save()
    return redirect('detail', blog_id=blog_id)


def update(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == 'POST':
        form = BlogForms(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            if blog.published:
                return redirect('home')
            return redirect('home_out')
    else:
        form = BlogForms(instance=blog)
    return render(request, 'blog/update.html', {'form': form, 'blog': blog})


def delete(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    blog.delete()
    return redirect('home')

@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('detail', blog_id=comment.blog.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment_edit.html', {
        'form': form,
        'comment': comment,
    })


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    blog_id = comment.blog.id
    comment.delete()
    return redirect('detail', blog_id=blog_id)

# lookup expr
# > 3  field__gt = 3
# >= 3  field__gte = 3

# < 3  field__lt = 3
# <= 3  field__lte = 3

# = 'text'  field__exact = 'text'
# = 'Text' or 'text'  field__iexact = 'text'

# = '23Text910'  field__contains = 'Text'
# = '23Text910' or 'asdatext4842'  field__icontains = 'Text'

# = 'Text910'  field__starstwith = 'Text'
# = 'Text910' or 'text4842'  field__istarstwith = 'Text'

# = '1389284Text'  field__endswith = 'Text'
# = '1389284Text' or '22313text'  field__iendswith = 'Text'

# field is null;   field__isnull=True
# field is not null;   field__isnull=False
