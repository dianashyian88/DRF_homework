from education.apps import EducationConfig
from rest_framework.routers import DefaultRouter
from education.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, \
    LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, \
    SubscriptionCreateAPIView, SubscriptionDestroyAPIView, PaymentCreateAPIView, PaymentDetailAPIView
from django.urls import path

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment_detail'),
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),

] + router.urls

