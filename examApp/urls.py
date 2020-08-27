from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addUser', views.addUser),
    path('userPage', views.userPage),
    path('destroySession', views.destroySession),
    path('loginUser', views.loginUser),
    path('addQuote', views.addQuote),
    path('like/<int:quoteId>', views.like),
    path('userQuote/<int:userQuote>', views.userQuote),
    path('goHome', views.goHome),
    path('delete/<int:quoteId>', views.delete),
    path('editUser', views.editUser),
    path('confirmEdit', views.confirmEdit)
]
