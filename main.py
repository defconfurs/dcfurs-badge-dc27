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
        elif badge.left.event():
            if badge.right.value():
                emote.random()
            elif selected == 0:
                selected = len(available)-1
                anim = available[selected]()
            else:
                selected = selected - 1
                anim = available[selected]()
        # Service events.
        #elif badge.ble.any():
        #    ble()
        elif badge.boop.event():
            if hasattr(anim, 'boop'):
                anim.boop()
            else:
                if settings.debug:
                    micropython.mem_info()
                emote.boop()
                ival = 1000

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
