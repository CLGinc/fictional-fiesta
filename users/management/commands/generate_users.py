import time
import logging

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            default=10,
            type=int,
            help='Number of users. Default: 10')

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        logger = logging.getLogger('django')
        users_to_create = list()
        if verbosity > 0:
            start_time = time.time()
            logger.info('Start generating users')
        latest_user_id = User.objects.latest('id').id
        for user_idx in range(options['users']):
            users_to_create.append(
                User(
                    username='gen.user{}@google.com'.format(
                        user_idx + latest_user_id + 1),
                    password='gen.user{}'.format(user_idx + latest_user_id + 1),
                    email='gen.user{}@google.com'.format(
                        user_idx + latest_user_id + 1),
                    first_name='Generated User',
                    last_name=str(user_idx + latest_user_id + 1)
                )
            )
            if verbosity > 2:
                logger.info('Generated User {}.'.format(user_idx))

        # Write objects to db
        if verbosity > 1:
            logger.info('Writing users to database.')
        User.objects.bulk_create(users_to_create)
        if verbosity > 1:
            logger.info('All users written to database.')

        if verbosity > 0:
            execution_time = time.time() - start_time
            logger.info(
                "Finished! Generated {} in {:0.2f} seconds!".format(
                    options['users'],
                    execution_time
                )
            )
