import random
import time
import logging

from django.core.management.base import BaseCommand

from projects.models import Project
from researchers.models import Researcher, Role


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
        if Researcher.objects.exists():
            for project_idx in range(options['projects']):
                number_of_researchers = 0
                while number_of_researchers == 0:
                    number_of_researchers = random.randrange(
                        Researcher.objects.count())
                researchers = random.sample(
                    list(Researcher.objects.all()),
                    number_of_researchers)
                # Create project
                project = Project.objects.create(
                    name="Project {}".format(project_idx),
                    description="Description for project {}".format(
                        project_idx),
                )
                # Create roles for project
                for idx, researcher in enumerate(researchers):
                    if idx == 1:
                        Role.objects.create(
                            researcher=researcher,
                            project=project,
                            role='owner'
                        )
                    else:
                        project_role = Role.objects.create(
                            researcher=researcher,
                            project=project,
                            role=random.choice(Role.ROLES[1:])[0]
                        )
        else:
            logger.info("No researchers in database! Operation cancelled!")
        execution_time = time.time() - start_time
        logger.info("Finished! Execution time: {0:0.2f} seconds!".format(
                execution_time))
