# coding=utf-8
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as l_in, logout as l_out
from django.http import HttpResponseRedirect
from django.http.response import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
import json

from ask_app.forms import *
from .models import *


class LoadView(View):
    def get(self, request):
        start = int(request.GET.get('start'))
        recent_questions = Question.objects.recent_questions()
        questions_for_send = []
        result = recent_questions[start:start + 4]
        for questn in result:
            questions_for_send.append(
                {
                    'text': questn.text,
                    'title': questn.title,
                    'author': questn.author.username,
                    'id': questn.id,
                    'avatar': questn.author.avatar.url,
                    # 'tags': list(questn.tags),
                    'number_answers': questn.number_answers,
                    'likes': questn.likes
                }
            )
        return HttpResponse(json.dumps(questions_for_send), content_type='application/json')


class AddAnswerView(View):
    def post(self, request):
        try:
            text = str(request.POST.get('text'))
            userid = int(request.POST.get('user'))
            questionid = int(request.POST.get('question'))
        except:
            return JsonResponse(dict(error='bad data'))

        if text:
            new_answer = Answer(author=UserProfile.objects.get(id=userid),
                                question=Question.objects.get(id=questionid),
                                text=text)
            new_answer.save()
            answer_for_send = []
            answer_for_send.append(
                {
                    'text': new_answer.text,
                    'createdate': str(new_answer.create_date.year) + "." + str(new_answer.create_date.month) + "." +
                                  str(new_answer.create_date.day),
                    'id': new_answer.id
                    # 'text': "super text for answer",
                    # 'createdate': "11.23.2017",
                    # 'id': "3"
                }
            )
            return HttpResponse(json.dumps(answer_for_send), content_type='application/json')
        else:
            return JsonResponse(dict(error='bad length of text'))


class IndexView(View):
    def get(self, request):
        context = {}
        context = _get_user_context(request, context)

        questions = Question.objects.recent_questions()
        questions_for_render = questions[0:20]
        context['objects'] = questions_for_render
        context['enable_modal_ask'] = True
        form = AskForm()

        context['form'] = form
        return render(request, 'index.html', context)

    def post(self, request):
        context = {}
        context = _get_user_context(request, context)

        questions = Question.objects.recent_questions()
        questions_for_render = questions[0:20]
        context['objects'] = questions_for_render
        context['enable_modal_ask'] = True
        form = AskForm(request.POST, UserProfile.objects.get(id=request.user.id))
        if form.is_valid():
            new_question = form.save()
            return redirect('question', new_question.id)

        context['form'] = form
        return render(request, 'index.html', context)

class TagView(View):
    def get(self, request, name):
        context = {}
        context = _get_user_context(request, context)
        questions = Question.objects.questions_by_tag(name)
        questions_for_render = questions[0:20]
        context['objects'] = questions_for_render
        # context['enable_modal_ask'] = True
        # if request.method == 'POST':
        #    form = AskForm(request.POST, UserProfile.objects.get(id=request.user.id))
        #    if form.is_valid():
        #        new_question = form.save()
        #        return redirect('question', new_question.id)
        # else:
        #    form = AskForm()
        # context['form'] = form
        return render(request, 'tag.html', context)

class HotView(View):
    def get(self, request):
        context = {}
        context = _get_user_context(request, context)
        questions = Question.objects.questions_with_high_rating()
        questions_for_render = paginate(questions, request)
        context['objects'] = questions_for_render
        return render(request, 'index.html', context)


class QuestionView(View):
    def get(self, request, _id):
        context = {}
        context = _get_user_context(request, context)

        try:
            main_question = Question.objects.get_with_tags(_id)
        except Question.DoesNotExist:
            raise Http404()

        answers = Answer.objects.get_with_likes(_id)
        answers_for_render = paginate(answers, request)
        form = AnswerForm()

        context['form'] = form
        context['question'] = main_question
        context['answers'] = answers_for_render
        return render(request, 'question.html', context)

    def post(self, request, _id):
        context = {}
        context = _get_user_context(request, context)

        try:
            main_question = Question.objects.get_with_tags(_id)
        except Question.DoesNotExist:
            raise Http404()
        answers = Answer.objects.get_with_likes(_id)
        answers_for_render = paginate(answers, request)
        form = AnswerForm(request.POST, context['user'], main_question)
        if form.is_valid():
            form.save()
            return redirect('question', _id)

        context['form'] = form
        context['question'] = main_question
        context['answers'] = answers_for_render
        return render(request, 'question.html', context)


