from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
  url(r'^$', Home.as_view(), name='home'),
  url(r'^user/', include('registration.backends.simple.urls')),
  url(r'^user/', include('django.contrib.auth.urls')),
  url(r'^review/create/$', login_required(ReviewCreateView.as_view()), name='review_create'),
  url(r'review/$', login_required(ReviewListView.as_view()), name='review_list'),
  url(r'^review/(?P<pk>\d+)/$', login_required(ReviewDetailView.as_view()), name='review_detail'),
  url(r'^review/update/(?P<pk>\d+)/$', login_required(ReviewUpdateView.as_view()), name='review_update'),
  url(r'^review/delete/(?P<pk>\d+)/$', login_required(ReviewDeleteView.as_view()), name='review_delete'),
  url(r'^review/(?P<pk>\d+)/comment/create/$', login_required(CommentCreateView.as_view()), name='comment_create'),
  url(r'^review/(?P<review_pk>\d+)/comment/update/(?P<comment_pk>\d+)/$', login_required(CommentUpdateView.as_view()), name='comment_update'),
  url(r'^review/(?P<review_pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', login_required(CommentDeleteView.as_view()), name='comment_delete'),
  url(r'^vote/$', login_required(VoteFormView.as_view()), name='vote'),
  url(r'^user/(?P<slug>\w+)/$', login_required(UserDetailView.as_view()), name='user_detail'),
  url(r'^user/update/(?P<slug>\w+)/$', login_required(UserUpdateView.as_view()), name='user_update'),
  url(r'^user/delete/(?P<slug>\w+)/$', login_required(UserDeleteView.as_view()), name='user_delete'),
  url(r'^search/$', login_required(SearchReviewListView.as_view()), name='search'),
)