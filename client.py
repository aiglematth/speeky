#Auteur --> aiglematth

#Imports
from Crypto.PublicKey import RSA
from socket           import socket, timeout, AF_INET, SOCK_STREAM
from threading        import Thread

#Classes
class Client():
    """
    Le client
    """
    def __init__(self, ip, user, passwd, port=4444):
        """
        Le constructeur
        :param ip:     L'ip du serveur
        :param user:   Notre nom d'utilisateur
        :param passwd: Le mot de passe
        :param port:   Le port de connexion au serveur
        """
        self.listUsers  = []
        self.sock       = (ip, port)
        self.user       = user
        self.sep        = "<->"
        self.formatPass = f"{user}:{passwd}"
        self.socket     = None
        self.mess       = []
        self.history    = []
        self.start      = True

    def connect(self):
        """
        On fait notre connexion
        :return: True ou False
        """
        sock = socket(AF_INET, SOCK_STREAM)
        try:
            sock.connect(self.sock)
        except:
            return False
        
        key  = RSA.importKey(sock.recv(1024*8))
        mess = key.encrypt(self.formatPass.encode(), 32)[0]
        sock.send(mess)

        if len(sock.recv(1024).decode()) <= 0:
            return False
        
        sock.settimeout(3)
        self.socket = sock
        recv = Recv(self)
        recv.start()
        return True

    def send(self, mess):
        """
        Envoie un message de la forme user<->message
        :param mess: Une chaine de chars
        """
        mess = f"{self.user}{self.sep}{mess}"
        self.socket.send(mess.encode())

    def addMess(self, mess):
        """
        On ajoute un message dans self.mess
        :param mess: Le message
        """
        try:
            (user, mess, liste) = mess.split(self.sep.encode())
            self.addList(liste)
            self.mess.append(user + self.sep.encode() + mess)
        except:
            self.mess.append(mess)

    def clearMess(self):
        """
        On vide les messages
        """
        self.mess = []

    def sendBye(self):
        """
        On envoie qu'on se deco
        """
        self.send("BYEYB")
    
    def wantList(self):
        """
        On veut la liste des connectés
        """
        self.socket.send(b"LISTSIL")

    def wantHistory(self):
        """
        On veut la liste des messages
        """
        self.socket.send(b"HISTORY")

    def addList(self, liste):
        """
        On set la liste des utilisateurs actifs
        :param liste: La liste formatée
        """
        l = liste.decode().split(",")
        if "EMPTY" not in l:
            self.listUsers = l
        else:
            self.listUsers = []

    def addHistory(self, mess):
        """
        On set l'attribut self.history
        :param mess: Le message à mettre en forme
        """
        m = mess.decode().split("<::>")
        m.remove("HISTORY")
        self.history = m

    def hey(self):
        """
        On envoie un HEYEH pour se signaler
        """
        self.send("HEYEH")

    def invisible(self):
        """
        On se rend invisible
        """
        self.sendBye()

    def showUsers(self):
        """
        On formate les users user,user,user
        """
        liste = ""
        for user in self.listUsers:
            liste += user + ","
        return liste[0:len(liste)-1]

    def close(self):
        """
        Clôt le socket
        """
        self.sendBye()
        self.start = False
        self.socket.close()

class Recv(Thread):
    """
    Notre thread de réception des messages
    """
    def __init__(self, selfClient):
        """
        Le constructeur
        :param selfClient: La référence à la classe au dessus
        """
        self.selfC = selfClient
        Thread.__init__(self)

    def run(self):
        """
        On surcharge la méthode
        """
        while self.selfC.start == True:
            try:
                message = self.selfC.socket.recv(4096)
                if len(message) == 0:
                    break
                elif message.decode().split("<::>")[0] == "HISTORY":
                    self.selfC.addHistory(message)
                elif len(message.decode().split(self.selfC.sep)) in [2,3]:
                    self.selfC.addMess(message)
                else:
                    self.selfC.addList(message)
            except timeout:
                pass
            except:
                break

if __name__ == "__main__":
    from sys  import exit
    from time import sleep

    def send(client):
        mess = input("MESS>> ")
        client.send(mess)

    def look(client):
        for mess in client.mess:
            (user, mess) = mess.decode().split(client.sep)
            print(f"### {user} ###")
            print(mess)
            banner = len(user) * "#"
            print(f"### {banner} ###")
    
    def connect(client):
        client.wantList()
        sleep(1)
        print(client.listUsers)

    def quit(client):
        client.close()
        print("Bye")
        exit(0)

    def read(client):
        client.hey()

    def bye(client):
        client.invisible()

    actions = {
        "v" : look,
        "e" : send,
        "q" : quit,
        "c" : connect,
        "r" : read,
        "b" : bye
    }

    serv   = input("Adresse du serveur : ")
    user   = input("Nom d'utilisateur  : ")
    passwd = input("Mot de passe       : ")
    client = Client(serv, user, passwd)
    if client.connect() == True:
        print("### Bienvenu dans le tchat ! ###")
    else:
        print("### Une erreur est survenue ###")
        exit(1)

    while True:
        choix = input("(v)oir les mess | (e)nvoyer un mess | (c)onnectées | (q)uitter ")
        if choix in actions.keys():
            actions[choix.lower()](client)
        else:
            print("Choix invalide")