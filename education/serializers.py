from rest_framework import serializers
from education.models import Course, Lesson, Payment, Subscription
from education.validators import DescriptionValidator
from education.utils import create_payment_data, retrieve_payment_data


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


class PaymentCreateSerializer(serializers.ModelSerializer):
    payment_data = serializers.SerializerMethodField()
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"

    def get_payment_data(self, instance):
        if instance.payment_form == "remittance":
            pay = create_payment_data(instance.amount)
            instance.stripe_id = pay["id"]
            instance.status = pay["status"]
            instance.save()
            return pay
        elif instance.payment_form == "cash":
            return ["Payment by cash"]


class PaymentDetailSerializer(serializers.ModelSerializer):
    payment_data = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"

    def get_payment_data(self, instance):
        if instance.stripe_id is not None:
            return retrieve_payment_data(instance.stripe_id)
        else:
            return ["Payment by cash"]
