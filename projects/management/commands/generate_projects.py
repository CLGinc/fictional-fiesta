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
        verbosity = options.get('verbosity')
        logger = logging.getLogger('django')
        projects_count = options.get('projects')
        all_users = list(User.objects.all())
        users_to_add = list()
        projects_to_create = list()
        roles_to_create = list()

        # If no users exist break
        if len(all_users) == 0:
            if verbosity > 0:
                logger.info('There are no users in the db. You need to create users before projects can be generated!')
                import sys
                sys.exit()

        if verbosity > 0:
            start_time = time.time()
            logger.info('Start generating projects')
        for project_idx in range(projects_count):
            if verbosity > 1:
                logger.info('Working on project {}.'.format(project_idx))
            number_of_users = random.randrange(1, len(all_users) + 1)
            users_to_add = random.sample(all_users, number_of_users)
            # Create project
            project = Project(
                name="Generated Project {}".format(project_idx),
                description="Description for project {}".format(
                    project_idx),
            )
            projects_to_create.append(project)
            if verbosity > 2:
                logger.info('Generated Project {}.'.format(project_idx))
            # Create roles for project. First is owner
            for index, user in enumerate(users_to_add):
                if index == 1:
                    role = 'owner'
                else:
                    role = random.choice(Role.ROLES[1:])[0]
                roles_to_create.append(
                    Role(
                        user=user,
                        project=project,
                        role=role
                    )
                )
                if verbosity > 2:
                    logger.info('Generated Role: "{}" with role "{}".'.format(user, role))
            if verbosity > 1:
                logger.info('Finished working on project {}.'.format(project_idx))

        # Write objects to db
        if verbosity > 1:
            logger.info('Writing projects to database.')
        Project.objects.bulk_create(projects_to_create)
        if verbosity > 1:
            logger.info('All projects written to database.')
        if verbosity > 1:
            logger.info('Writing roles to database.')
        Role.objects.bulk_create(roles_to_create)
        if verbosity > 1:
            logger.info('All roles written to database.')

        if verbosity > 0:
            execution_time = time.time() - start_time
            logger.info("Finished! Generated {} projects in {:0.2f} seconds!".format(
                projects_count,
                execution_time)
            )
