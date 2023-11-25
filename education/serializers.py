from rest_framework import serializers
from education.models import Course, Lesson, Payment, Subscription
from education.validators import DescriptionValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [DescriptionValidator(field='description'),
                      DescriptionValidator(field='link_to_video')]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [serializers.UniqueTogetherValidator(fields=['student', 'course'],
                                                          queryset=Subscription.objects.all())]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription_status = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj.pk).count()

    def get_subscription_status(self, obj):
        if Subscription.objects.filter(course=obj.pk, student=obj.owner).count() > 0:
            return True

    class Meta:
        model = Course
        fields = '__all__'
        validators = [DescriptionValidator(field='description')]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
