import pytest
from datetime import datetime
from django.contrib import admin
from school_management.tests.factories import ClassRoomFactory
from user_management.models import Enrolment
from user_management.tests.factories import EnrolmentFactory, StudentFactory


@pytest.mark.django_db
def test_create_enrolment():
    student = StudentFactory()
    classroom = ClassRoomFactory()
    enrolment = Enrolment.objects.create(student=student, 
                                         classroom=classroom, 
                                         status=Enrolment.Status.ENROLLED,
                                         enrolment_date=datetime.now())
    assert enrolment.student == student
    assert enrolment.classroom == classroom
    assert enrolment.status == Enrolment.Status.ENROLLED


@pytest.mark.django_db
def test_read_enrolment():
    enrolment = EnrolmentFactory()
    retrieved_enrolment = Enrolment.objects.get(id=enrolment.id)
    assert retrieved_enrolment == enrolment


@pytest.mark.django_db
def test_update_enrolment():
    enrolment = EnrolmentFactory(status=Enrolment.Status.ENROLLED)
    enrolment.status = Enrolment.Status.WITHDRAWN
    enrolment.save()
    updated_enrolment = Enrolment.objects.get(id=enrolment.id)
    assert updated_enrolment.status == Enrolment.Status.WITHDRAWN


@pytest.mark.django_db
def test_delete_enrolment():
    enrolment = EnrolmentFactory()
    enrolment_id = enrolment.id
    enrolment.delete()
    with pytest.raises(Enrolment.DoesNotExist):
        Enrolment.objects.get(id=enrolment_id)


@pytest.mark.django_db
def test_enrolment_student_classroom_relation():
    student = StudentFactory()
    classroom = ClassRoomFactory()
    enrolment = EnrolmentFactory(student=student, classroom=classroom)
    assert enrolment.student == student
    assert enrolment in classroom.enrolments.all()


@pytest.mark.django_db
def test_enrolment_str():
    enrolment = EnrolmentFactory()
    assert str(enrolment) == str(enrolment.student.user)


def test_enrolment_admin_registration():
    assert admin.site._registry.get(Enrolment) is not None, 'Enrolment is not registered in the admin site'
