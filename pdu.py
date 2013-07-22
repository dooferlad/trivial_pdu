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
import time

class TelnetPDUControl(TelnetProtocol):

    def dataReceived(self, bytes_rx):
        bytes_rx = bytes_rx.rstrip()
        if not len(bytes_rx):
            # Don't respond to empty input
            return

        print bytes_rx
        if bytes_rx[-1] == "-":
            self.cmd_index += 1
            if self.cmd_index == len(self.cmds):
                # end of command list
                reactor.stop()
            else:
                # Next command
                time.sleep(1)
                self.sent_cmd = False

        if self.sent_cmd:
            # Don't re-send commands...
            return

        # If we are here, we haven't sent the current command, so send it.
        self.sent_cmd = True
        self.transport.write(self.cmds[self.cmd_index])

    def __init__(self, cmds):
        self.sent_cmd = False
        self.cmds = cmds
        self.cmd_index = 0

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
                    default=23,
                    type=int)
parser.add_argument("--index",
                    required=True,
                    help="Index on PDU of port to control.")
parser.add_argument("--on",
                    action="store_true",
                    help="Turn on power.")
parser.add_argument("--off",
                    action="store_true",
                    help="Turn off power.")
parser.add_argument("--reboot",
                    action="store_true",
                    help="Turn toggle power off then back on.")

args = parser.parse_args()

if args.on == args.off and not args.reboot:
    # If both on and off or neither on or off have been specified, this is an
    # error.
    print >> sys.stderr, "Error: Please specify --on XOR --off."
    exit(1)

prefix = "p" + args.index + "v"
cmds = []

if args.on:
    cmds.append(prefix + "1")
elif args.off:
    cmds.append(prefix + "0")
elif args.reboot:
    cmds.append(prefix + "0")
    cmds.append(prefix + "1")
else:
    args.print_help()
    exit(1)

reactor.connectTCP(args.server, args.port, TelnetFactory(cmds))
reactor.run()
