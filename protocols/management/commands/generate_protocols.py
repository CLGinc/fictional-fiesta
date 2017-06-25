import random
import time
import logging

from django.core.management.base import BaseCommand

from protocols.models import Protocol, Result
from projects.models import Project
from users.models import User, Role


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--protocols',
            default=100,
            type=int,
            help='Number of protocols. Default: 100')
        parser.add_argument(
            '-s',
            '--steps',
            default=10,
            type=int,
            help='Number of steps per protocol procedure. Default: 10')
        parser.add_argument(
            '-r',
            '--results',
            default=10,
            type=int,
            help='Number of results per protocol. Default: 10')
        parser.add_argument(
            '-d',
            '--data-columns',
            default=10,
            type=int,
            help='Number of data-columns per result. Default: 10')

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        protocols_count = options.get('protocols')
        steps_count = options.get('steps')
        results_count = options.get('results')
        columns_count = options.get('data_columns')
        logger = logging.getLogger('django')
        projects_exist = Project.objects.exists()
        all_projects = list(Project.objects.all())
        max_projects = len(all_projects) if len(all_projects) <= 20 else 20
        projects_to_add = list()
        all_users = list(User.objects.all())
        max_users = len(all_users) if len(all_users) <= 20 else 20
        users_to_add = list()
        protocols_to_create = list()
        roles_to_create = list()
        results_to_create = list()

        # If no users exist break
        if len(all_users) == 0:
            if verbosity > 0:
                logger.info('There are no users in the db. You need to create users before protocols can be generated!')
                import sys
                sys.exit()

        if verbosity > 0:
            start_time = time.time()
            logger.info('Start generating protocols!')
        for protocol_idx in range(protocols_count):
            # Preparations for connecting
            # protocol with projects and users

            if verbosity > 1:
                logger.info('Working on protocol {}.'.format(protocol_idx))
            # Get a sample of users. The first user is Owner!
            number_of_users = random.randrange(1, max_users + 1)
            users_to_add = random.sample(all_users, number_of_users)
            if verbosity > 2:
                logger.info('Users sample ({}): {}.'.format(number_of_users, users_to_add))
            # Decide whether projects should be added and get a sample
            if projects_exist:
                add_to_projects = random.choice((True, False))
                if add_to_projects:
                    number_of_projects = random.randrange(
                        start=1,
                        stop=max_projects + 1
                    )
                    projects_to_add.append(
                        random.sample(all_projects, number_of_projects)
                    )
                    if verbosity > 2:
                        logger.info('Projects sample ({}): {}.'.format(number_of_projects, projects_to_add[-1]))
                else:
                    projects_to_add.append(list())
            # Generate steps
            procedure = {'steps': []}
            for step_idx in range(steps_count):
                procedure['steps'].append(
                    {
                        'description': 'Step {} description'.format(step_idx + 1),
                        'title': 'Step {}'.format(step_idx + 1)
                    }
                )
            # Create protocol
            protocol = Protocol(
                name='Generated Protocol {}'.format(protocol_idx),
                description='Description for protocol {}'.format(protocol_idx),
                label=random.choice(Protocol.LABELS)[0],
                last_modified_by=users_to_add[0],
                procedure=procedure
            )
            protocols_to_create.append(protocol)
            if verbosity > 2:
                logger.info('Generated protocol {}.'.format(protocol_idx))
            # Create random role between protocol and user. First is owner
            for index, user in enumerate(users_to_add):
                if index == 1:
                    role = 'owner'
                else:
                    role = random.choice(Role.ROLES[1:])[0]
                roles_to_create.append(
                    Role(
                        user=user,
                        protocol=protocol,
                        role=role
                    )
                )
                if verbosity > 2:
                    logger.info('Generated Role: "{}" with role "{}".'.format(user, role))
            # Generate data columns
            data_columns = {
                "dependent_variable": [],
                "independent_variable": [
                    {
                        "data": [
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                        ],
                        "title":"Independent Variable"
                    }
                ]
            }
            for column_idx in range(columns_count):
                data_columns['dependent_variable'].append(
                    {
                        'data': [
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048)
                        ],
                        'title': 'Trial {}'.format(column_idx + 1),
                    }
                )
            # Create randomly generated results for the selected protocol
            for result_idx in range(results_count):
                is_successful = False
                state = random.choice(Result.STATES)[0]
                if state == 'finished':
                    is_successful = random.choice((True, False))
                results_to_create.append(
                    Result(
                        title='Generated Result {}'.format(result_idx),
                        note='Note for result {}'.format(result_idx),
                        owner=user,
                        state=state,
                        is_successful=is_successful,
                        protocol=protocol,
                        project=random.choice(
                            projects_to_add[-1]) if add_to_projects else None,
                        data_columns=data_columns,
                        independent_variable='Salt Concentration (%)',
                        dependent_variable='Light Transmittance (%T)'
                    )
                )
                if verbosity > 2:
                    logger.info('Generated result {}.'.format(result_idx))
            if verbosity > 1:
                logger.info('Finished working on protocol {}.'.format(protocol_idx))

        # Write objects to db
        if verbosity > 1:
            logger.info('Writing protocols to database.')
        protocols = Protocol.objects.bulk_create(protocols_to_create)
        if verbosity > 1:
            logger.info('All protocols written to database.')

        if projects_exist:
            for index, protocol in enumerate(protocols):
                protocol.projects.add(*projects_to_add[index])
                if verbosity > 2:
                    logger.info('Added projects {} to "{}".'.format(projects_to_add[index], protocol))
            if verbosity > 1:
                logger.info('All projects added to protocols.')

        if verbosity > 1:
            logger.info('Writing roles to database.')
        Role.objects.bulk_create(roles_to_create)
        if verbosity > 1:
            logger.info('All roles written to database.')

        if verbosity > 1:
            logger.info('Writing results to database.')
        Result.objects.bulk_create(results_to_create)
        if verbosity > 1:
            logger.info('All results written to database.')

        if verbosity > 0:
            execution_time = time.time() - start_time
            logger.info(
                "Finished! Generated {} protocols with {} steps each, {} results with {} data columns each in {:0.2f} seconds!".format(
                    protocols_count,
                    steps_count,
                    results_count * protocols_count,
                    columns_count,
                    execution_time
                )
            )
