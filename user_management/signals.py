from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from .models import SchoolAdmin, Teacher


@receiver(post_save, sender=SchoolAdmin)
def assign_school_admin_perms(sender, instance: SchoolAdmin, created: bool, **kwargs):
    if created:

        group, _ = Group.objects.get_or_create(name='SchoolAdmins')
        instance.user.groups.add(group)

        school = instance.school  # Assuming SchoolAdmin has a direct relationship with School
        # Assign object-level permissions related to the School
        assign_perm('user_management.change_school', instance.user, school)
        assign_perm('user_management.delete_school', instance.user, school)
        assign_perm('user_management.view_school', instance.user, school)

        # For managing Teachers specifically at their school
        for teacher in Teacher.objects.filter(school=school):
            assign_perm('user_management.change_teacher', instance.user, teacher)
            assign_perm('user_management.delete_teacher', instance.user, teacher)
            assign_perm('user_management.view_teacher', instance.user, teacher)


@receiver(post_save, sender=Teacher)
def assign_teacher_perms(sender, instance: Teacher, created: bool, **kwargs):
    if created:
        # Assign permissions for self-management
        assign_perm('user_management.change_teacher', instance.user, instance)
        assign_perm('user_management.view_teacher', instance.user, instance)

        for admin in SchoolAdmin.objects.filter(school=instance.school):
            assign_perm('user_management.change_teacher', admin.user, instance)
            assign_perm('user_management.delete_teacher', admin.user, instance)
            assign_perm('user_management.view_teacher', admin.user, instance)
