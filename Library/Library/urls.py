"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from firstapp import views
# from Users import views
from Users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', views.home, name='home_page'),
    path('books/', views.show_books, name='all_active_books'),
    path('update1/<int:id>/', views.update_book, name='update_book'),
    path('delete1/<int:pk>/', views.delete_book, name='delete_book'),
    path('soft-delete/<int:pk>/', views.soft_delete_book, name='soft_delete_book'),
    path('inactive-books/', views.show_inactive_books, name='all_inactive_books'),
    path('restore-books/<int:pk>/', views.restore_books, name='restore_books'),


    # path('book-form/', views.book_form, name='book_form'),
    # path('sibtc-form/', views.sibtc, name='sibtc'),

    # split view
    # path('views_a/', views.view_a, name='view_a),
    # path('views_b/', views.view_b, name='view_b),
    # path('sibtc-form/', views.sibtc, name='sib),
    # path('sibtc-form/', views.sibtc, name='sib),

    path("index/", views.index, name="index"),

    # User url
    path("register/", user_views.register_request, name="register"),
    path("login/", user_views.login_request, name="login_user"),
    path("logout/", user_views.logout_request, name="logout_user"),
    
    path("create-csv/", views.create_csv, name="create_csv"),
    path("create-excel-active-books/", views.create_excel_active_books, name="create_excel_active_books"),
    path("create-excel-inactive-books/", views.create_excel_inactive_books, name="create_excel_inactive_books"),
    path("upload-csv/", views.upload_csv, name="upload_csv"),
    path("read-text/", views.read_text, name="read_text"),
    path("download-csv/", views.download_csv, name="download_csv"),
    path("book-duplicate/", views.book_duplicate, name="book_duplicate"),
    path("book-/", views.book_duplicate, name="book_duplicate"),
    path("create-csv-raw/", views.create_csv_raw, name="create_csv_raw"),

    # class based view
    # path("cbv/", views.NewView.as_view(), name='cbv'),
    path("cbv-create-book/", views.BookCreate.as_view(), name='BookCreate'),
    path("retrive/", views.BookRetrive.as_view(), name='BookRetrive'),
    path("retrive/<int:pk>/", views.BookDetail.as_view(), name='BookDetail'),
    path("update/<int:pk>/", views.BookUpdate.as_view(), name='BookUpdate'),
    path("delete/<int:pk>/", views.BookDelete.as_view(), name='BookDelete'),

    path("login-cbv/", user_views.LoginPageView.as_view(), name='LoginPageView'),
    path("logout-cbv/", user_views.LogoutView.as_view(), name='LogoutView'),

    # another application users are fetching in another application
    path("get-studs/", views.get_all_stud, name="test"),



]
