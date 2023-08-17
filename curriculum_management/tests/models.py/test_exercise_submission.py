import pytest
from curriculum_management.tests.factories import ExerciseSubmissionFactory
from curriculum_management.models import ExerciseSubmission


@pytest.mark.django_db
def test_create_exercise_submission():
    submission = ExerciseSubmissionFactory()
    assert submission.id is not None

@pytest.mark.django_db
def test_read_exercise_submission():
    submission = ExerciseSubmissionFactory()
    fetched_submission = ExerciseSubmission.objects.get(pk=submission.id)
    assert submission == fetched_submission

@pytest.mark.django_db
def test_update_exercise_submission():
    submission = ExerciseSubmissionFactory()
    new_score = 90
    submission.score = new_score
    submission.save()
    updated_submission = ExerciseSubmission.objects.get(pk=submission.id)
    assert updated_submission.score == new_score

@pytest.mark.django_db
def test_delete_exercise_submission():
    submission = ExerciseSubmissionFactory()
    submission_id = submission.id
    submission.delete()
    with pytest.raises(ExerciseSubmission.DoesNotExist):
        ExerciseSubmission.objects.get(pk=submission_id)
