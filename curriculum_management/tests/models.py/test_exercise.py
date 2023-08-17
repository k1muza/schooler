from curriculum_management.models import Exercise
from curriculum_management.tests.factories import ExerciseFactory, SubjectFactory
import pytest
from school_management.tests.factories import ClassRoomFactory
from user_management.tests.factories import StudentFactory, TeacherFactory


@pytest.mark.django_db
def test_create_exercise():
    students = [StudentFactory() for _ in range(3)]
    exercise = ExerciseFactory(taken_by=students)

    assert Exercise.objects.count() == 1
    assert exercise.taken_by.count() == 3

@pytest.mark.django_db
def test_read_exercise():
    exercise = ExerciseFactory()
    retrieved_exercise = Exercise.objects.get(pk=exercise.id)
    assert retrieved_exercise == exercise

@pytest.mark.django_db
def test_update_exercise():
    exercise = ExerciseFactory(title="Original Title")
    exercise.title = "Updated Title"
    exercise.save()

    # Verifying the update
    updated_exercise = Exercise.objects.get(pk=exercise.id)
    assert updated_exercise.title == "Updated Title"

@pytest.mark.django_db
def test_delete_exercise():
    # Creating an Exercise
    exercise = ExerciseFactory()

    # Deleting the Exercise
    exercise.delete()

    # Verifying the deletion
    assert Exercise.objects.count() == 0
