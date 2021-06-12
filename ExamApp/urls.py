from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('main', views.main),
    path('friends', views.friends),
    path('remove/<int:id>', views.remove),
    path('add/<int:id>', views.add),
    path('user/<int:id>', views.user)
]
