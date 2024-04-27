from django.contrib.auth.models import Group
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from school_management.models import Class

from .models import Guardian, SchoolAdmin, Student, Teacher


@receiver(post_save, sender=SchoolAdmin)
def assign_school_admin_perms(sender, instance: SchoolAdmin, created: bool, **kwargs):
    if created:

        group, _ = Group.objects.get_or_create(name='SchoolAdmins')
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

        group, _ = Group.objects.get_or_create(name='Teachers')
        instance.user.groups.add(group)
        # Assign permissions for self-management
        assign_perm('user_management.change_teacher', instance.user, instance)
        assign_perm('user_management.view_teacher', instance.user, instance)
        assign_perm('school_management.view_school', instance.user, instance.school)

        for admin in SchoolAdmin.objects.filter(school=instance.school):
            assign_perm('user_management.change_teacher', admin.user, instance)
            assign_perm('user_management.delete_teacher', admin.user, instance)
            assign_perm('user_management.view_teacher', admin.user, instance)

        # Students to access their teacher
        for student in instance.students.all():
            assign_perm('user_management.view_teacher', student.user, instance)
            for guardian in student.guardians.all():
                assign_perm('user_management.view_teacher', guardian.user, instance)


@receiver(post_save, sender=Student)
def assign_student_perms(sender, instance: Student, created: bool, **kwargs):
    if created:
        assign_perm('user_management.view_student', instance.user, instance)
        assign_perm('school_management.view_school', instance.user, instance.school)

        for teacher in instance.teachers.all():
            assign_perm('user_management.view_teacher', instance.user, teacher)

        for admins in SchoolAdmin.objects.filter(school=instance.school):
            assign_perm('user_management.view_student', admins.user, instance)
            assign_perm('user_management.change_student', admins.user, instance)
            assign_perm('user_management.delete_student', admins.user, instance)


@receiver(m2m_changed, sender=Guardian.students.through)
def assign_guardian_perms(sender, instance: Guardian, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        for student in instance.students.all():
            assign_perm('user_management.view_student', instance.user, student)
            assign_perm('school_management.view_school', instance.user, student.school)
            
        for teacher in instance.teachers.all():
            assign_perm('user_management.view_teacher', instance.user, teacher)


@receiver(m2m_changed, sender=Class.students.through)
def assign_student_perms(sender, instance: Class, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        for student in instance.students.all():
            assign_perm('user_management.view_student', student.user, student)
            assign_perm('user_management.view_student', instance.teacher.user, student)
            assign_perm('user_management.view_teacher', student.user, instance.teacher)
