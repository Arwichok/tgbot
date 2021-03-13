from . import commands, errors


def setup_handlers(dp):
    commands.setup(dp)
    errors.setup(dp)
