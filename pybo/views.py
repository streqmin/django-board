from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import *
from django.utils import timezone
from .forms import *


def index(request):
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


def answer_create(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    print("request.method: ", request.method)

    if request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question_id)
    else:
        return HttpResponseNotAllowed("only post id available")

    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)


def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")

    else:
        form = QuestionForm()

    return render(request, "pybo/question_form.html", {"form": form})
