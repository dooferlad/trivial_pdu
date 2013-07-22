A very low cost PDU
===================
This project contains an Arduino sketch that controls some digital output pins
via its serial port and a python command line tool designed to connect to the
Arduino over telnet. It is assumed that you have a telnet to serial server
running, such as ser2net.

In order to make the hardware side of this project work you need to connect some
of the output pins from your Arduino to a relay breakpot board, such as
[this one][1] including power. The [Arduino Uno][0] I am using can cope with
this quite eaily.


PDU Command Structure
---------------------
The code running no the Arduino listens to the serial port and responds to
commands in the form `p<port number>v<value>`, so `p4v1` would turn on port 4 and
`p1v0` would turn off port 1.

Arduinos are designed to reset when a new connection is made over the serial
port (USB TTY included). The reset process is reasonably fast and this allows
the boards to be programmed easily, but it also means that all the relays get
turned off when you connect. You can change this by breaking the RESET EN
connection. On the Arduiono Uno this is a solder pad that you can easily
re-connect.

Remote PDU Access
-----------------
I am using [ser2net][2] to present the serial port of the
Arduino via telnet by hooking it up to a PC running Ubuntu.

[0]: http://arduino.cc/en/Main/arduinoBoardUno
[1]: http://www.cutedigi.com/breakout-board/dc-5v-eight-channels-relay-breakout-with-optoisolator.html
[2]: http://ser2net.sourceforge.net/
