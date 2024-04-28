from typing import Iterable
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from school_management.models import Class

from .models import Guardianship, Administrator, Student, Teacher


def assign_global_permissions_administrator(group: Group):
    assign_perm('user_management.add_administrator', group)
    assign_perm('user_management.add_teacher', group)
    assign_perm('user_management.add_student', group)
    assign_perm('user_management.add_guardianship', group)
    assign_perm('school_management.add_school', group)


def assign_global_permissions_teacher(group: Group):
    assign_perm('user_management.add_teacher', group)
    assign_perm('user_management.add_student', group)
    assign_perm('user_management.add_guardianship', group)


def assign_global_permissions_student(group: Group):
    assign_perm('user_management.add_student', group)
    assign_perm('user_management.add_guardianship', group)


@receiver(post_save, sender=Administrator)
def assign_school_admin_perms(sender, instance: Administrator, created: bool, **kwargs):
    if created:

        group, new_group = Group.objects.get_or_create(name='Administrators')

        if new_group:
            assign_global_permissions_administrator(group)

        instance.user.groups.add(group)

        # Assign object-level permissions related to the School
        assign_perm('school_management.change_school', instance.user, instance.school)
        assign_perm('school_management.delete_school', instance.user, instance.school)
        assign_perm('school_management.view_school', instance.user, instance.school)

        # For managing Teachers specifically at their school
        for teacher in Teacher.objects.filter(school=instance.school):
            assign_perm('user_management.change_teacher', instance.user, teacher)
            assign_perm('user_management.delete_teacher', instance.user, teacher)
            assign_perm('user_management.view_teacher', instance.user, teacher)

        for student in Student.objects.filter(school=instance.school):
            assign_perm('user_management.change_student', instance.user, student)
            assign_perm('user_management.delete_student', instance.user, student)
            assign_perm('user_management.view_student', instance.user, student)


@receiver(post_save, sender=Teacher)
def assign_teacher_perms(sender, instance: Teacher, created: bool, **kwargs):
    if created:

        group, new_group = Group.objects.get_or_create(name='Teachers')

        if new_group:
            assign_global_permissions_teacher(group)

        instance.user.groups.add(group)
        # Assign permissions for self-management
        assign_perm('user_management.change_teacher', instance.user, instance)
        assign_perm('user_management.view_teacher', instance.user, instance)
        assign_perm('school_management.view_school', instance.user, instance.school)

        for admin in Administrator.objects.filter(school=instance.school):
            assign_perm('user_management.change_teacher', admin.user, instance)
            assign_perm('user_management.delete_teacher', admin.user, instance)
            assign_perm('user_management.view_teacher', admin.user, instance)


@receiver(post_save, sender=Student)
def assign_student_perms(sender, instance: Student, created: bool, **kwargs):
    if created:

        group, new_group = Group.objects.get_or_create(name='Students')

        if new_group:
            assign_global_permissions_student(group)

        assign_perm('user_management.view_student', instance.user, instance)
        assign_perm('user_management.change_student', instance.user, instance)
        assign_perm('school_management.view_school', instance.user, instance.school)

        for admins in Administrator.objects.filter(school=instance.school):
            assign_perm('user_management.view_student', admins.user, instance)
            assign_perm('user_management.change_student', admins.user, instance)
            assign_perm('user_management.delete_student', admins.user, instance)


@receiver(post_save, sender=Guardianship)
def assign_guardian_perms(sender, instance: Guardianship, created, **kwargs):
    # Create permissions
    if created:
        assign_perm('user_management.view_guardianship', instance.user, instance)
        assign_perm('user_management.change_guardianship', instance.user, instance)
        assign_perm('user_management.delete_guardianship', instance.user, instance)

        # Assign permissions for viewing students
        for student in instance.user.studentships.all():
            assign_perm('user_management.view_student', instance.guardian, student)

        # Assign permissions for viewing teachers
        for teacher in instance.user.teachers.all():
            assign_perm('user_management.view_guardianship', teacher.user, instance)

        # Assign permissions for viewing administrators
        for admin in instance.user.administrators.all():
            assign_perm('user_management.view_guardianship', admin.user, instance)

        # Assign permissions for viewing schools
        for school in instance.user.schools.all():
            assign_perm('user_management.view_school', instance.guardian, school)


@receiver(m2m_changed, sender=Class.students.through)
def assign_student_perms(sender, instance: Class, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        students: Iterable[Student] = instance.students.filter(pk__in=pk_set)
        for student in students:
            assign_perm('user_management.view_student', student.user, student)
            assign_perm('user_management.view_student', instance.teacher.user, student)
            assign_perm('user_management.change_student', instance.teacher.user, student)
            assign_perm('user_management.view_teacher', student.user, instance.teacher)

            for guardian_user in student.user.guardians.all():
                assign_perm('user_management.view_teacher', guardian_user, instance.teacher)
