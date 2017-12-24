from django.conf.urls import url
import ask_app.views as views

urlpatterns = [
               url(r'^login$', views.login, name='login'),
               url(r'^reg$', views.registration, name='reg'),
               url(r'^tag/(?P<name>\w+)$', views.tag, name='tag'),
               #url(r'^tag/', views.tag, name='tag'),
               url(r'^ask$', views.ask, name='ask'),
               url(r'^hot$', views.hot, name='hot'),
               url(r'^question/(?P<id>\d+)$', views.question, name='question'),
               #url(r'^question/', views.question, name='question'),
               url(r'^settings$', views.settings, name='settings'),
               url(r'^$', views.index, name='index'),
               url(r'^success$', views.success, name='success'),
               url(r'^logout$', views.logout, name='logout')
]