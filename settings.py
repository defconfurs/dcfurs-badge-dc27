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

# The base cooldown timing (in milliseconds) for BLE messages,
# which is applied to special beacons received with a high RSSI.
# Beacons with weaker signals are subject to a cooldown which
# will be a multiple of this time.
blecooldown = 60000
