##
## Some global settings constants
##

# The amount of inactivity (in milliseconds) that must elapse
# before the badge will consider going into standby. If set to
# zero then the badge will never attempt to sleep.
sleeptimeout = 900000

# The default banner message to print in the scroll.py animation.
banner = "DEFCON Furs"

# Enable extra verbose debug messages.
debug = False

# The animation to play at boot.
bootanim = "scroll"

# Whether the maze animation should autosolve.
mazesolver = True

# The base cooldown timing (in seconds) for BLE messages,
# which is applied to special beacons received with a high RSSI.
# Beacons with weaker signals are subject to a cooldown which
# will be a multiple of this time.
blecooldown = 60

# Default boop detection is done using the capacative touch
# detection on the nose (0), but we can also move the detection
# to use the capacative touch on the teeth (1).
boopselect = 0

# Default color selection that animations should use unless there
# is something more specific provided by the animation logic.
color = 0xffffff
