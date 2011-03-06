# -*- coding: utf-8 -*-

import scribus
import re
import ast
from PyQt4 import Qt, QtNetwork

global sock
global foo

methodList = [method for method in dir(scribus) if callable(getattr(scribus, method))]

class IRCBadMessage(Exception):
    pass


def nm_to_n(s):
    """Get the nick part of a nickmask.

    (The source of an Event is a nickmask.)
    """
    return s.split("!")[0]

def parsemsg(s):
    """
    Breaks a message from an IRC server into its prefix, command, and arguments.
    """
    prefix = ''
    trailing = []
    if not s:
       raise IRCBadMessage("Empty line.")
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    return prefix, command, args

def info(object, spacing=10, collapse=1):
    """
    Print methods and doc strings.
    Takes module, class, list, dictionary, or string.
    """
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    #return "\n".join(["%s %s" %
                      #(method.ljust(spacing),
                       #processFunc(str(getattr(object, method).__doc__)))
                     #for method in methodList])
    return ["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList]


class MySock(Qt.QObject):
    """
    Class qui va persister et prendre en charge la lecture/ecriture sur le socket
    """
    def __init__(self, s):
        self.sock = s  # Socket preexistante et configurée
        Qt.QObject.connect(self.sock, Qt.SIGNAL("readyRead()"), self.slotRead)  # Connecte au signal émit par la socket "sock" à sa méthode de lecture slotread
    
    def privmsg(self, chan, msg):
        self.sock.write("PRIVMSG %s :%s\r\n" % (chan, msg))
    
    def on_privmsg(self, nick, chan, msg):
        if chan == "#osp" and msg.startswith("!"):
            p = r"^([a-zA-Z]+)\((.+)*\)"
            r = re.search(p, msg[1:])
            if r is None:
                return
            else:
                cmd, args = r.groups()
            if cmd in methodList:
                scribus.setRedraw(False)
                try:
                    if args is None:
                        r = getattr(scribus, cmd)()
                    elif type(ast.literal_eval(args)) is tuple:
                        r = getattr(scribus, cmd)(*ast.literal_eval(args))
                    else:
                        r = getattr(scribus, cmd)(ast.literal_eval(args))
                    self.privmsg(chan, "called %s" % cmd)
                    self.privmsg(chan, "returned %s" % r if r is not None else "nothing")
                    # Ugly workaround to force scribus refreshing
                    scribus.zoomDocument(101)
                    scribus.zoomDocument(100)
                except TypeError:
                    self.privmsg(chan, "%s" % getattr(scribus, cmd).__doc__)
                scribus.setRedraw(True)
            elif cmd == "help":
                for i in info(scribus):
                    self.privmsg(chan, "%s" % i)
            else:
                self.privmsg(chan, "No such a command: %s" % cmd)
    
    def slotRead(self):
        raw_msg = unicode(self.sock.readAll())
        prefix, cmd, args = parsemsg(raw_msg)
        if cmd == "PRIVMSG":
            self.on_privmsg(nm_to_n(prefix), args[0], args[1][:-2])


sock = QtNetwork.QTcpSocket()  # Creates a socket
sock.connectToHost(QtNetwork.QHostAddress.LocalHost, 6667, Qt.QIODevice.ReadWrite)  # Connects the socket
#sock.waitForReadyRead(30000)  # Waits a little bit
sock.write("NICK qtbot\r\n")  # Chooses a nick
sock.write("USER qtbot _qtbot __qtbot :Python IRC\r\n") # Sets alternative nicknames
sock.write("JOIN #osp\r\n")  # Joins the channel #osp
sock.write("PRIVMSG #osp :Hello World.\r\n")  # Says hello world
foo = MySock(sock)  # Creates an instance of MySock with sock
