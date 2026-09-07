from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, Comment
from taggit.models import Tag
from django.db.models import Count, Q
from .forms import EmailPostForm, CommentForm, SearchForm
from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
def post_list(request, tag_slug=None):
    post_list = Post.published.all() 
    tag = None
    if tag_slug:
        tag = get_object_or_404(
            Tag, slug = tag_slug,
        )
        post_list = post_list.filter(tags__in=[tag])
        
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request,  'blog/post/list.html', {'posts': page_obj, 'tag': tag} )


# class PostListView(ListView,):
#     queryset = Post.published.all()
#     template_name = 'blog/post/list.html'
#     context_object_name = 'posts'
#     paginate_by = 2
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paginator = context['paginator']
    #     page_number = self.request.GET.get('page', 1)
    #     safe_page_obj = paginator.get_page(page_number)
    #     context['page_obj'] = safe_page_obj
    #     context['posts'] = safe_page_obj
    #     return context
    
    

def post_detail(request, year, month, day, slug_info):
    post = get_object_or_404(
        Post, 
        status='PB', 
        slug = slug_info, 
        publish__year= year , 
        publish__month = month, 
        publish__day = day,
        )
    comments = post.comments.filter(active=True)
    # this line does the same thing
    # comments = Comment.objects.filter(post = post, active=True )
    form = CommentForm()
    
    post_tag = post.tags.values_list('id', flat=True)
    similar_post = Post.published.filter(
        tags__in= post_tag
        ).exclude(pk = post.pk)
    similar_posts = similar_post.annotate(
        same_tag=Count('tags')
    ).order_by('-same_tag', '-publish')[:4]
    
    return render(request, 'blog/post/detail.html', {'post': post, 'form': form, 'comments': comments, 'similar_posts': similar_posts} )
def post_share(request, pk):
    post = get_object_or_404(
        Post, pk = pk, status= Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"Recommands you read {post.title}"
            )
            message = (
                f"Read {post.title} at {request.build_absolute_uri(post.get_absolute_url())}"
            )
            send_mail(
                subject = subject,
                message = message,
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list= [cd['to']],
                fail_silently=False,
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
@require_POST
def post_comment(request, pk):
    post = get_object_or_404(
        Post, pk = pk, status=Post.Status.PUBLISHED
    )
    comment = False
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        
        comment = True
    else:
        form = CommentForm()
    return render(request, 'blog/post/comment.html', {'post':post, 'form':form, 'comment': comment})
def post_search(request):
    cd = None
    search_ranking = None
    if 'search' in request.GET:
        form =SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data['search']
            stem_word = SearchQuery(cd)
            
            post = Post.published.annotate(
                 search = SearchVector('title', weight='A') + 
                             SearchVector('body', weight='B'),
                 rank = SearchRank(SearchVector('title', weight='A') + 
                             SearchVector('body', weight='B'), stem_word),
                 similarity = TrigramSimilarity('title', stem_word)
            )
            search_query = post.filter(search=stem_word)
            search_rating = search_query.filter(
                Q(rank__gte=0.3) | Q(similarity__gt=0.1))
            # search_rating = post.filter(
            #     Q(rank__gte=0.3) | Q(similarity__gt=0.1))
            search_ranking = search_rating.order_by('-rank', '-similarity')
    else:
        form = SearchForm()
    return render(request, 'blog/post/search.html', {'search_ranking': search_ranking , 'form': form, 'cd': cd})
        
