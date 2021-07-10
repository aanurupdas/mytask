from django.urls import path
from users.views import signup, signin, verify_user, resend_verification_email


urlpatterns = [
    path("signup", view=signup, name="signup"),
    path("signin", view=signin, name="signin"),
    path("resend", view=resend_verification_email, name="resend verify email"),
    path(
        "verify-user/<str:token>/",
        view=verify_user,
        name="create_password",
    ),
]
