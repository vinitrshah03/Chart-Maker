from django.urls import path
from .views import *

urlpatterns=[
    path('',home, name='home'),
    path('home2/',home2, name='home2'),
    path('about/',about, name='about'),
    path('profile/', profile, name='profile'),
    path('Login/',Login, name='Login'),
    path('register/',register, name='register'),
    path('contract/',contract, name='contract'),
    path('set-session/',set_session, name='set_session'),
    path('get-session/',get_session, name='get_session'),
    path('Line/',Line, name='Line'),
    path("bar",bar,name="bar"),
    path("pie",pie,name="pie"),
    path("Line/insertview",insertview,name="insertview"),
    path("Line/insertview2",insertview2,name="insertview2"),
    path("Line/plot_view",plot_view,name="plot_view"),
    path("bar_plot_view",bar_plot_view,name="bar_plot_view"),
    path("pie_plot_view",pie_plot_view,name="pie_plot_view"),
    path("Line/download_view",download_view,name="download_view"),
    path("pie/download_view",download_view,name="download_view"),
    path("bar/download_view",download_view,name="download_view"),
    path("download_view",download_view,name="download_view"),
    path("charts",charts,name = "charts"),
    path("randgentr",randgentr,name = "randgentr"),
    path("csvchart",csvchart,name = "csvchart"),
    path("csv",csv,name = "csv"),
    path("buttons",buttons,name="buttons"),
    path("password_reset/", password_reset, name="password_reset"),
    path("password_reset/done/", password_reset_done, name="password_reset_done"),
    path("password_reset/<int:pk>/<str:token>/", password_reset_confirm, name="password_reset_confirm"),
    path("password_reset/complete/", password_reset_complete, name="password_reset_complete"),
    path("bar_insert1",bar_insert1,name="bar_insert1"),
    path("bar_insert2",bar_insert2,name="bar_insert2"),
    path("pie_insert2",pie_insert2,name="pie_insert2"),
    path("pie_insert1",pie_insert1,name="pie_insert1"),
    path("all_images",all_images,name="all_images"),
    path("a_c",a_c,name="a_c"),
]