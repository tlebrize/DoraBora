from .base import BaseDatabase
from dora_bora.datamodel import Account, AccountList


class AccountsDatabase(BaseDatabase):
    table = "accounts"
    model = Account
    list_model = AccountList
