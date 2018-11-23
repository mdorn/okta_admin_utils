# -*- coding: utf-8 -*-

"""Main module."""

from .tasks import (
    create_fake_users,
    delete_deactivated_users,
    get_users,
    deactivate_duplicate_apps,
    delete_inactive_apps
)
from .logs import configure_logging
configure_logging()

TASK_CONFIG = {
    'create-fake-users': create_fake_users,
    'remove-deactivated-users': delete_deactivated_users,
    'get-users': get_users,
    'deactivate-duplicate-apps': deactivate_duplicate_apps,
    'delete-inactive-apps': delete_inactive_apps,
}
