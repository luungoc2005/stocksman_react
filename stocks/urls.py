from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # get stock
    url(r'^get_stock/(?P<stock_code>[a-zA-Z0-9]{3})/$', views.get_stock),
    # ref data
    url(r'^ref/get_indices$', views.get_indices),
    # find stock
    url(r'^find_stock/(?P<code>[a-zA-Z0-9]+)/(?:(?P<limit>\d+))$', views.find_stock),
    # top stocks
    url(r'^top_stocks(?:/(?P<filter>[a-zA-Z]+))?(?:/(?P<timestamp>\d+))?(?:/(?P<limit>\d+))?/$',
        views.top_stocks),
]