
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в одну из 10 групп курса.
    """

    if created:
        course = instance.course

        # Создаем 10 групп для курса, если их еще нет
        for i in range(1, 11):
            Group.objects.get_or_create(course=course, group_number=i)

        # Находим группу с наименьшим количеством студентов
        smallest_group = None
        min_size = float('inf')

        for group in Group.objects.filter(course=course):
            group_size = group.students.count()
            if group_size < min_size:
                smallest_group = group
                min_size = group_size

        # Добавляем пользователя в найденную группу
        if smallest_group:
            smallest_group.students.add(instance.user)