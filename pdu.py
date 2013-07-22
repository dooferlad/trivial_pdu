#!/usr/bin/python

# This file is part of Aduino PDU.
# 
# Aduino PDU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Aduino PDU is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Aduino PDU.  If not, see <http://www.gnu.org/licenses/>.

"""
Arduino simple PDU CLI controller.
Connects to PDU over telnet, issues command, quits.

Why am I using twisted? Because I am playing. No other technical decision!
"""

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, TelnetProtocol
import argparse
import sys

class TelnetPDUControl(TelnetProtocol):

    def dataReceived(self, bytes_rx):
        self.rx += bytes_rx
        if self.rx.rstrip()[-1] == "-":
            reactor.stop()

        if self.sent_cmd:
            return

        self.sent_cmd = True
        print self.cmd
        self.transport.write(self.cmd)

    def __init__(self, cmd):
        self.sent_cmd = False
        self.rx = ""
        self.cmd = cmd

    def connectionMade(self):
        pass

class TelnetFactory(ClientFactory):
    def __init__(self, cmd):
        self.cmd = cmd

    def buildProtocol(self, addr):
        return TelnetTransport(TelnetPDUControl, self.cmd)

parser = argparse.ArgumentParser("Send command to Arduino PDU.")
parser.add_argument("server",
                    help="Server to telnet to in order to access the PDU.")
parser.add_argument("port",
                    help="Port to telnet to in order to access the PDU.",
                    default=23)
parser.add_argument("--index",
                    required=True,
                    help="Index on PDU of port to control.")
parser.add_argument("--on",
                    action="store_true",
                    help="Turn on power.")
parser.add_argument("--off",
                    action="store_true",
                    help="Turn off power.")

args = parser.parse_args()

if args.on == args.off:
    # If both on and off or neither on or off have been specified, this is an
    # error.
    print >> sys.stderr, "Error: Please specify --on XOR --off."
    exit(1)

cmd = "p" + args.index + "v"

if args.on:
    cmd += "1"
elif args.off:
    cmd += "0"
else:
    args.print_help()
    exit(1)

print cmd

reactor.connectTCP("192.168.1.10", 2000, TelnetFactory(cmd))
reactor.run()
