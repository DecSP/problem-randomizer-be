from django.urls import path

from problem_randomizer_be.users.api.views import LoginView, SignUpView

app_name = "users"
urlpatterns = [
    path("login", view=LoginView.as_view(), name="login"),
    path("signup", view=SignUpView.as_view(), name="signup"),
]
