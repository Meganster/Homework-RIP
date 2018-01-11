# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(User):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True, verbose_name='Аватар', default='avatar.jpg')

    class Meta:
        verbose_name = 'Userprofile'
        verbose_name_plural = 'Userprofiles'

    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return "%d: \n\t%s" % (self.id, self.username)


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Тег')
    questions = models.ManyToManyField('Question')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


# class Like(models.Model):
#    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
#    like_date_time = models.DateTimeField(auto_now_add=True)
#    like_target_question = models.ForeignKey('Question', on_delete=models.CASCADE)
#    like_target_answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
# unique для 3 полей
# две модели лайков для вопросов и ответов
# две связи к вопросу и к ответу одна из них нулл


class QuestionManager(models.Manager):
    @staticmethod
    def add_likes(all_questions):
        for question in all_questions:
            all_likes = LikeQuestion.objects.filter(like_target_question=question)
            # question.likes = len(all_likes)
            question.likes = 0
            for like in all_likes:
                question.likes += like.status
        return all_questions

    @staticmethod
    def add_tags(all_questions):
        for question in all_questions:
            question_tags = list(Tag.objects.filter(questions__id=int(question.id)))
            question.tags = question_tags
        return all_questions

    @staticmethod
    def add_numbers_answers(all_questions):
        for question in all_questions:
            all_answers = Answer.objects.filter(question=question)
            question.number_answers = len(all_answers)
        return all_questions

    # новые вопросы
    def recent_questions(self):
        all_questions = list(super(QuestionManager, self).get_queryset().order_by('-create_date'))
        self.add_likes(all_questions)
        self.add_tags(all_questions)
        self.add_numbers_answers(all_questions)
        return all_questions

    # вопросы по тегу
    def questions_by_tag(self, tag):
        all_questions = Question.objects.filter(tag__name=tag)
        self.add_tags(all_questions)
        self.add_likes(all_questions)
        self.add_numbers_answers(all_questions)
        return all_questions

    # самые популярные вопросы
    def questions_with_high_rating(self):
        all_questions = Question.objects.all()
        self.add_likes(all_questions)
        self.add_tags(all_questions)
        self.add_numbers_answers(all_questions)

        result = list(all_questions)
        result.sort(key=lambda question: question.likes, reverse=True)
        return result

    # выберет все вопросы и
    # добавит к ним теги
    def get_all_with_tags(self):
        all_questions = list(Question.objects.all())
        self.add_tags(all_questions)
        self.add_likes(all_questions)
        return all_questions

    # выберет один вопрос с question_id и
    # добавит к нему теги
    def get_with_tags(self, question_id):
        question = Question.objects.get(id=question_id)
        question_tags = list(Tag.objects.filter(questions__id=int(question_id)))
        question.tags = question_tags
        all_likes = LikeQuestion.objects.filter(like_target_question=question)
        question.likes = 0
        for like in all_likes:
            question.likes += like.status
        return question


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок вопроса')
    text = models.TextField(verbose_name=u'Тело вопроса')
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name=u'Автор')
    create_date = models.DateField(auto_now_add=True, verbose_name=u'Дата создания')

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return "%s: \n\t%s" % (self.title, self.text)


class AnswerManager(models.Manager):
    # выберет все ответы на вопрос с question_id и
    # добавит к ним лайки
    def get_with_likes(self, question_id):
        all_answers = Answer.objects.filter(question=int(question_id))
        for answer in all_answers:
            all_likes = LikeAnswer.objects.filter(like_target_answer=answer)
            answer.likes = len(all_likes)
        return all_answers


class Answer(models.Model):
    text = models.TextField(verbose_name=u'Тело ответа')
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True, verbose_name=u'Дата создания')

    objects = AnswerManager()

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return "%d: \n\t%s" % (self.id, self.text)


class LikeQuestion(models.Model):
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    like_date_time = models.DateTimeField(auto_now_add=True)
    like_target_question = models.ForeignKey('Question', on_delete=models.CASCADE)
    status = models.IntegerField(default=0, verbose_name=u'Статус лайк или дизлайк')

    class Meta:
        unique_together = ('author', 'like_target_question',)
        verbose_name = 'Like for question'
        verbose_name_plural = 'Like for questions'

    def __str__(self):
        return "%s: \n\t%d" % (self.author, self.status)


class LikeAnswer(models.Model):
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    like_date_time = models.DateTimeField(auto_now_add=True)
    like_target_answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    status = models.IntegerField(default=0, verbose_name=u'Статус лайк или дизлайк')

    class Meta:
        unique_together = ('author', 'like_target_answer',)
        verbose_name = 'Like for answer'
        verbose_name_plural = 'Like for answers'

    def __str__(self):
        return "%s: \n\t%d" % (self.author, self.status)
