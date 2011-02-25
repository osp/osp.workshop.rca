import socket
 
network = 'irc.freenode.net'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
irc.send ( 'NICK proutcacaprout\r\n' )
irc.send ( 'USER proutcacaprout proutcacaprout proutcacaprout :Python IRC\r\n' )
irc.send ( 'JOIN #stdin\r\n' )
irc.send ( 'PRIVMSG #stdin :Hello World.\r\n' )
while True:
    data = irc.recv ( 4096 )
    if data.find ( 'PING' ) != -1:
        irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
    if data.find ( '!proutcacaprout quit' ) != -1:
        irc.send ( 'PRIVMSG #stdin :Fine, if you don\'t want me\r\n' )
        irc.send ( 'QUIT\r\n' )
    if data.find ( 'hi proutcacaprout' ) != -1:
        irc.send ( 'PRIVMSG #stdin :I already said hi...\r\n' )
    if data.find ( 'hello proutcacaprout' ) != -1:
        irc.send ( 'PRIVMSG #stdin :I already said hi...\r\n' )
    if data.find ( 'KICK' ) != -1:
        irc.send ( 'JOIN #stdin\r\n' )
    if data.find ( 'cheese' ) != -1:
        irc.send ( 'PRIVMSG #stdin :WHERE!!!!!!\r\n' )
    if data.find ( 'slaps proutcacaprout' ) != -1:
        irc.send ( 'PRIVMSG #stdin :This is the Trout Protection Agency. Please put the Trout Down and walk away with your hands in the air.\r\n' )
    print data
