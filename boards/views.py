from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
# from django.http import HttpResponse
from django.http import Http404
from boards.models import Board, Topic, User, Post
from .forms import NewTopicForm, PostForm
from django.db.models import Count
from boards.forms import PostForm
from django.views.generic import CreateView, UpdateView, ListView
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
	# list_boards = list()
	boards= Board.objects.all()
	return render(request, 'home.html', {'boards':boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})

def about(request):
    # do something...
    return render(request, 'about.html')

def about_company(request):
    # do something else...
    # return some data along with the view...
    return render(request, 'about_company.html', {'company_name': 'Simple Complex'})

def about_vitor(request):
	return render(request, 'vitor.html')

def about_erica(request):
	return render(request, 'erica.html')

def privacy_policy(request):
	pass

def about_author(request):
	return render(request, 'author.html')

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'base.html', {'username':username})



'''When we call form.save(), it will automatically "commit" the operation, triggering the save method 
of the model class. The thing is, for the Topic model, the "board" and "starter" fields are non-nullable 
at the database level. Which means if we save the form without providing a "board" and "starter" value, it 
will throw an exception. So what we do is, save the form changing the commit flag to False so it will 
prepare all the model fields, then we provide the extra data which is mandatory (board and starter) and 
manually save the topic calling topic.save()'''

@login_required
def new_topic(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    # user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
                )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'newtopic.html', {'board': board, 'form': form})


def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    queryset = board.topics.order_by('-last_updated').annotate(replies = Count('posts')-1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(page.num_pages)
    return render(request, 'topics.html', {'board':board, 'topics':topics})


def forget_password(request ):
    return render(request, 'base.html')


def reset_pass(request):
    return render(request, 'password_reset.html')


@login_required
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views+=1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if(form.is_valid):
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )            

            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})            

class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name = 'new_post.html'

'''
Reverse_lazy is, as the name implies, a lazy implementation of the reverse URL resolver. Unlike the traditional 
reverse function, reverse_lazy won't execute until the value is needed. It is useful because it prevent 
'Reverse Not Found' exceptions when working with URLs that may not be immediately known.
'''

'''
We can’t decorate the class directly with the @login_required decorator. We have to use the utility 
@method_decorator, and pass a decorator (or a list of decorators) and tell which method should be decorated. 
In class-based views it’s common to decorate the dispatch method. It’s an internal method Django use (defined 
inside the View class). All requests pass through this method, so it’s safe to decorate it.
'''


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        # if(form.is_valid):  #it's unnesessary in GCBV, request.POST...
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'
    

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies = Count('posts')-1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):            
            self.topic.views+=1
            self.topic.save()
            self.request.session[session_key]=True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('-created_at')
        return queryset

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
