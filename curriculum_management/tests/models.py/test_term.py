import pytest
import datetime
from django.contrib import admin
from curriculum_management.models import Term
from curriculum_management.tests.factories import TermFactory
from django.db.utils import IntegrityError

@pytest.mark.django_db
def test_create_term():
    term = TermFactory()
    assert Term.objects.count() == 1
    assert term.name == Term.objects.first().name

@pytest.mark.django_db
def test_read_term():
    term = TermFactory()
    retrieved_term = Term.objects.get(pk=term.pk)
    assert retrieved_term == term

@pytest.mark.django_db
def test_update_term():
    term = TermFactory()
    new_name = "Spring Term"
    term.name = new_name
    term.save()
    retrieved_term = Term.objects.get(pk=term.pk)
    assert retrieved_term.name == new_name

@pytest.mark.django_db
def test_delete_term():
    term = TermFactory()
    term.delete()
    assert Term.objects.count() == 0

@pytest.mark.django_db
def test_term_start_date_before_end_date():
    term = TermFactory.build()
    term.end_date = term.start_date - datetime.timedelta(days=1)
    with pytest.raises(IntegrityError):
        term.save()

def test_term_admin_registration():
    assert admin.site._registry.get(Term) is not None, 'Term is not registered in the admin site'
