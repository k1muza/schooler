import pytest
from django.urls import reverse
from school_management.models import Class
from school_management.tests.factories import ClassFactory
from user_management.models import Guardianship
from user_management.tests.factories import GuardianshipFactory, StudentFactory, TeacherFactory, AdministratorFactory, UserFactory


@pytest.mark.django_db
def test_guardian_view_by_associated_student(client):
    student = StudentFactory()
    guardian_user = UserFactory()

    guardianship = GuardianshipFactory(user=student.user, guardian=guardian_user)
    client.force_login(student.user)
    response = client.get(reverse('guardian-detail', args=[str(guardianship.id)]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_guardian_view_by_associated_teacher(client):
    teacher = TeacherFactory()
    student = StudentFactory(school=teacher.school)
    klass: Class = ClassFactory(teacher=teacher, school=teacher.school)
    klass.students.add(student)
    guardian = GuardianshipFactory(user=student.user, guardian=UserFactory())
    client.force_login(teacher.user)
    response = client.get(reverse('guardian-detail', args=[str(guardian.id)]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_guardian_view_by_school_admin(client):
    administrator = AdministratorFactory()
    student = StudentFactory(school=administrator.school)
    guardian = GuardianshipFactory(user=student.user, guardian=UserFactory())
    client.force_login(administrator.user)
    response = client.get(reverse('guardian-detail', args=[str(guardian.id)]))
    assert response.status_code == 200
