from rest_framework import viewsets, generics
from education.models import Course, Lesson, Payment
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from education.permissions import IsOwner, IsStaff, NotStaff
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated & (IsStaff | IsOwner)]

    def perform_create(self, serializer):
        """Функция сохраняет id пользователя, который создает курс, в поле owner"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def list(self, request, *args, **kwargs):
        """Функция позволяет отфильтровать курсы по пользователю"""
        if request.user.is_staff:
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.filter(owner=request.user)
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & NotStaff]

    def perform_create(self, serializer):
        """Функция сохраняет id пользователя, который создает урок, в поле owner"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & (IsStaff | IsOwner)]

    def list(self, request, *args, **kwargs):
        """Функция позволяет отфильтровать курсы по пользователю"""
        if request.user.is_staff:
            queryset = Lesson.objects.all()
        else:
            queryset = Lesson.objects.filter(owner=request.user)
        serializer = LessonSerializer(queryset, many=True)
        return Response(serializer.data)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner & NotStaff]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('course', 'lesson', 'payment_form')
    ordering_fields = ('payment_date',)
    search_fields = ('course', 'lesson',)
    permission_classes = [IsAuthenticated]
