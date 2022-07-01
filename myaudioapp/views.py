from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from .models import Notification, Question, Answer, Like, Profile
from django.contrib.auth.models import User, auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count


@login_required(login_url='login')
def index(request):
    query = request.GET.get('q', None)
    list_of_question = Question.objects.all()
    if query is not None:
        list_of_question = Question.objects.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(user__username__icontains=query)
        )
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'index.html', {
        'unread_notifications':unread_notifications,
        'list_of_question':list_of_question
        
        })

def public_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    try:
        number_of_likes = Like.objects.filter(post__user=profile.user).count()
    except ObjectDoesNotExist:
        number_of_likes = None
    context = {
        'profile':profile,
        'number_of_likes':number_of_likes
    }
    return render(request, 'public_profile.html', context)

def viewQuestion(request, slug):
    question = get_object_or_404(Question, slug=slug)

    answers = Answer.objects.filter(post_id=question).annotate(likes_count=Count("like"))

    context = {'question':question, 'answers':answers}

    return render(request, 'viewQuestion.html', context)


class My_Question(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'body', 'category']
    template_name = 'question.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super (My_Question, self).form_valid(form)

class My_Answer(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer']
    template_name = 'answer.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        result = super().form_valid(form)
        question_author = form.instance.post.user
        Notification.objects.create(user=question_author, message="someone answer your question!", url=form.instance)
        return result

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification_list.html'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-timestamp")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credential') 
            return redirect('login')
    else:        
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email or user name Already taking')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username is taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                return redirect('index')
        else:
            messages.info(request, 'Password Not Match')
            return redirect('register')   
        return redirect ('/')     
    else:
        return render(request, 'signup.html')


def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)        
    Like.objects.get_or_create(post=answer, user=request.user)    
    return redirect('view-Question', answer.post.slug)
