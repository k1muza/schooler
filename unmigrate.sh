#!/bin/bash

# List all the apps with migrations
apps=(
    "user_management" "school_management" "exam_management" "curriculum_management" "attendance_management")

# Roll back all migrations for the listed apps
for app in "${apps[@]}"; do
   python manage.py migrate $app zero
done
