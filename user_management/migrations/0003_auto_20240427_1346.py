from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_groups_and_permissions(apps, schema_editor):
    Student = apps.get_model('user_management', 'Student')

    teachers, _ = Group.objects.get_or_create(name='Teachers')

    student_content_type = ContentType.objects.get_for_model(Student)

    permissions = [
        ('add_student', 'Can add student'),
        ('change_student', 'Can change student'),
        ('delete_student', 'Can delete student'),
        ('view_student', 'Can view student'),
    ]

    for codename, name in permissions:
        perm, _ = Permission.objects.get_or_create(
            codename=codename,
            content_type=student_content_type,
            defaults={
                'name': name
            }
        )
        teachers.permissions.add(perm)


def remove_groups_and_permissions(apps, schema_editor):
    Group.objects.filter(name='Teachers').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_auto_20240427_1209'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, remove_groups_and_permissions),
    ]
