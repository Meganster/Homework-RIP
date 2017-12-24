# -*- coding: utf-8 -*-
import random

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import UserManager
from ask_app.models import *
from faker import Faker


class ManagerUserProfile:
    def create_user(self, username, password, email):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('Users must have a password')

        user = UserProfile(username=username, email=email, password=password)
        user.save()
        return user

    def get_by_username(self, username):
        user = UserProfile.objects.get(username=username)
        return user

    def get_by_id(self, _id):
        user = UserProfile.objects.get(id=_id)
        return user

fake = Faker()
usermanager = ManagerUserProfile()


def create_user():
    name = fake.name()
    email = fake.email()
    passwrd = fake.password()
    usermanager.create_user(username=name, password=passwrd, email=email)
    print('Successfully fill data for user "%s", "%s", "%s"' % (name, email, passwrd))

def create_question(user_id):
    title = fake.sentence()
    text = fake.text()
    question = Question(title=title, text=text, author=usermanager.get_by_id(user_id))
    question.save()
    print('Successfully fill data for question "%s", "%d"' % (title, user_id))

def create_answer(question_id, user_id):
    answer1 = Answer(text=fake.sentence(), author=usermanager.get_by_id(user_id), question=Question.objects.get(id=question_id))
    answer1.save()
    answer2 = Answer(text=fake.sentence(), author=usermanager.get_by_id(user_id + 1), question=Question.objects.get(id=question_id))
    answer2.save()
    print('Successfully fill data for answer1 "%d", "%d"' % (question_id, user_id))
    print('Successfully fill data for answer2 "%d", "%d"' % (question_id, user_id + 1))

def create_tag(question_id):
    words = fake.words()
    name_tag1 = words[0]
    name_tag2 = words[1]

    tag1 = Tag()
    tag1.name = name_tag1
    tag1.save()
    tag1.questions.add(Question.objects.get(id=question_id))
    tag1.save()

    tag2 = Tag()
    tag2.name = name_tag2
    tag2.save()
    tag2.questions.add(Question.objects.get(id=question_id))
    tag2.save()
    print('Successfully fill data for tag "%s", "%s", "%d"' % (name_tag1, name_tag2, question_id))

def create_like_answer(answer_id, user_id):
    like_answer = LikeAnswer(like_target_answer=Answer.objects.get(id=answer_id), author=usermanager.get_by_id(user_id))
    like_answer.save();
    print('Successfully fill data for like_answer "%d", "%d"' % (answer_id, user_id))

def create_like_question(question_id, user_id):
    for i in range(user_id, random.randrange(user_id, random.randint(user_id + 1, user_id + 10))):
        like_question = LikeQuestion(like_target_question=Question.objects.get(id=question_id), author=usermanager.get_by_id(i))
        like_question.save();
    print('Successfully fill data for like_question "%d", "%d"' % (question_id, user_id))

class Command(BaseCommand):
    def handle(self, *args, **options):
        max_const = 100
        #for i in range(1, max_const):
        #    create_user()

        #for i in range(1, max_const):
        #    create_question(i)

        #for i in range(1, max_const):
        #    create_answer(i + 00, i + 50)

        #for i in range(1, max_const):
        #   create_tag(i)

        #for i in range(1, max_const):
            #create_like_answer(i + 10, i + 40)
            #create_like_question(i + 4, i + 10)
