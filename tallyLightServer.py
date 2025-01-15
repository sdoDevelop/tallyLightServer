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

HostAOffString = "LED1;Off;HostA;Mute;On"
HostAOnString = "LED1;On;HostA;Mute;Off"
HostBOffString = "LED2;Off;HostB;Mute;On"
HostBOnString = "LED2;On;HostB;Mute;Off"
HostCOffString = "LED3;Off;HostC;Mute;On"
HostCOnString = "LED3;On;HostC;Mute;Off"
HostDOffString = "LED4;Off;HostD;Mute;On"
HostDOnString = "LED4;On;HostD;Mute;Off"
BrettOffString = "LED5;Off;Brett;Mute;On"
BrettOnString = "LED5;On;Brett;Mute;Off"


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
            messageString = HostAOffString
        if message == [144, 38, 63]:
            messageString = HostAOnString
        if message == [144, 39, 127]:
            messageString = HostBOffString
        if message == [144, 39, 63]:
            messageString = HostBOnString
        if message == [144, 40, 127]:
            messageString = HostCOffString
        if message == [144, 40, 63]:
            messageString = HostCOnString
        if message == [144, 41, 127]:
            messageString = HostDOffString
        if message == [144, 41, 63]:
            messageString = HostDOnString
        if message == [144, 42, 127]:
            messageString = BrettOffString
        if message == [144, 42, 63]:
            messageString = BrettOnString
        if message[0] == 176 and message[1] == 6:
            strip = 1
            section = 1
            brightnessLevel = message[2]
            if brightnessLevel > 100:
                brightnessLevel = 100
            messageString = "Brightness;1;1;"+str(brightnessLevel)

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
    
def sendBrightnessControl(strip=0, section=0, brightness=100):
    brightnessPacket = [
        "Brightness",
        strip,
        section,
        brightness,
        None,
        None,
        None,
        None,
        None,
        None,
    ]

def turnAllOn():
    hostAOn()
    hostBOn()
    hostCOn()
    hostDOn()
    brettOn()

def turnAllOff():
    hostAOff()
    hostBOff()
    hostCOff()
    hostDOff()
    brettOff()

def hostAOn():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=HostAOnString)

def hostAOff():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=HostAOffString)

def hostBOn():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=HostBOnString)

def hostBOff():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=HostBOffString)

def hostCOn():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=HostCOnString)

def hostCOff():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=HostCOffString)

def hostDOn():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=HostDOnString)

def hostDOff():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=HostDOffString)

def brettOn():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=BrettOnString)

def brettOff():
    send_udp_packet(ip=tallyClientIP, port=tallyClientPort, message=BrettOffString)

def onByNumber(hostNumber=0, on=False):
    if hostNumber == 0:
        if on:
            turnAllOn()
        else:
            turnAllOff()
    elif hostNumber == 1:
        if on:
            hostAOn()
        else:
            hostAOff()
    elif hostNumber == 2:
        if on:
            hostBOn()
        else:
            hostBOff()
    elif hostNumber == 3:
        if on:
            hostCOn()
        else:
            hostCOff()
    elif hostNumber == 4:
        if on:
            hostDOn()
        else:
            hostDOff()
    elif hostNumber == 5:
        if on:
            brettOn()
        else:
            brettOff()

def blinkAll(repeat=1, speed=1):
    for i in range(repeat):
        turnAllOn()
        time.sleep(speed)
        turnAllOff()
        time.sleep(speed)

def blinkThroughSections(repeat=1, speed=1):
    turnAllOff()
    for i1 in range(repeat):
        for i in range(5):
            onByNumber(hostNumber=i+1, on=True)
            time.sleep(speed)
            onByNumber(hostNumber=i+1, on=False)
            time.sleep(speed)

def chaseAcrossStrips(repeat=1, speed=1):
    turnAllOff()
    for i1 in range(repeat):
        for sectionIndex in range(5):
            for stripIndex in range(3):
                onByNumber(hostNumber=sectionIndex+1, on=True)
                time.sleep

def testModeFunction(mode=0):
    if mode == 0:
        while True:
            blinkAll(repeat=4, speed=.2)
            blinkThroughSections(repeat=4, speed=.2)

def main():
    # Prompts user for MIDI input port
    # port = sys.argv[1] if len(sys.argv) > 1 else None
    port = midiDeviceName
    testMode = sys.argv[1]if len(sys.argv) > 1 else 1
    if testMode is not None:
        print("TEST MODE")
        testModeFunction()

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
