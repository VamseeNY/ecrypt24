from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.registerView),
    path('login/',views.loginView)
]
