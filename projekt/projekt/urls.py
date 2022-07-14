"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView
from app_1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home_page, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('courses/', views.courses, name='courses'),
    path('all_students/', views.all_students, name='all_students'),
    path('student_list/<str:course_id>', views.student_list, name='student_list'),
    path('profesori/', views.profesori, name='profesori'),
    path('my_courses/<str:user_id>', views.my_courses, name='my_courses'),
    path('register/', views.register, name='register'),
    path('insert_course/', views.insert_course, name='insert_course'),
    path('detail_course/<str:course_id>', views.course_detail, name='detail_course'),
    path('insert_user/', views.insert_user, name='insert_user'),
    path('edit_user/<int:user_id>', views.edit_user, name='edit_user'),
    path('edit_course/<str:course_id>', views.edit_course, name='edit_course'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('details_user/<int:user_id>', views.user_details, name='details_user'),
    path('upisni_list/<int:student_id>', views.upisni_list, name='upisni_list'),
    path('ispis_predmeta/<int:predmet_id>/<int:student_id>', views.ispis_predmeta, name='ispis_predmeta'),
    path('upis_predmeta/<int:predmet_id>/<int:student_id>', views.upis_predmeta, name='upis_predmeta'),
    path('polozio_predmet/<int:predmet_id>/<int:student_id>', views.polozio_predmet, name='polozio_predmet'),
    path('izgubio_potpis/<int:predmet_id>/<int:student_id>', views.izgubio_potpis, name='izgubio_potpis'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
    path('zbroj_upisanih_bodova/<int:student_id>', views.zbroj_upisanih_bodova, name='zbroj_upisanih_bodova'),
    path('zbroj_polozenih_bodova/<int:student_id>', views.zbroj_polozenih_bodova, name='zbroj_polozenih_bodova'),

]
