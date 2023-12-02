from rest_framework import viewsets, generics
from education.models import Course, Lesson, Payment, Subscription
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, \
    SubscriptionSerializer, PaymentCreateSerializer, PaymentDetailSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from education.permissions import IsOwner, IsStaff, NotStaff
from education.pagination import EducationPaginator
from education.tasks import send_mail_update_course


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курсов"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated & (IsStaff | IsOwner)]
    pagination_class = EducationPaginator

    def perform_create(self, serializer):
        """Функция сохраняет id пользователя, который создает курс, в поле owner"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def list(self, request, *args, **kwargs):
        """Функция позволяет отфильтровать курсы по пользователю и выводить данные постранично"""
        if request.user.is_staff:
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.filter(owner=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_update(self, serializer):
        """Функция вызывает отложенную задачу по отправке уведомлений об обновлении курса"""
        update_course = serializer.save()
        update_course.save()
        send_mail_update_course.delay(update_course.id)


class LessonCreateAPIView(generics.CreateAPIView):
    """Эндпойнт создания урока"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & NotStaff]

    def perform_create(self, serializer):
        """Функция сохраняет id пользователя, который создает урок, в поле owner,
        а также вызывает отложенную задачу по отправке уведомлений об обновлении курса"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson.course is not None:
            send_mail_update_course.delay(new_lesson.course_id)


class LessonListAPIView(generics.ListAPIView):
    """Эндпойнт выведения списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & (IsStaff | IsOwner)]
    pagination_class = EducationPaginator

    def list(self, request, *args, **kwargs):
        """Функция позволяет отфильтровать курсы по пользователю и выводить данные постранично"""
        if request.user.is_staff:
            queryset = Lesson.objects.all()
        else:
            queryset = Lesson.objects.filter(owner=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпойнт выведения информации об одном уроке"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Эндпойнт обновления урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsOwner]

    def perform_update(self, serializer):
        """Функция вызывает отложенную задачу по отправке уведомлений об обновлении курса"""
        update_lesson = serializer.save()
        update_lesson.save()
        if update_lesson.course is not None:
            send_mail_update_course.delay(update_lesson.course_id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Эндпойнт удаления урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner & NotStaff]


class PaymentListAPIView(generics.ListAPIView):
    """Эндпойнт выведения информации о платежах"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('course', 'lesson', 'payment_form')
    ordering_fields = ('payment_date',)
    search_fields = ('course', 'lesson',)
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Эндпойнт создания платежа"""
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Функция сохраняет цену курса/урока в поле amount"""
        pay = serializer.save()
        if pay.course is not None:
            pay.amount = Course.objects.get(pk=pay.course.pk).price
        if pay.lesson is not None:
            pay.amount = Lesson.objects.get(pk=pay.lesson.pk).price
        pay.save()


class PaymentDetailAPIView(generics.RetrieveAPIView):
    """Эндпойнт получения информации о платеже"""
    serializer_class = PaymentDetailSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Эндпойнт создания подписки на обновления курса"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Функция сохраняет id пользователя, который оформляет подписку, в поле student"""
        new_subscription = serializer.save()
        new_subscription.student = self.request.user
        new_subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Эндпойнт удаления подписки на обновления курса"""
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
