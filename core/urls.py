from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
  url(r'^$', Home.as_view(), name='home'),
  url(r'^user/', include('registration.backends.simple.urls')),
  url(r'^user/', include('django.contrib.auth.urls')),
  url(r'^question/create/$', login_required(QuestionCreateView.as_view()), name='question_create'),
  url(r'question/$', login_required(QuestionListView.as_view()), name='question_list'),
  url(r'^question/(?P<pk>\d+)/$', login_required(QuestionDetailView.as_view()), name='question_detail'),
  url(r'^question/update/(?P<pk>\d+)/$', login_required(QuestionUpdateView.as_view()), name='question_update'),
  url(r'^question/delete/(?P<pk>\d+)/$', login_required(QuestionDeleteView.as_view()), name='question_delete'),
  url(r'^question/(?P<pk>\d+)/answer/create/$', login_required(AnswerCreateView.as_view()), name='answer_create'),
  url(r'^question/(?P<question_pk>\d+)/answer/update/(?P<answer_pk>\d+)/$', login_required(AnswerUpdateView.as_view()), name='answer_update'),
  url(r'^question/(?P<question_pk>\d+)/answer/delete/(?P<answer_pk>\d+)/$', login_required(AnswerDeleteView.as_view()), name='answer_delete'),
  url(r'^vote/$', login_required(VoteFormView.as_view()), name='vote'),
  url(r'^user/(?P<slug>\w+)/$', login_required(UserDetailView.as_view()), name='user_detail'),
  url(r'^user/update/(?P<slug>\w+)/$', login_required(UserUpdateView.as_view()), name='user_update'),
  url(r'^user/delete/(?P<slug>\w+)/$', login_required(UserDeleteView.as_view()), name='user_delete'),
  url(r'^search/$', login_required(SearchQuestionListView.as_view()), name='search'),
)