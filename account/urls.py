from django.contrib.messages import success
from django.urls import path, reverse_lazy
from account import views as account_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(template_name='account/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='account/logout.html'),
         name='logout'),
    path('register/', account_views.register, name='register'),
    path('profile/', account_views.profile, name='profile'),
    path('change-profile/', account_views.change_profile, name='change_profile'),

    # reset_password
    path('password/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html',
        success_url=reverse_lazy('password_reset_done')),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ),
         name='password_reset_done'
         ),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confrim.html'
    ),
         name='password_reset_confirm'),
    path('password-reset-complated/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complated.html'
    ),
         name='password_reset_complete'),
]
