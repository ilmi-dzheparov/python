from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=4)
        group, create = Group.objects.get_or_create(name="profile_manager")
        permission_profile = Permission.objects.get(codename="view_profile")
        permission_logentry = Permission.objects.get(codename="view_logentry")
        # Add hprmission to group
        group.permissions.add(permission_profile)
        # Add group to user
        user.groups.add(group)
        # Add permission to user
        user.user_permissions.add(permission_logentry)
        group.save()
        user.save()