class AskView(View):
    def get(self, request):
        context = {}
        context = _get_user_context(request, context)
        form = AskForm()

        context['form'] = form
        return render(request, 'ask.html', context)

    def post(self, request):
        context = {}
        context = _get_user_context(request, context)
        form = AskForm(request.POST, UserProfile.objects.get(id=request.user.id))
        if form.is_valid():
            new_question = form.save()
            return redirect('question', new_question.id)
        context['form'] = form
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
        # context['user'] = UserProfile.objects.get_or_create(username=request.user.username)
        context['user'] = UserProfile.objects.get(username=request.user.username)
    else:
        context['user_logged_in'] = False

    context['enable_modal_ask'] = False
    return context


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            context = {}
            context = _get_user_context(request, context)
            return render(request, 'index.html', context)

        form = LoginForm()
        return render(request, 'login.html', {
            'form': form
        })

    def post(self, request):
        if request.user.is_authenticated():
            context = {}
            context = _get_user_context(request, context)
            return render(request, 'index.html', context)

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
        return render(request, 'login.html', {
            'form': form
        })


class RegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated():
            context = {}
            context = _get_user_context(request, context)
            return render(request, 'index.html', context)

        register_form = RegisterForm()
        return render(request, 'registration.html', {
            'form': register_form
        })

    def post(self, request):
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            new_profile = register_form.save()
            l_in(request, new_profile)
            return HttpResponseRedirect("/success")
        return render(request, 'registration.html', {
            'form': register_form
        })


class SuccessView(View):
    def get(self, request):
        context = {}
        context = _get_user_context(request, context)
        if request.user.is_authenticated():
            context['success'] = True
            return redirect('/')
        else:
            return render(request, 'success.html', {
                'success': False
            })


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated():
            l_out(request)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


class SettingsView(View):
    def get(self, request):
        user = request.user
        _profile = UserProfile.objects.filter(user_ptr_id=user.id).last()
        print("=====================")
        print(user.id)

        init = {"username": _profile.username,
                "email": _profile.email,
                "avatar": _profile.avatar}
        form = ProfileForm(initial=init)
        context = {'form': form}
        context = _get_user_context(request, context)
        return render(request, 'settings.html', context)

    def post(self, request):
        user = request.user
        _profile = UserProfile.objects.filter(user_ptr_id=user.id).last()
        print("=====================")
        print(user.id)

        form = ProfileForm(request.POST, request.FILES, _profile)
        if form.is_valid():
            _profile.username = form.cleaned_data["username"]
            _profile.email = form.cleaned_data["email"]
            if form.cleaned_data["avatar"]:
                _profile.avatar = form.cleaned_data["avatar"]
            _profile.save()
        context = {'form': form}
        context = _get_user_context(request, context)
        return render(request, 'settings.html', context)


class VoteView(View):
    def post(self, request):
        try:
            qid = int(request.POST.get('qid'))
        except:
            return JsonResponse(dict(error='bad question id'))

        _vote = request.POST.get('vote')
        question = Question.objects.get_with_tags(question_id=qid)
        likes = question.likes
        if _vote == "inc":
            likes += 1
        else:
            likes -= 1
        return JsonResponse(dict(ok=1, vote=_vote, likes=likes))

class AnswerView(View):
    def post(self, request):
        try:
            qid = int(request.POST.get('qid'))
        except:
            return JsonResponse(dict(error='bad question id'))

        _vote = request.POST.get('vote')
        question = Question.objects.get_with_tags(question_id=qid)
        likes = question.likes
        if _vote == "inc":
            likes += 1
        else:
            likes -= 1
        return JsonResponse(dict(ok=1, vote=_vote, likes=likes))