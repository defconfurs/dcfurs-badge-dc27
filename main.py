# main.py -- put your code here!
import pyb
import dcfurs
import badge
import emote
import micropython
import settings
import ubinascii

print("Booting...")
import animations

## Select the user's preferred boot animation.
available = animations.all()
selected = 0
if settings.bootanim:
    try:
        selected = available.index(getattr(animations, settings.bootanim))
    except Exception:
        pass

## Handle events from the bluetooth module.
def check_ble():
    if not badge.ble:
        return
    
    flags = badge.ble.read(badge.ble.REG_FLAGS)
    if flags & badge.ble.FLAG_EMOTE:
        ## Remote emote extravaganza!
        value = badge.ble.read16(badge.ble.REG_EMOTE)
        color = badge.ble.color()
        if (value):
            try:
                emote.render(chr(value & 0xff) + chr(value >> 8), color)
            except Exception:
                emote.random(color)
        else:
            emote.random(color)
        pyb.delay(2500)
    if flags & badge.ble.FLAG_AWOO:
        ## Someone started a howl
        msg = animations.scroll(" AWOOOOOOOOOOOOOOOO")
        delay = 0
        while delay < 5000:
            msg.draw()
            pyb.delay(msg.interval)
            delay += msg.interval

anim = available[selected]()
while True:
    anim.draw()
    ival = anim.interval
    while ival > 0:
        ## Change animation on button press, or emote if both pressed.
        if badge.right.event():
            if badge.left.value():
                emote.random()
            else:
                selected = (selected + 1) % len(available)
                anim = available[selected]()
                print("Playing animation " + available[selected].__name__)
        elif badge.left.event():
            if badge.right.value():
                emote.random()
            elif selected == 0:
                selected = len(available)-1
                anim = available[selected]()
                print("Playing animation " + available[selected].__name__)
            else:
                selected = selected - 1
                anim = available[selected]()
                print("Playing animation " + available[selected].__name__)
        # Service events.
        elif badge.boop.event():
            if hasattr(anim, 'boop'):
                anim.boop()
            else:
                if settings.debug:
                    micropython.mem_info()
                emote.boop()
                ival = 1000
        elif badge.ble:
            check_ble()

        ## Pause for as long as long as both buttons are pressed.
        if badge.right.value() and badge.left.value():
            ival += 50

        ## Run the animation timing
        if ival > 50:
            pyb.delay(50)
            ival -= 50
        else:
            pyb.delay(ival)
            ival = 0

        ## Attempt to suspend the badge between animations
        badge.trysuspend()
