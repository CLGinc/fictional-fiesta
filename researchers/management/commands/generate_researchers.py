import random
import json
import time
import logging
import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User

from researchers.models import Researcher


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-r',
            '--researchers',
            default=10,
            type=int,
            help='Number of researchers. Default: 10')

    def handle(self, *args, **options):
        start_time = time.time()
        logger = logging.getLogger('django')
        logger.info('Start generating researchers')
        for researcher_idx in range(options['researchers']):
            user = User.objects.create(
                username=uuid.uuid4(),
                password=uuid.uuid4(),
                first_name="User {}".format(researcher_idx)
            )
            researcher = Researcher.objects.create(
                user=user
            )
        execution_time = time.time() - start_time
        logger.info("Finished! Execution time: {0:0.2f} seconds!".format(
                execution_time))
