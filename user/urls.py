from django.conf.urls import url, include
from . import views


urlpatterns = [

    url(r'^user/login/$', views.UserLogin.as_view()),

    url(r'^user/(?P<user_id>[0-9]+)/logout/$', views.UserLogout.as_view()),

    url(r'^user/register/$', views.UserRegistration.as_view()),

    url(r'^admin/(?P<admin_id>[0-9]+)/user/$', views.AdminUser.as_view()),

    url(r'^admin/(?P<admin_id>[0-9]+)/user/(?P<user_id>[0-9]+)/$', views.AdminModifyUser.as_view()),

]