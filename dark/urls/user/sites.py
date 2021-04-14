from django.urls import path

from dark.views.user import UserRegistrationView, UserLoginView, UserLogoutView


class UserSite:
    def get_urls(self):
        urlpatterns = [
            path('register/', UserRegistrationView.as_view(), name='register'),
            path('login/', UserLoginView.as_view(template_name='dark/user/login.html'), name='login'),
            path('logout/', UserLogoutView.as_view(template_name='dark/user/logout.html'), name='logout'),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'user', 'user'


site = UserSite()
