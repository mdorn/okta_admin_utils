# -*- coding: utf-8 -*-

"""Main module."""

from okta_admin_utils.tasks import (
    create_fake_users,
    delete_deactivated_users,
    get_users,
    deactivate_apps,
    deactivate_duplicate_apps,
    delete_inactive_apps,
    create_oidc_app,
    create_group,
    create_test_users,
    trigger_rate_limit_violation,
)
from okta_admin_utils.logs import configure_logging
configure_logging()

TASK_CONFIG = {
    'create-fake-users': create_fake_users,
    'remove-deactivated-users': delete_deactivated_users,
    'get-users': get_users,
    'deactivate-apps': deactivate_apps,
    'deactivate-duplicate-apps': deactivate_duplicate_apps,
    'delete-inactive-apps': delete_inactive_apps,
    'create-oidc-app': create_oidc_app,
    'create-group': create_group,
    'create-test-users': create_test_users,
    'trigger-rate-limit-violation': trigger_rate_limit_violation,
}
