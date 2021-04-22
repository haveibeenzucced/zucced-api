"""Object-relational mapping between the compromised_accounts database table and it's
python counter part
"""
from zucced_api.core.db import DB


class Model(DB.Model):
    """Model."""

    __tablename__ = 'compromised_accounts'

    facebook_id_hash = DB.Column(DB.String(), primary_key=True, nullable=False)
