"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy
from chat import views

app_name='chat'
urlpatterns = [
    path('', views.MesssageListView.as_view()),
    path('messages', views.MesssageListView.as_view(), name='all'),
    path('messages/<int:pk>', views.MesssageDetailView.as_view(), name='message_detail'),
    path('messages/create',
         views.MesssageCreateView.as_view(success_url=reverse_lazy('chat:all')), name='message_create'),
    path('messages/<int:pk>/update',
         views.MesssageUpdateView.as_view(success_url=reverse_lazy('chat:all')), name='message_update'),
    path('messages/<int:pk>/delete',
         views.MesssageDeleteView.as_view(success_url=reverse_lazy('chat:all')), name='message_delete'),
    path('registration', views.RegistrationView.as_view(), name='registration'),
]
