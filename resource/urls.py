from django.conf.urls import url, include
from . import views


urlpatterns = [

    url(r'^admin/(?P<admin_id>[0-9]+)/user/resource/$', views.AdminUserResource.as_view()),

    url(r'^user/(?P<user_id>[0-9]+)/resource/$', views.UserResource.as_view()),

]