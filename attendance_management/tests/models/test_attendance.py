from django.db import DataError
import pytest
from attendance_management.models import ClassAttendance
from attendance_management.tests.factories import ClassAttendanceFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_class_attendance():
    attendance = ClassAttendanceFactory()
    assert attendance.status == ClassAttendance.Status.PRESENT


@pytest.mark.django_db
@pytest.mark.models
def test_read_class_attendance():
    attendance = ClassAttendanceFactory()
    retrieved_attendance = ClassAttendance.objects.get(pk=attendance.pk)
    assert retrieved_attendance == attendance


@pytest.mark.django_db
@pytest.mark.models
def test_update_class_attendance():
    attendance = ClassAttendanceFactory()
    new_status = ClassAttendance.Status.ABSENT
    attendance.status = new_status
    attendance.save()
    retrieved_attendance = ClassAttendance.objects.get(pk=attendance.pk)
    assert retrieved_attendance.status == new_status


@pytest.mark.django_db
@pytest.mark.models
def test_delete_class_attendance():
    attendance = ClassAttendanceFactory()
    attendance.delete()
    assert ClassAttendance.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.models
def test_class_attendance_str():
    attendance = ClassAttendanceFactory()
    assert str(attendance) == f'{attendance.student} - {attendance.classroom} - {attendance.attendance_date}'


@pytest.mark.django_db
@pytest.mark.models
def test_invalid_status():
    with pytest.raises(DataError):
        ClassAttendanceFactory(status='InvalidStatus')
