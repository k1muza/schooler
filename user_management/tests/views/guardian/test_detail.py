import pytest
from django.urls import reverse
from school_management.models import Class
from school_management.tests.factories import ClassFactory
from user_management.tests.factories import GuardianFactory, StudentFactory, TeacherFactory, SchoolAdminFactory


@pytest.mark.django_db
def test_guardian_view_by_associated_student(client):
    student = StudentFactory()
    client.force_login(student.user)
    guardian = GuardianFactory()
    guardian.students.add(student)
    response = client.get(reverse('guardian-detail', args=[str(guardian.id)]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_guardian_view_by_associated_teacher(client):
    teacher = TeacherFactory()
    student = StudentFactory(school=teacher.school)
    klass: Class = ClassFactory(teacher=teacher, school=teacher.school)
    klass.students.add(student)
    guardian = GuardianFactory()
    guardian.students.add(student)
    client.force_login(teacher.user)
    response = client.get(reverse('guardian-detail', args=[str(guardian.id)]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_guardian_view_by_school_admin(client):
    school_admin = SchoolAdminFactory()
    student = StudentFactory(school=school_admin.school)
    guardian = GuardianFactory()
    guardian.students.add(student)
    client.force_login(school_admin.user)
    response = client.get(reverse('guardian-detail', args=[str(guardian.id)]))
    assert response.status_code == 200
