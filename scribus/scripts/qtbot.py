# -*- coding: utf-8 -*-

import scribus
from PyQt4 import Qt, QtNetwork

global sock
global foo


class MySock(Qt.QObject):
    """
    Class qui va persister et prendre en charge la lecture/ecriture sur le socket
    """
    def __init__(self, s):
        self.sock = s  # Socket preexistante et configurée
        Qt.QObject.connect(self.sock, Qt.SIGNAL("readyRead()"), self.slotRead)  # Connecte au signal émit par la socket "sock" à sa méthode de lecture slotread

    def slotRead(self):
        msg = self.sock.readAll()
        self.sock.write("PRIVMSG #osp :yo cool.\r\n")
        text = scribus.createText(100, 100, 100, 100)
        scribus.setText(msg, text)
        # now do something constructive!!!


sock = QtNetwork.QTcpSocket()  # Creates a socket
sock.connectToHost(QtNetwork.QHostAddress.LocalHost, 6667, Qt.QIODevice.ReadWrite)  # Connects the socket
sock.waitForReadyRead(30000)  # Waits a little bit
sock.write("NICK qtbot\r\n")  # Chooses a nick
sock.write("USER qtbot _qtbot __qtbot :Python IRC\r\n") # Sets alternative nicknames
sock.write("JOIN #osp\r\n")  # Joins the channel #osp
sock.write("PRIVMSG #osp :Hello World.\r\n")  # Says hello world
foo = MySock(sock)  # Creates an instance of MySock with sock
