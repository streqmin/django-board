from django.test import TestCase
from django.db.models import Count, Sum, Avg, Min, Max
from django.db.models.functions import Length  # Length를 여기에서 임포트

from django.utils import timezone
from pybo.models import Answer, Question


class AggregateTestCase(TestCase):

    def setUp(self):
        """
        Test setup method to create initial data
        """
        # 질문 3개 생성
        q1 = Question.objects.create(
            subject="Python이란?",
            content="Python은 프로그래밍 언어입니다.",
            create_date=timezone.now(),
        )
        q2 = Question.objects.create(
            subject="Django란?",
            content="Django는 Python 웹 프레임워크입니다.",
            create_date=timezone.now(),
        )
        q3 = Question.objects.create(
            subject="Java란?",
            content="Java는 객체 지향 언어입니다.",
            create_date=timezone.now(),
        )

        # 각 질문에 대한 답변 생성
        Answer.objects.create(
            question=q1,
            content="Python은 매우 유용합니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q1,
            content="Python은 쉽고 강력합니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q2,
            content="Django는 빠르고 확장성이 좋습니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q3,
            content="Java는 크로스 플랫폼에서 사용됩니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q3,
            content="Java는 많은 라이브러리와 도구를 지원합니다.",
            create_date=timezone.now(),
        )

    def test_value(self):

        resultQuestion = Question.objects.values("subject", "content")
        ## SQL 쿼리:
        ## SELECT subject, content  FROM Answer;
        ## 딕셔너리 형태로 반환
        # result = Question.objects.all().values()  # 딕셔너리
        # result = Question.objects.all().values_list()  # 튜플
        print(resultQuestion)

        resultAnswer = Answer.objects.values("id", "question__subject", "content")
        # 관련 테입즐 필드 조회(외부키 조회)
        # SELECT Answer.id, Question.subject, Answer.content
        # FROM Answer
        # JOIN Question ON Answer.question_id = Question.id;
        print(resultAnswer)
        print(resultAnswer.query)

    def test_filter(self):

        # SELECT * FROM Question WHERE id = 1;
        # 1. 특정 ID 의 질문 조회
        idquery = Question.objects.filter(id=1)
        print(idquery.query)

        # SELECT * FROM Question WHERE subject = 'Django란?';
        # 2. 특정 제목을 가진 질문 조회
        subjectquery = Question.objects.filter(subject="Django란?")
        print(subjectquery)

        # 3. 특정 내용이 포함된 질문 조회(icontains)
        # SELECT * FROM Question WHERE content LIKE '%Python%';
        contentquery = Question.objects.filter(content__icontains="Python")
        print(contentquery)

        # 4. 날짜형 조회
        # query = Question.objects.filter(create_date)
        # print(query)

        # SELECT * FROM Question WHERE id < 5;
        # 5. 숫자 필터링
        # lt: less than
        # lte: less than or equals
        # gt: greater than
        # gte: greater than or equals
        idgtquery = Question.objects.filter(id__gt=5)
        print(idgtquery)

        # 특정 ID 사이의 질문 조회(between)
        idrangequery = Question.objects.filter(id__range=(1, 5))
        print(idrangequery)

        # 2025년 1월 1일과 2025년 3월 14일 사이에 생성된 질문
        daterangequery = Question.objects.filter(
            create_date__range=("2025-01-01", "2025-03-14")
        )
        print(daterangequery)

        # 제목이 Django란? 이고, 내용에 MTV 가 포함된 질문
        qquery = Question.objects.filter(subject="Django란?", content__icontains="MTV")
        print(qquery)

        # 제목이 'Django란?'이거나 'Python이란?'인 질문 (OR 조건)
        from django.db.models import Q

        orquery = Question.objects.filter(
            Q(subject="Django란?") | Q(subject="Python이란?")
        )
        print(orquery)

        # 정렬
        order = Question.objects.order_by("-id").values()
        print(order)

        # null 처리
        nullquery = Question.objects.filter(answer__isnull=False)
        print(nullquery)

        if Question.objects.filter(subject="Django란?").exists():
            print("해당 질문이 존재합니다.")

        print("ㄴ------test_filter-----------")

    # annotation @, aggregate
    def test_annotate(self):
        pass

    def test_aggregate(self):
        pass
