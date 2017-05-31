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
        start_time = time.time()
        logger = logging.getLogger('django')
        logger.info('Start generating protocols')
        for protocol_idx in range(options['protocols']):
            # Preparations for connecting
            # protocol with projects and users
            add_to_projects = False
            user = random.choice(User.objects.all())
            if Project.objects.exists():
                add_to_projects = random.choice((True, False))
            if add_to_projects:
                number_of_projects = 0
                while number_of_projects == 0:
                    number_of_projects = random.randrange(
                        Project.objects.count())
                projects = random.sample(
                    list(Project.objects.all()),
                    number_of_projects)
            else:
                projects = list()
            # Generate steps
            procedure = {'steps': []}
            for step_idx in range(options['steps']):
                procedure['steps'].append(
                    {
                        'description': 'Step {} description'.format(step_idx),
                        'title': 'Step {}'.format(step_idx)
                    }
                )
            # Create protocol
            protocol = Protocol.objects.create(
                name='Protocol {}'.format(protocol_idx),
                description='Description for protocol {}'.format(protocol_idx),
                label=random.choice(Protocol.LABELS)[0],
                last_modified_by=user,
                procedure=procedure
            )
            # Create random role between protocol and user
            Role.objects.create(
                user=user,
                protocol=protocol,
                role=random.choice(Role.ROLES[:2])[0]
            )
            # Create random role between projects and user
            if add_to_projects:
                for project in projects:
                    project.protocols.add(protocol)
                    if not(project.roles.filter(user=user)):
                        Role.objects.create(
                            user=user,
                            project=project,
                            role=random.choice(Role.ROLES[1:])[0]
                        )
            # Generate data columns
            data_columns = {
                'data_columns': [
                    {
                        'data': [
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048)
                        ],
                        "variable":"independent",
                        "title":"Independent Variable"
                    }
                ]
            }
            for column_idx in range(options['data_columns']):
                data_columns['data_columns'].append(
                    {
                        'data': [
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048),
                            random.randint(0, 2048)
                        ],
                        'title': 'Trial {}'.format(column_idx + 1),
                        'variable': 'dependent'
                    }
                )
            # Create randomly generated results for the selected protocol
            for result_idx in range(options['results']):
                is_successful = False
                state = random.choice(Result.STATES)[0]
                if state == 'finished':
                    is_successful = random.choice((True, False))
                Result.objects.create(
                    title='Result {}'.format(result_idx),
                    note='Note for result {}'.format(result_idx),
                    owner=user,
                    state=state,
                    is_successful=is_successful,
                    protocol=protocol,
                    project=random.choice(
                        projects) if add_to_projects else None,
                    data_columns=data_columns,
                    data_type='number',
                    independent_variable='Salt Concentration (%)',
                    dependent_variable='Light Transmittance (%T)'
                )
        execution_time = time.time() - start_time
        logger.info(
            "Finished! Execution time: {0:0.2f} seconds!".format(
                execution_time
            )
        )
