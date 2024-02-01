from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.login_in,name="login"),
    path("register",views.register,name="register"),
    path("index", views.index,name="index"),
    path("history",views.history, name="history"),
    path("loan",views.loan,name="loan"),
    path("balance",views.balance,name="balance"),
    path("send", views.send, name="send"),
    path('send_money_api/', views.send_money_api, name='send_money_api'),
    path('history/', views.history, name='transaction_history'),
    path('loanform', views.loanform, name="loanform"),
    path('formEdu',views.formEdu  , name="formEdu"),
    path('formHome',views.formHome,name="formHome"),
    path("mark_notification_as_read/",views.mark_notification_as_read, name="mark_notification_as_read"),
    path("mark_all_notifications_as_read/", views.mark_all_notifications_as_read, name="mark_all_notifications_as_read"),
    
    

   

]



# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)