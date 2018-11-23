# -*- coding: utf-8 -*-

"""Main module."""

from .tasks import (
    create_fake_users,
    remove_deactivated_users,
    get_users
)
from .logs import configure_logging
configure_logging()

TASK_CONFIG = {
    'create-fake-users': create_fake_users,
    'remove-deactivated-users': remove_deactivated_users,
    'get-users': get_users,
}
