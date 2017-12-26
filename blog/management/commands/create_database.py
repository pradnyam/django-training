from django.core.management.base import BaseCommand, CommandError
from blog.models import Base, engine
import sqlalchemy

class Command(BaseCommand):
    help = 'Create database tables'

    def handle(self, *args, **options):
        try:
            Base.metadata.create_all(engine)
            print("Tables are created!")
        except:
            raise CommandError('Error occurred while creating database tables')
