from django.urls import include, path
from .views import base_views, question_views, answer_views

app_name = "pybo"

urlpatterns = [
    path("", base_views.index, name="index"),
    # http://127.0.0.1:8000/pybo/<int:question_id>/
    path("<int:question_id>/", base_views.detail, name="detail"),
    path(
        "answer/create/<int:question_id>/",
        answer_views.answer_create,
        name="answer_create",
    ),
    path("question/create/", question_views.question_create, name="question_create"),
    # path("set-cookie/", views.set_cookie_view, name="set_cookie"),
    # path("get-cookie/", views.get_cookie_view, name="get_cookie"),
    # path("delete-cookie/", views.delete_cookie_view, name="delete_cookie"),
    # path("set-session/", views.set_session_view, name="set_session"),
    # path("get-session/", views.get_session_view, name="get_session"),
    # path("delete-session/", views.delete_session_view, name="delete_session"),
    path(
        "question/modify/<int:question_id>/",
        question_views.question_modify,
        name="question_modify",
    ),
    path(
        "answer/modify/<int:answer_id>/",
        answer_views.answer_modify,
        name="answer_modify",
    ),
    path(
        "question/delete/<int:question_id>/",
        question_views.question_delete,
        name="question_delete",
    ),
    path(
        "answer/delete/<int:answer_id>/",
        answer_views.answer_delete,
        name="answer_delete",
    ),
    path(
        "question/vote/<int:question_id>/",
        question_views.question_vote,
        name="question_vote",
    ),
    path("answer/vote/<int:answer_id>/", answer_views.answer_vote, name="answer_vote"),
]
