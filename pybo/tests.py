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

    # def test_value(self):

    #     resultQuestion = Question.objects.values("subject", "content")
    #     ## SQL 쿼리:
    #     ## SELECT subject, content  FROM Answer;
    #     ## 딕셔너리 형태로 반환
    #     # result = Question.objects.all().values()  # 딕셔너리
    #     # result = Question.objects.all().values_list()  # 튜플
    #     print(resultQuestion)

    #     resultAnswer = Answer.objects.values("id", "question__subject", "content")
    #     # 관련 테입즐 필드 조회(외부키 조회)
    #     # SELECT Answer.id, Question.subject, Answer.content
    #     # FROM Answer
    #     # JOIN Question ON Answer.question_id = Question.id;
    #     print(resultAnswer)
    #     print(resultAnswer.query)

    # def test_filter(self):

    #     # SELECT * FROM Question WHERE id = 1;
    #     # 1. 특정 ID 의 질문 조회
    #     idquery = Question.objects.filter(id=1)
    #     print(idquery.query)

    #     # SELECT * FROM Question WHERE subject = 'Django란?';
    #     # 2. 특정 제목을 가진 질문 조회
    #     subjectquery = Question.objects.filter(subject="Django란?")
    #     print(subjectquery)

    #     # 3. 특정 내용이 포함된 질문 조회(icontains)
    #     # SELECT * FROM Question WHERE content LIKE '%Python%';
    #     contentquery = Question.objects.filter(content__icontains="Python")
    #     print(contentquery)

    #     # 4. 날짜형 조회
    #     # query = Question.objects.filter(create_date)
    #     # print(query)

    #     # SELECT * FROM Question WHERE id < 5;
    #     # 5. 숫자 필터링
    #     # lt: less than
    #     # lte: less than or equals
    #     # gt: greater than
    #     # gte: greater than or equals
    #     idgtquery = Question.objects.filter(id__gt=5)
    #     print(idgtquery)

    #     # 특정 ID 사이의 질문 조회(between)
    #     idrangequery = Question.objects.filter(id__range=(1, 5))
    #     print(idrangequery)

    #     # 2025년 1월 1일과 2025년 3월 14일 사이에 생성된 질문
    #     daterangequery = Question.objects.filter(
    #         create_date__range=("2025-01-01", "2025-03-14")
    #     )
    #     print(daterangequery)

    #     # 제목이 Django란? 이고, 내용에 MTV 가 포함된 질문
    #     qquery = Question.objects.filter(subject="Django란?", content__icontains="MTV")
    #     print(qquery)

    #     # 제목이 'Django란?'이거나 'Python이란?'인 질문 (OR 조건)
    #     from django.db.models import Q

    #     orquery = Question.objects.filter(
    #         Q(subject="Django란?") | Q(subject="Python이란?")
    #     )
    #     print(orquery)

    #     # 정렬
    #     order = Question.objects.order_by("-id").values()
    #     print(order)

    #     # null 처리
    #     nullquery = Question.objects.filter(answer__isnull=False)
    #     print(nullquery)

    #     if Question.objects.filter(subject="Django란?").exists():
    #         print("해당 질문이 존재합니다.")

    #     print("ㄴ------test_filter-----------")

    # annotation @, aggregate
    def test_annotate(self):
        questions = Question.objects.annotate(
            latest_answer_date=Max("answer__create_date")
        )

        for q in questions:
            print("#####")
            print(q.subject, q.latest_answer_date)

        cntquestion = Question.objects.annotate(answer_count=Count("answer"))
        for q in cntquestion:
            print("#####")
            print(q.subject, q.answer_count)

        print("ㄴ------test_annotate-----------")

    def test_aggregate(self):

        # 1. 전체 대답 갯수
        # select count(id) as total_answers from answer
        answer = Answer.objects.aggregate(total_answers=Count("id"))
        # print(answer) #{'total_answers': 5}

        # 2. 전체 질문 개수 구하기
        question = Question.objects.aggregate(total_questions=Count("id"))
        # print(question) #{'total_questions': 5}

        # 3. 전체 답변의 평균 길이 구하기
        # SELECT AVG(LENGTH(content)) AS avg_content_length FROM Answer;
        result = Answer.objects.aggregate(avg_content_length=Avg(Length("content")))
        # print(result)

        # 4.가장 오래된 질문 날짜 구하기(MIN)
        question = Question.objects.aggregate(oldest_questions=Min("create_date"))
        print(question)  # {'total_questions': 5}

        # 5. 전체 답변 글자 수 합계 구하기
        # 6. 가장 긴 질문 길이 구하기

        print("ㄴ------test_aggregate-----------")

    def test_raw(self):
        # raw 함수 다이렉트로 sql 구문을 적을수 있도록 만든함수
        questions = Question.objects.raw("SELECT * FROM pybo_question")
        for question in questions:
            print(question.id, question.subject)

        # 2. 특정 질문 가져오기 (id=1)
        # SELECT * FROM pybo_question WHERE id = 1;
        questions = Question.objects.raw(
            "SELECT * FROM pybo_question where id = %s", [1]
        )
        for q in questions:
            print(q.subject, q.content)

        # 3. 특정 키워드가 포함된 질문 검색
        keyword = "%Django%"
        questions = Question.objects.raw(
            "SELECT * FROM pybo_question WHERE content LIKE %s", [keyword]
        )
        for q in questions:
            print(q.subject)

        # 4. 답변이 가장 많은 질문 가져오기
        questions = Question.objects.raw(
            """
            SELECT q.id, q.subject, COUNT(a.id) AS answer_count
            FROM pybo_question q
            LEFT JOIN pybo_answer a ON q.id = a.question_id
            GROUP BY q.id
            ORDER BY answer_count DESC
            LIMIT 1
            """
        )
        for q in questions:
            print(q.subject, q.answer_count)

        print("ㄴ------test_raw-----------")

    def test_f(self):
        pass

    def test_sum_answer_ids(self):
        """
        Test for Sum aggregation on answer ids
        """
        result = Answer.objects.aggregate(Sum("id"))
        # SQL 쿼리:
        # SELECT SUM(id) FROM Answer;
        print(result)
        self.assertEqual(result["id__sum"], 16)  # AssertionError: 15 != 16
