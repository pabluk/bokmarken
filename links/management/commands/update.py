from django.core.management.base import BaseCommand, CommandError

from links.models import Link


class Command(BaseCommand):
    args = '<link_id link_id ...>'
    help = 'Load title and image for non updated links.'

    def handle(self, *args, **options):
        if args:
            ids = args
        else:
            ids = [link.id for link in Link.objects.filter(is_update=False)]

        for link_id in ids:
            try:
                link = Link.objects.get(pk=int(link_id))
            except Link.DoesNotExist:
                raise CommandError('Link "%s" does not exist' % link_id)
            if not link.is_update:
                link.update()
                link.save()
                self.stdout.write('Successfully updated link "%s"' % link_id)
        self.stdout.write('Done.')
