#!/usr/bin/env python

import logging
import sys
import time
import socket

from rtmidi.midiutil import open_midiinput

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

tallyClientIP = "10.75.140.5"
tallyClientPort = 5005
midiDeviceName = "MIDI Control 1"


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        # print("Received Message: " + str(message))

        # Check if midi message matches any of our filter criterea. filter should return a string if it matches and None otherwise
        messageString = self.message_filter(deltatime=deltatime, message=message)

        if messageString is not None:
            # print("Generated UDP Message: " + messageString)
            send_udp_packet(tallyClientIP, tallyClientPort, messageString)
        else:
            # print("No UDP String Created")
            pass


    def message_filter(self, deltatime, message):
        messageString = None
        if message == [144, 38, 127]:
            messageString = "LED1;Off;HostA;Mute;On"
        if message == [144, 38, 63]:
            messageString = "LED1;On;HostA;Mute;Off"
        if message == [144, 39, 127]:
            messageString = "LED2;Off;HostB;Mute;On"
        if message == [144, 39, 63]:
            messageString = "LED2;On;HostB;Mute;Off"
        if message == [144, 40, 127]:
            messageString = "LED3;Off;HostC;Mute;On"
        if message == [144, 40, 63]:
            messageString = "LED3;On;HostC;Mute;Off"
        if message == [144, 41, 127]:
            messageString = "LED4;Off;HostD;Mute;On"
        if message == [144, 41, 63]:
            messageString = "LED4;On;HostD;Mute;Off"
        if message == [144, 42, 127]:
            messageString = "LED5;Off;Brett;Mute;On"
        if message == [144, 42, 63]:
            messageString = "LED5;On;Brett;Mute;Off"

        return messageString


def send_udp_packet(ip, port, message):
    """Send a UDP packet to the specified IP and port."""
    returnValue = False
    try:
        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Encode the message to bytes
        message_bytes = message.encode('utf-8')

        # Send the packet
        udp_socket.sendto(message_bytes, (ip, port))

        print(f"Packet sent to {ip}:{port} with message: {message}")
        returnValue = True
    except Exception as e:
        print(f"Error sending UDP packet: {e}")
    finally:
        # Close the socket
        udp_socket.close()
        return returnValue


def main():
    # Prompts user for MIDI input port, unless a valid port number or name
    # is given as the first argument on the command line.
    # API backend defaults to ALSA on Linux.
    # port = sys.argv[1] if len(sys.argv) > 1 else None
    port = midiDeviceName

    try:
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Attaching MIDI input callback handler.")
    midiin.set_callback(MidiInputHandler(port_name))

    print("Entering main loop. Press Control-C to exit.")
    try:
        # Just wait for keyboard interrupt,
        # everything else is handled via the input callback.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin


if __name__ == "__main__":
    main()
