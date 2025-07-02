from . import knife
from . import ship
from . import mute
from . import unmute
# später z. B. auch: from . import hug, slap, fun, ...

def register(bot):
    knife.register(bot)
    ship.register(bot)
    mute.register(bot)
    unmute.register(bot)
    # weitere.register(bot)