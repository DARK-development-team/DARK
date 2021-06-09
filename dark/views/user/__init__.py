__all__ = [
    'UserRegistrationView',
    'UserLoginView',
    'UserLogoutView',
]

from .login import UserLoginView
from .logout import UserLogoutView
from .register import UserRegistrationView
