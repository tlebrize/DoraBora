from dora_bora.logics import LoginLogic
from dora_bora.constants import POLICY
from dora_bora.database import AccountsDatabase, ServersDatabase, CharactersDatabase
from dora_bora.datamodel import ServerState, Gender, Class


def test_login():
    login = LoginLogic()
    login.start()

    assert login.outputs.get() == POLICY

    key = login.outputs.get()
    assert key.startswith("HC")
    assert len(key) == 32 + 2

    login.inputs.put("1.29.1")
    login.handle_input()
    assert login.outputs.get() == None

    accounts_db = AccountsDatabase("test")
    account = accounts_db.create(
        {
            "username": "test",
            "nickname": "testnick",
            "password": "password",
            "subscribed_seconds": 1000000,
            "is_game_master": "false",
            "security_question": "testsecu",
            "community": 0,
        }
    )

    login.inputs.put("test\n#1123456")
    login.handle_input()
    assert login.username == "test"
    assert login.password_hash == "123456"

    login_info = login.outputs.get().split("\0")
    assert login_info[0] == "Adtestnick"
    assert login_info[1] == "Ac0"
    assert login_info[2] == "AH1;0;110;0"
    assert login_info[3] == "AlK0"
    assert login_info[4] == "AQtestsecu"

    servers_db = ServersDatabase("test")
    servers_db.set(1, "state", ServerState.Online)
    characters_db = CharactersDatabase("test")
    characters_db.create(
        {
            "server_id": 1,
            "account_id": account.id,
            "name": "Pls",
            "gender": Gender.Female,
            "class_": Class.Iop,
            "colors": [-1, -1, -1],
            "kamas": 0,
            "spell_points": 0,
            "stat_points": 0,
            "energy": 0,
            "level": 1,
            "xp": 0,
        }
    )

    login.inputs.put("Ax")
    login.handle_input()
    assert login.outputs.get() == "AxK1000000000|1,1"

    login.inputs.put("AX1")
    login.handle_input()
    assert login.outputs.get() == "AYK127.0.0.1:4446;1"
