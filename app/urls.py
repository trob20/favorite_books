from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('books', views.dashboard),
    path('books/add_book', views.add_book),
    path('books/<int:b_id>', views.display_all),
    path('books/favorites/<int:u_id>', views.display_one),
    path('books/update/<int:b_id>', views.update),
    path('books/delete/<int:b_id>', views.delete),
    path('books/favor/<int:b_id>', views.favor),
    path('books/unfavor/<int:b_id>', views.unfavor)
]