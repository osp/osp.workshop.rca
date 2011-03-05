# -*- coding: utf-8 -*-

import scribus
from PyQt4 import Qt, QtNetwork

global sock
global foo

methodList = [method for method in dir(scribus) if callable(getattr(scribus, method))]


def info(object, spacing=10, collapse=1):
    """
    Print methods and doc strings.
    Takes module, class, list, dictionary, or string.
    """
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    return "\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])


class MySock(Qt.QObject):
    """
    Class qui va persister et prendre en charge la lecture/ecriture sur le socket
    """
    def __init__(self, s):
        self.sock = s  # Socket preexistante et configurée
        Qt.QObject.connect(self.sock, Qt.SIGNAL("readyRead()"), self.slotRead)  # Connecte au signal émit par la socket "sock" à sa méthode de lecture slotread

    def slotRead(self):
        msg = unicode(self.sock.readAll())
        cmd = ":".join(msg.split(":")[2:])[:-2]
        if cmd.startswith("!") and cmd[1:] in methodList:
            try:
                getattr(scribus, cmd[1:])()
                self.sock.write("PRIVMSG #osp :called %s.\r\n" % cmd[1:])
            except TypeError:
                self.sock.write("PRIVMSG #osp :%s\r\n" % getattr(scribus, cmd[1:]).__doc__)
            
        #else:
            #self.sock.write("PRIVMSG #osp :%s is an unknown method.\r\n" % msg)
        #text = scribus.createText(100, 100, 100, 100)
        #scribus.setText(msg, text)
        # now do something constructive!!!


sock = QtNetwork.QTcpSocket()  # Creates a socket
sock.connectToHost(QtNetwork.QHostAddress.LocalHost, 6667, Qt.QIODevice.ReadWrite)  # Connects the socket
#sock.waitForReadyRead(30000)  # Waits a little bit
sock.write("NICK qtbot\r\n")  # Chooses a nick
sock.write("USER qtbot _qtbot __qtbot :Python IRC\r\n") # Sets alternative nicknames
sock.write("JOIN #osp\r\n")  # Joins the channel #osp
sock.write("PRIVMSG #osp :Hello World.\r\n")  # Says hello world
foo = MySock(sock)  # Creates an instance of MySock with sock
