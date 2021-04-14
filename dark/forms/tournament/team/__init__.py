__all__ = [
    'AddTeamForm',
    'ChangeTeamNameForm',
    'AddTeamRoleForm',
    'ModifyTeamRoleForm',
    'AddTeamMemberForm',
    'ChangeTeamMemberRoleForm',
    'AddTeamBotForm',
    'ModifyTeamBotForm',
]

from .add import AddTeamForm
from .change_name import ChangeTeamNameForm
from .role import AddTeamRoleForm, ModifyTeamRoleForm
from .member import AddTeamMemberForm, ChangeTeamMemberRoleForm
from .bot import AddTeamBotForm, ModifyTeamBotForm
