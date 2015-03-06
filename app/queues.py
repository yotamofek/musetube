from django.conf import settings
from kombu import Exchange, Queue

task_exchange = Exchange('tasks', type='direct')


def create_queue(name):

    return