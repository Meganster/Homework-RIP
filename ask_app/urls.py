from django.conf.urls import url
import ask_app.views as views

urlpatterns = [
               url(r'^login$', views.LoginView.as_view(), name='login'),
               url(r'^reg$', views.RegistrationView.as_view(), name='reg'),
               url(r'^tag/(?P<name>\w+)$', views.TagView.as_view(), name='tag'),
               #url(r'^tag/', views.tag, name='tag'),
               url(r'^ask$', views.AskView.as_view(), name='ask'),
               url(r'^hot$', views.HotView.as_view(), name='hot'),
               url(r'^question/(?P<_id>\d+)$', views.QuestionView.as_view(), name='question'),
               #url(r'^question/', views.question, name='question'),
               url(r'^settings$', views.SettingsView.as_view(), name='settings'),
               url(r'^$', views.IndexView.as_view(), name='index'),
               url(r'^success$', views.SuccessView.as_view(), name='success'),
               url(r'^logout$', views.LogoutView.as_view(), name='logout'),
               url(r'^vote/$', views.VoteView.as_view()),
               url(r'^load/', views.LoadView.as_view()),
               url(r'^addanswer/', views.AddAnswerView.as_view())
]