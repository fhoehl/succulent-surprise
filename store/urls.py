from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^tos/$', views.tos, name='tos'),
    url(r'^checkout/$', views.OrderCreate.as_view(), name='checkout'),
]
