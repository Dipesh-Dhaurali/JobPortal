from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from candidate.models import CandidateAccount


class Command(BaseCommand):
    help = 'Create CandidateAccount records for users who do not have them'

    def handle(self, *args, **options):
        """Create CandidateAccount for all users without one"""
        users_without_account = User.objects.filter(candidate_account__isnull=True)
        
        if not users_without_account.exists():
            self.stdout.write(self.style.SUCCESS('All users already have CandidateAccount records!'))
            return
        
        created_count = 0
        for user in users_without_account:
            CandidateAccount.objects.create(user=user, account_status='active')
            created_count += 1
            self.stdout.write(f'Created CandidateAccount for {user.username}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} CandidateAccount record(s)!'))
