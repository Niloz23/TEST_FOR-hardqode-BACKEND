from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import Balance, Subscription
from courses.models import Course



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_payment(request):
    user = request.user
    course_id = request.data.get('course_id')

    if not course_id:
        return Response({"detail": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.objects.get(id=course_id, is_available=True)
    except Course.DoesNotExist:
        return Response({"detail": "Course not found or not available."}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, есть ли у пользователя достаточно бонусов
    cost = float(course.cost)
    if user.balance.amount < cost:
        return Response({"detail": "Not enough bonus points to purchase this course."}, status=status.HTTP_400_BAD_REQUEST)

    # Проверяем, не куплен ли уже курс
    if Subscription.objects.filter(user=user, course=course).exists():
        return Response({"detail": "You are already subscribed to this course."}, status=status.HTTP_400_BAD_REQUEST)

    # Списываем бонусы
    user.balance.amount -= cost
    user.balance.save()

    # Создаем подписку на курс
    Subscription.objects.create(user=user, course=course)

    return Response({"detail": "Payment successful and subscription created."}, status=status.HTTP_201_CREATED)

class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.groups.filter(name='students').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.groups.filter(name='students').exists()

class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
