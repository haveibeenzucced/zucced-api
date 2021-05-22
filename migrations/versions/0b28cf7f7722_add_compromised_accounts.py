"""add_compromised_accounts.

Revision ID: 0b28cf7f7722
Revises:
Create Date: 2021-04-22 01:16:36.837487
"""
import pathlib
import sys

# Make migrations importable.
DIR_NAME = str(pathlib.Path(__file__).parents[2])
sys.path.append(DIR_NAME)

from alembic import op
from migrations import helper

# revision identifiers, used by Alembic.
revision = "0b28cf7f7722"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    helper.execute(
        bind=op.get_bind(),
        filename="add_compromised_accounts/upgrade.sql",
    )


def downgrade():
    helper.execute(
        bind=op.get_bind(),
        filename="add_compromised_accounts/downgrade.sql",
    )
