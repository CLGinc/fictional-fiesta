import random
import time
import logging

from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import User, Role


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--projects',
            default=100,
            type=int,
            help='Number of projects. Default: 100')

    def handle(self, *args, **options):
        start_time = time.time()
        logger = logging.getLogger('django')
        logger.info('Start generating projects')
        if User.objects.exists():
            for project_idx in range(options['projects']):
                number_of_users = 0
                while number_of_users == 0:
                    number_of_users = random.randrange(
                        User.objects.count())
                users = random.sample(
                    list(User.objects.all()),
                    number_of_users)
                # Create project
                project = Project.objects.create(
                    name="Generated Project {}".format(project_idx),
                    description="Description for project {}".format(
                        project_idx),
                )
                # Create roles for project
                for idx, user in enumerate(users):
                    if idx == 1:
                        Role.objects.create(
                            user=user,
                            project=project,
                            role='owner'
                        )
                    else:
                        project_role = Role.objects.create(
                            user=user,
                            project=project,
                            role=random.choice(Role.ROLES[1:])[0]
                        )
        else:
            logger.info("No users in database! Operation cancelled!")
        execution_time = time.time() - start_time
        logger.info("Finished! Generated {} projects in {:0.2f} seconds!".format(
            options['projects'],
            execution_time)
        )
