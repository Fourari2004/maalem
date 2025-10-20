from django.core.management.base import BaseCommand
from maalem.users.models import User

class Command(BaseCommand):
    help = 'Clean up duplicate users'

    def handle(self, *args, **options):
        # Get all users with the same email
        users = User.objects.filter(email="test@example.com")
        
        if users.count() > 2:
            self.stdout.write(f"Found {users.count()} users with email test@example.com")
            
            # Keep only the client and artisan users
            client_users = users.filter(user_type="client")
            artisan_users = users.filter(user_type="artisan")
            
            if client_users.count() > 1:
                # Keep the first one and delete the rest
                client_to_keep = client_users.first()
                client_to_delete = client_users.exclude(id=client_to_keep.id)
                self.stdout.write(f"Deleting {client_to_delete.count()} duplicate client users")
                client_to_delete.delete()
                
            if artisan_users.count() > 1:
                # Keep the first one and delete the rest
                artisan_to_keep = artisan_users.first()
                artisan_to_delete = artisan_users.exclude(id=artisan_to_keep.id)
                self.stdout.write(f"Deleting {artisan_to_delete.count()} duplicate artisan users")
                artisan_to_delete.delete()
                
            self.stdout.write("Cleanup completed")
        else:
            self.stdout.write("No duplicate users found")