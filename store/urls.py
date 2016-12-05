from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^order/$', views.OrderCreate.as_view(), name='order'),
    url(r'^checkout/$', views.OrderCreate.as_view(), name='checkout'),
]
