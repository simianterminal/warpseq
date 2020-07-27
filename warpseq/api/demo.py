import os
import sys

def suggest_device(api, device):


    available = api.devices.list_available()
    if device in available:
        return device

    device = os.environ.get("WARP_MIDI_DEVICE", None)
    if device in available:
        return device

    print("")
    print("")

    if len(available) == 0:
        print("Warp requires at least one MIDI device.")
        print("None were detected. You may need to create an virtual bus following your OS instructions.")

    else:

        print("AVAILABLE MIDI DEVICES:")

        for x in available:
            print("- %s" % x)

        print("")
        print("Warp requires at least one MIDI device.  Select one from the above list by setting")
        print("the environment variable WARP_MIDI_DEVICE")

    print("")
    print("(exiting)")
    print("")

    sys.exit(1)
