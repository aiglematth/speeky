#Auteur --> aiglematth

#Imports
from socket           import socket, timeout, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from Crypto.PublicKey import RSA
from Crypto           import Random
from constantes       import SOCK, BITS
from manageUsers      import ManageUsers as Creds
from threadNet        import *

#Classes
class Serveur():
    """
    Classe principale de notre serveur
    """
    def __init__(self, sock=SOCK):
        """
        Constructeur
        :param sock: Un tuple (ip,port)
        """
        self.sep     = "<->"
        self.sock    = sock
        self.users   = []
        self.clients = []
        self.mess    = []
        self.creds   = Creds()
        self.verif   = self.creds.verifCompte
        self.start   = True

    """
    Principal
    """
    def run(self):
        """
        Méthode principale, lance le serveur
        :return: Booléen
        """
        try:
            threadEnvoyer = Envoyer(self)
            threadEnvoyer.start()
            print("### START ###")
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                sock.bind(self.sock)
                sock.listen(5)
                
                while True:
                    #On gère les nouveaux clients
                    client = self.acceptClient(sock)
                    print("### FIN D'UN ACCEPTCLIENT ###")
                    if client != False:
                        print("### NEW CLIENT ###")
                        threadRecept = Reception(client, self)
                        threadRecept.start()
                    
        except KeyboardInterrupt:
            print("### STOP ###")
            self.start = False
            self.stopClients()
            return True
        """
        except:
            print("### ERROR ###")
            self.start = False
            self.stopClients()
            return False
        """

    """
    On se simplifie la vie en dégroupant les tâches
    """
    def acceptClient(self, sock):
        """
        Se gère d'accepter un client
        :param sock: Le socket d'écoute
        :return:     Le socket client ou False
        """
        (client, infos) = sock.accept()
        #On génère les clefs
        key = RSA.generate(BITS, Random.new().read)
        pub = key.exportKey()
        #On lui envoie la clef
        client.send(pub)
        sock.settimeout(3)
        try:
            cr = client.recv(RECV)
            sock.settimeout(None)
        except timeout:
            sock.settimeout(None)
            return False
        #On attend la reception des creds de la forme user:passhash
        credsChiffre = key.decrypt(cr)
        creds        = credsChiffre.decode().strip().split(":")
        if len(creds) != 2:
            return False
        
        if self.verif(creds[0], creds[1]) == False:
            client.close()
            return False
        else:
            client.send(b"OK")
            self.clients.append(client)
            self.users.append(creds[0])
            return client
    
    def stopClients(self):
        """
        Méthode pour stopper les clients
        """
        for client in self.clients:
            client.close()

    def removeClient(self, client):
        """
        Permet de retirer un client de self.clients
        :param client: Le socket client
        """
        self.clients.remove(client)
    
    def addMess(self, mess):
        """
        Permet d'ajouter un mess dans self.mess
        :param mess: Le message à ajouter
        """
        mess = mess.decode() + self.sep + self.showUsers()
        self.mess.append(mess.encode())

    def showUsers(self):
        """
        Montre les users
        :return: Une liste formatée d'users
        """
        liste = ""
        for user in self.users:
            liste += user + ","
        liste  = liste[0:len(liste)-1]
        if len(liste) == 0:
            liste = "EMPTY"
        return liste

    def clearMess(self):
        """
        Permet de retirer les mess de self.mess
        """
        self.mess = []
    
    def removeUser(self, message):
        """
        On retire un utilisateur de self.users
        :param message: Le message
        """
        message = message.decode().split(self.sep)
        try:
            self.users.remove(message[0])
        except:
            pass
    
    def addUser(self, message):
        """
        On ajoute un user
        :param message: Le message à analyser
        """
        try:
            user = message.decode().strip().split(self.sep)[0]
            if user not in self.users:
                self.users.append(user)
        except:
            pass

    def db(self, dbM):
        """
        On formate les messages recus de la db
        :param dbM: Le tuple
        """
        send = f"HISTORY<::>"
        for (user,message) in dbM:
            send += f"{user}{self.sep}{message}<::>"
        send = send[0:len(send)-len("<::>")]
        return send

if __name__ == "__main__":
    s = Serveur()
    s.run()