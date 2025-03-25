from django.shortcuts import get_object_or_404, redirect, render
from ..models import *
from django.utils import timezone
from ..forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정권한이 없습니다")
        return redirect("pybo:detail", question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()  # 수정일시 저장
            answer.save()
            return redirect("pybo:detail", question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {"form": form}
    return render(request, "pybo/answer_form.html", context)


@login_required(login_url="common:login")
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "삭제권한이 없습니다")
        return redirect("pybo:detail", question_id=answer.question.id)
    answer.delete()
    return redirect("pybo:index")


@login_required(login_url="common:login")
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, "본인이 작성한 글은 추천할수 없습니다")
    else:
        answer.voter.add(request.user)
    return redirect("pybo:detail", question_id=answer.question.id)
