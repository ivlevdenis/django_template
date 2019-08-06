from django.urls import path

from apps.web.views import main

app_name = 'web'
urlpatterns = [
    path('', main.main_view, name='main')
]
