from .base import BaseDatabase
from dora_bora.datamodel import Account, AccountList


class AccountsDatabase(BaseDatabase):
    default_fields = ["id", "state"]
    table = "accounts"
    model = Account
    list_model = AccountList
