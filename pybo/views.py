from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth.decorators import login_required


def index(request):
    print(request.user)
    page = request.GET.get("page", "1")

    question_list = Question.objects.order_by("-create_date")

    paginator = Paginator(question_list, 10)  # 페이지 당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {"question_list": page_obj}
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)

    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)


@login_required(login_url="common:login")
def answer_create(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    print("request.method: ", request.method)

    if request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question_id)
    else:
        form = AnswerForm()

    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)


@login_required(login_url="common:login")
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")

    else:
        form = QuestionForm()

    return render(request, "pybo/question_form.html", {"form": form})


def set_cookie_view(request):
    response = HttpResponse("쿠키가 설정되었습니다.")
    response.set_cookie("my_cookie", "cookie_value", max_age=3600)
    return response


def get_cookie_view(request):
    cookie_value = request.COOKIES.get("my_cookie", "쿠키가 없습니다.")
    return HttpResponse(f"쿠키값: {cookie_value}")


def delete_cookie_view(request):
    response = HttpResponse("쿠키가 삭제되었습니다.")
    response.delete_cookie("my_cookie")
    return response


def set_session_view(request):
    request.session["username"] = "Django"
    request.session.set_expiry(3600)
    return HttpResponse("세션이 설정되었습니다.")


def get_session_view(request):
    from django.contrib.sessions.models import Session
    from django.contrib.sessions.backends.db import SessionStore

    # 특정 세션 키 조회
    session_key = "5q3z6qx9qjod0j4b9yienf3p1t7m5ywb"  # 실제 저장된 session_key 입력
    session = Session.objects.get(session_key=session_key)

    # 세션 데이터 복호화
    session_data = SessionStore(session_key=session_key).load()
    print(session_data)  # {'username': 'DjangoUser'}

    username = request.session.get("username", "세션이 없습니다.")
    return HttpResponse(f"세션값: {username}")


def delete_session_view(request):
    request.session.flush()
    return HttpResponse("세션이 삭제되었습니다.")
