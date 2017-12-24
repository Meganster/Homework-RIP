# coding=utf-8
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as l_in, logout as l_out
from django.http import HttpResponseRedirect

from ask_app import forms
from .models import *

def settings(request):
    context = _get_user_context(request)
    return render(request, 'settings.html', context)


def index(request):
    context = _get_user_context(request)
    questions = Question.objects.recent_questions()
    questions_for_render = paginate(questions, request)
    context['objects'] = questions_for_render
    return render(request, 'index.html', context)


def tag(request, name):
    context = _get_user_context(request)
    questions = Question.objects.questions_by_tag(name)
    questions_for_render = paginate(questions, request)
    context['objects'] = questions_for_render
    return render(request, 'tag.html', context)


def hot(request):
    context = _get_user_context(request)
    questions = Question.objects.questions_with_high_rating()
    questions_for_render = paginate(questions, request)
    context['objects'] = questions_for_render
    return render(request, 'index.html', context)


def question(request, id):
    context = _get_user_context(request)
    main_question = Question.objects.get_with_tags(id)
    answers = Answer.objects.get_with_likes(id)
    answers_for_render = paginate(answers, request)
    context['question'] = main_question
    context['answers'] = answers_for_render
    return render(request, 'question.html', context)


def ask(request):
    context = _get_user_context(request)
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


def _get_user_context(request):
    context = {}
    if request.user.is_authenticated():
        context['user_logged_in'] = True
        context['user'] = UserProfile.objects.get(username=request.user.username)
    else:
        context['user_logged_in'] = False
    return context


def registration(request):
    context = _get_user_context(request)
    errors = []
    if context['user_logged_in']:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            password = form.cleaned_data['password']
            confirmpass = form.cleaned_data['confirmpass']
            if password != confirmpass:
                errors.append("Пароли не совпадают")
            data = form.data.copy()
            same_UserProfiles = None
            try:
                same_UserProfiles = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                pass
            if same_UserProfiles:
                errors.append("Пользователь с таким именем уже существует")
                data['username'] = ""
            same_UserProfiles = None
            try:
                same_UserProfiles = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                pass
            if same_UserProfiles:
                errors.append("Пользователь с таким адресом эл. почты уже существует")
                data['email'] = ""
            form.data = data
            if errors:
                return render(request, 'registration.html', {'form': form,
                              'errors': errors})
            UserProfile.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
        return HttpResponseRedirect("/login")
    return render(request, 'registration.html', {'form': forms.RegistrationForm(), 'errors': []})


def login(request):
    context = _get_user_context(request)
    errors = []
    if context["user_logged_in"]:
        return HttpResponseRedirect('/')
    # переписать все проверки в хенделы для формы
    # и вызывать только form.is_valid()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = None
            try:
                user = UserProfile.objects.get(username=username_or_email)
            except UserProfile.DoesNotExist:
                try:
                    user = UserProfile.objects.get(email=username_or_email)
                except UserProfile.DoesNotExist:
                    errors.append("Пользователя с таким именем или адресом эл. почты не существует")
                    return render(request, 'login.html', {'form': form, 'errors': errors})

            user_auth = authenticate(username=user.username, password=password)
            if user_auth is not None:
                l_in(request, user_auth)
                return HttpResponseRedirect("/success")
            else:
                errors.append("Пароль неверен")
                return render(request, 'login.html', {'form': form, 'errors': errors})
    return render(request, 'login.html', {'form': forms.LoginForm()})


def success(request):
    context = _get_user_context(request)
    if request.user.is_authenticated():
        context['success'] = True
        return render(request, 'success.html', context)
    else:
        return render(request, 'success.html', {"success": False})


def logout(request):
    if request.user.is_authenticated():
        l_out(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')