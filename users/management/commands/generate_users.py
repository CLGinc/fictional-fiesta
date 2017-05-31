import time
import logging

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-r',
            '--users',
            default=10,
            type=int,
            help='Number of users. Default: 10')

    def handle(self, *args, **options):
        start_time = time.time()
        logger = logging.getLogger('django')
        logger.info('Start generating users')
        latest_user_id = User.objects.latest('id').id
        for user_idx in range(options['users']):
            User.objects.create_user(
                username='user{}@google.com'.format(
                    user_idx + latest_user_id + 1),
                password='user{}'.format(user_idx + latest_user_id + 1),
                email='user{}@google.com'.format(
                    user_idx + latest_user_id + 1),
                first_name='User',
                last_name=str(user_idx + latest_user_id + 1)
            )
        execution_time = time.time() - start_time
        logger.info(
            "Finished! Execution time: {0:0.2f} seconds!".format(execution_time)
        )
