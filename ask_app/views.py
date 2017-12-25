# coding=utf-8
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as l_in, logout as l_out
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


def question(request, _id):
    context = {}
    context = _get_user_context(request, context)

    try:
        main_question = Question.objects.get_with_tags(_id)
    except Question.DoesNotExist:
        raise Http404()

    answers = Answer.objects.get_with_likes(_id)
    answers_for_render = paginate(answers, request)

    if request.method == 'POST':
        form = AnswerForm(request.POST, context['user'], main_question)
        if form.is_valid():
            form.save()
            return redirect('question', _id)
    else:
        form = AnswerForm()

    context['form'] = form
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
        #context['user'] = UserProfile.objects.get_or_create(username=request.user.username)
        context['user'] = UserProfile.objects.get(username=request.user.username)
    else:
        context['user_logged_in'] = False
    return context


def login(request):
    if request.user.is_authenticated():
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
            user_auth = authenticate(username=username, password=password)  # try auth
            if user_auth is not None:  # if auth is success
                l_in(request, user_auth)  # start session
                return HttpResponseRedirect("/success")
            else:  # else, auth gone wrong
                form.add_error(None, "Username or password is incorrect")

    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.user.is_authenticated():
        context = {}
        context = _get_user_context(request, context)
        return render(request, 'index.html', context)
    if request.method == 'GET':
        register_form = RegisterForm()
    else:
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            new_profile = register_form.save()
            l_in(request, new_profile)
            return HttpResponseRedirect("/success")
    return render(request, 'registration.html', {'form': register_form})


def create_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/")
    else:
        form = AnswerForm()

    context = {'form': form}
    context = _get_user_context(request, context)
    return render(request, "form.html", context)


def success(request):
    context = {}
    context = _get_user_context(request, context)
    if request.user.is_authenticated():
        context['success'] = True
        return redirect('/')
    else:
        return render(request, 'success.html', {"success": False})


@login_required()
def logout(request):
    if request.user.is_authenticated():
        l_out(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@login_required()
def settings(request):
    user = request.user
    _profile = UserProfile.objects.filter(user_ptr_id=user.id).last()
    print("=====================")
    print(user.id)

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
