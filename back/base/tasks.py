from celery import shared_task
from django.utils import timezone
from base.models import Assignment, UserAssignment, AssignmentStatus

@shared_task
def check_deadlines():
    now = timezone.now()
    try:
        past_due_status = AssignmentStatus.objects.get(status="Past Due Date")
        submitted_status = AssignmentStatus.objects.get(status="Submitted")
    except AssignmentStatus.DoesNotExist as e:
        print(f'Error: {e}')
        return

    assignments = Assignment.objects.filter(deadline__lt=now)

    for assignment in assignments:
        user_assignments = UserAssignment.objects.filter(assignment=assignment).exclude(status=submitted_status)

        for user_assignment in user_assignments:
            user_assignment.status = past_due_status
            user_assignment.save()