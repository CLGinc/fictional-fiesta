import random
import json

from django.core.management.base import BaseCommand
from django.utils import timezone

from protocols.models import Protocol, Procedure
from protocols.models import Step, Result, DataColumn, Protocol
from projects.models import Project
from researchers.models import Researcher, Role


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
        MEASUREMENTS = (
            ('Volume', 'litre'),
            ('Mass', 'kg'),
            ('Mass', 'mg'),
            ('Mass', 'g'),
            ('Speed' 'km/h'),
            ('Speed' 'm/s'),
            ('Speed' 'm/s'),
        )
        #'''
        for protocol_idx in range(options['protocols']):
            # Preparations for connecting
            # protocol with projects and researchers
            researcher = random.choice(Researcher.objects.all())
            add_to_project = random.choice((True, False))
            if add_to_project:
                project = random.choice(Project.objects.all())
            else:
                project = None
            # Create protocol
            protocol = Protocol.objects.create(
                name='Protocol {}'.format(protocol_idx),
                description='Description for protocol {}'.format(protocol_idx),
                label=random.choice(Protocol.LABELS)[0]
            )
            procedure = Procedure.objects.create(
                protocol=protocol,
                datetime_last_modified=timezone.now(),
                last_modified_by=researcher
            )
            # Create steps for procedure
            for step_idx in range(options['steps']):
                step = Step.objects.create(
                    text='Step {} for protocol {}'.format(
                        step_idx,
                        protocol_idx),
                    procedure=procedure,
                    order=step_idx
                )
            # Create randomly generated results for the selected protocol
            for result_idx in range(options['results']):
                result = Result.objects.create(
                    note='Note for result {}'.format(result_idx),
                    owner=researcher,
                    state=random.choice(Result.STATES)[0],
                    is_successful=random.choice((True, False)),
                    protocol=protocol,
                    project=project
                )
            # Create data columnd constructed from random data
            for data_idx in range(options['data_columns']):
                data = {
                    "title": "Column {}".format(data_idx),
                    "Data": random.sample(list(range(100)), 10)
                }
                measurement = random.choice(MEASUREMENTS)
                data_column = DataColumn.objects.create(
                    result=result,
                    data=json.dumps(data),
                    is_independent=random.choice((True, False)),
                    measurement=measurement[0],
                    unit=measurement[1],
                )
            # Create random role between protocol and researcher
            protocol_role = Role.objects.create(
                researcher=researcher,
                protocol=protocol,
                role=random.choice(Role.ROLES)[0]
            )
            # Create random role between project and researcher
            if add_to_project:
                project.protocols.add(protocol)
                if not(project.roles.filter(researcher=researcher)):
                    project_role = Role.objects.create(
                        researcher=researcher,
                        project=project,
                        role=random.choice(Role.ROLES)[0]
                    )
        #'''
