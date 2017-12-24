# coding=utf-8
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.http.response import Http404, JsonResponse
from django.contrib.auth.decorators import login_required

from ask_app.forms import *
from .models import *


def index(request):
    context = {}
    context = _get_user_context(request, context)
    questions = Question.objects.recent_questions()
    questions_for_render = paginate(questions, request)
    context['objects'] = questions_for_render
    return render(request, 'index.html', context)


def tag(request, name):
    context = {}
    context = _get_user_context(request, context)
    questions = Question.objects.questions_by_tag(name)
    questions_for_render = paginate(questions, request)
    context['objects'] = questions_for_render
    return render(request, 'tag.html', context)


def hot(request):
    context = {}
    context = _get_user_context(request, context)
    questions = Question.objects.questions_with_high_rating()
    questions_for_render = paginate(questions, request)
    context['objects'] = questions_for_render
    return render(request, 'index.html', context)


def question(request, id):
    context = {}
    context = _get_user_context(request, context)
    main_question = Question.objects.get_with_tags(id)
    answers = Answer.objects.get_with_likes(id)
    answers_for_render = paginate(answers, request)
    context['question'] = main_question
    context['answers'] = answers_for_render
    return render(request, 'question.html', context)


def ask(request):
    context = {}
    context = _get_user_context(request, context)
    return render(request, 'ask.html', context)


def paginate(objects_list, request, page_objects_num=20):
    paginator = Paginator(objects_list, page_objects_num)
    page = request.GET.get('page')

    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects_page = paginator.page(paginator.num_pages)
    return objects_page


def _get_user_context(request, context):
    if request.user.is_authenticated():
        context['user_logged_in'] = True
        context['user'] = UserProfile.objects.get(username=request.user.username)
    else:
        context['user_logged_in'] = False
    return context


def login(request):
    if request.user.is_authenticated:
        context = {}
        context = _get_user_context(request, context)
        return render(request, 'index.html', context)

    # if a user just wants to login
    if request.method == 'GET':
        form = LoginForm()
    else:  # else, if he sends some data in POST
        form = LoginForm(request.POST)  # initialize the form with POST data
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request=request, username=username, password=password) # try auth
            if user is not None:  # if auth is success
                login(request, user)  # start session
                return HttpResponseRedirect("/success")
            else:  # else, auth gone wrong
                form.add_error(None, "Username or password is incorrect")

    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.user.is_authenticated:
        context = {}
        context = _get_user_context(request, context)
        return render(request, 'index.html', context)
    if request.method == 'GET':
        register_form = RegisterForm()
    else:
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            new_profile = register_form.save()
            login(request, new_profile)
            return HttpResponseRedirect("/success")
    return render(request, 'registration.html', {'form': register_form})


def success(request):
    context = _get_user_context(request)
    if request.user.is_authenticated():
        context['success'] = True
        return render(request, 'success.html', context)
    else:
        return render(request, 'success.html', {"success": False})


def logout(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

# old settings
# def settings(request):
#    context = _get_user_context(request)
#    return render(request, 'settings.html', context)

@login_required()
def settings(request):
    user = request.user
    _profile = UserProfile.objects.filter(id=user.id).last()

    if request.POST:
        form = ProfileForm(request.POST, request.FILES, _profile)
        if form.is_valid():
            _profile.username = form.cleaned_data["username"]
            _profile.email = form.cleaned_data["email"]
            if form.cleaned_data["avatar"]:
                _profile.avatar = form.cleaned_data["avatar"]
            _profile.save()
    else:
        # build initial dict
        init = {"username": _profile.username,
                "email": _profile.email,
                "avatar": _profile.avatar}
        form = ProfileForm(initial=init)

    context = {'form': form}
    context = _get_user_context(request, context)
    return render(request, 'settings.html', context)


@login_required()
def vote(request):
    try:
        qid = int(request.POST.get('qid'))
    except:
        return JsonResponse(dict(error='bad question id'))
    _vote = request.POST.get('vote')
    question = Question.objects.get_with_rating(id=qid)
    rating = question.rating
    if _vote == "inc":
        rating += 1
    else:
        rating -= 1
    return JsonResponse(dict(ok=1, vote=_vote, rating=rating))
