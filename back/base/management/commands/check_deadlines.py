from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models import Assignment, UserAssignment, AssignmentStatus
import logging

class Command(BaseCommand):
    help = 'Check all assignments for deadlines and update status if past due date'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        try:
            past_due_status = AssignmentStatus.objects.get(status="Past Due Date")
            submitted_status = AssignmentStatus.objects.get(status="Submitted")
        except AssignmentStatus.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            return

        # Get all assignments with deadlines that have passed
        assignments = Assignment.objects.filter(deadline__lt=now)

        for assignment in assignments:
            # Get all user assignments for this assignment that are not submitted
            user_assignments = UserAssignment.objects.filter(assignment=assignment).exclude(status=submitted_status)

            for user_assignment in user_assignments:
                user_assignment.status = past_due_status
                user_assignment.save()
                logging.info(f'Updated assignment {user_assignment.assignment.id} for user {user_assignment.user.id} to past due status.')

        self.stdout.write(self.style.SUCCESS('Successfully checked and updated assignment deadlines'))