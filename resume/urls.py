from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # صفحه اصلی
    path('signup/', views.register_view, name='signup'),  # ثبت‌نام
    path('login/', views.login_view, name='login'),  # ورود
    path('logout/', views.logout_view, name='logout'),  # خروج
    path('dashboard/', views.dashboard_view, name='dashboard'),  # داشبورد
    path('personal-resume/', views.view_personal_resume, name='view_personal_resume'),  # رزومه
    # سایر مسیرهای مورد نیاز
    path('contact/', views.contact_view, name='contact'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('admin/', admin.site.urls),
    path('add-experience/', views.add_experience, name='add_experience'),
    path('add-education/', views.add_education, name='add_education'),
    path('add-portfolio/', views.add_portfolio, name='add_portfolio'),

    path('edit_skill/<int:id>/', views.edit_skill, name='edit_skill'),
     path('delete_skill/<int:id>/', views.delete_skill, name='delete_skill'),
     path('edit_experience/<int:id>/', views.edit_experience, name='edit_experience'),
    path('delete_experience/<int:id>/', views.delete_experience, name='delete_experience'),
    path('edit_education/<int:id>/', views.edit_education, name='edit_education'),
    path('delete_education/<int:id>/', views.delete_education, name='delete_education'),  # برای حذف

    path('portfolio/', views.portfolio_list, name='portfolio_list'),
     path('delete-portfolio/<int:id>/', views.delete_portfolio, name='delete_portfolio'),
    
]
