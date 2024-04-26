from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups_and_permissions(apps, schema_editor):
    # Use historical models to ensure compatibility
    Teacher = apps.get_model('user_management', 'Teacher')

    # Create or get the SchoolAdmin group
    school_admin_group, _ = Group.objects.get_or_create(name='SchoolAdmins')

    # Get content type for the Teacher model
    teacher_content_type = ContentType.objects.get_for_model(Teacher)

    # Define permissions for SchoolAdmins
    permissions = [
        ('add_teacher', 'Can add teacher'),
        ('change_teacher', 'Can change teacher'),
        ('delete_teacher', 'Can delete teacher'),
        ('view_teacher', 'Can view teacher'),
    ]

    for codename, name in permissions:
        perm, _ = Permission.objects.get_or_create(
            codename=codename,
            content_type=teacher_content_type,
            defaults={
                'name': name
            }
        )
        school_admin_group.permissions.add(perm)

def remove_groups_and_permissions(apps, schema_editor):
    Group.objects.filter(name='SchoolAdmins').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0005_alter_guardian_students'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, remove_groups_and_permissions),
    ]
