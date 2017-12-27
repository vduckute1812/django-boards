from django.conf.urls import include, url
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('about/author/', include([
    	path('', views.about_author,  name='about_author'),
    	path('vitor/', views.about_vitor, name='about_vitor'),
    	path('erica/', views.about_erica, name = 'about_erica'),
    	])),

    path('/', include([
		re_path(r'^(?P<pk>\d+)/new/$', views.new_topic, name = 'new_topic'),
    	re_path(r'^(?:page-(?P<pk>\d+))/$', views.TopicListView.as_view(), name='board_topics'),
        re_path(r'^(?P<username>[\w.@+-]+)/$', views.user_profile, name='user_profile'),	
        re_path(r'^privacy/$', views.privacy_policy, name='privacy_policy'),
        re_path(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
        re_path(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
        re_path(r'^about/$', views.about, name='about'),
        re_path(r'^about/company/$', views.about_company, name='about_company'),
        re_path(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/$', views.PostUpdateView.as_view(), name='edit_post'),
        ])),
]
