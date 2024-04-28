from typing import Iterable
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from school_management.models import Class

from .models import Guardian, SchoolAdmin, Student, Teacher


def assign_global_permissions_schooladmin(group: Group):
    assign_perm('user_management.add_schooladmin', group)
    assign_perm('user_management.add_teacher', group)
    assign_perm('user_management.add_student', group)
    assign_perm('user_management.add_guardian', group)
    assign_perm('school_management.add_school', group)


def assign_global_permissions_teacher(group: Group):
    assign_perm('user_management.add_teacher', group)
    assign_perm('user_management.add_student', group)
    assign_perm('user_management.add_guardian', group)


def assign_global_permissions_student(group: Group):
    assign_perm('user_management.add_student', group)
    assign_perm('user_management.add_guardian', group)


@receiver(post_save, sender=SchoolAdmin)
def assign_school_admin_perms(sender, instance: SchoolAdmin, created: bool, **kwargs):
    if created:

        group, new_group = Group.objects.get_or_create(name='SchoolAdmins')

        if new_group:
            assign_global_permissions_schooladmin(group)

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

        for admin in SchoolAdmin.objects.filter(school=instance.school):
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
        assign_perm('school_management.view_school', instance.user, instance.school)

        for admins in SchoolAdmin.objects.filter(school=instance.school):
            assign_perm('user_management.view_student', admins.user, instance)
            assign_perm('user_management.change_student', admins.user, instance)
            assign_perm('user_management.delete_student', admins.user, instance)


@receiver(m2m_changed, sender=Guardian.students.through)
def assign_guardian_perms(sender, instance: Guardian, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        students: Iterable[Student] = instance.students.filter(pk__in=pk_set)
        for student in students:
            assign_perm('user_management.view_student', instance.user, student)
            assign_perm('school_management.view_school', instance.user, student.school)
            assign_perm('user_management.view_guardian', student.user, instance)
            
            for teacher in student.teachers.all():
                assign_perm('user_management.view_teacher', instance.user, teacher)
                assign_perm('user_management.view_guardian', teacher.user, instance)

            for school_admin in SchoolAdmin.objects.filter(school=student.school):
                assign_perm('user_management.view_guardian', school_admin.user, instance)


@receiver(m2m_changed, sender=Class.students.through)
def assign_student_perms(sender, instance: Class, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        students: Iterable[Student] = instance.students.filter(pk__in=pk_set)
        for student in students:
            assign_perm('user_management.view_student', student.user, student)
            assign_perm('user_management.view_student', instance.teacher.user, student)
            assign_perm('user_management.change_student', instance.teacher.user, student)
            assign_perm('user_management.view_teacher', student.user, instance.teacher)
