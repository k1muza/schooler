from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from guardian.shortcuts import assign_perm

from school_management.models import Class
        