#Auteur --> aiglematth

#Imports
from threading  import Thread
from time       import sleep
from constantes import RECV
from dbMessages import DbMessages

#Classes
class Envoyer(Thread):
    """
    La classe qui pourra envoyer les messages aux clients
    """
    def __init__(self, selfNet):
        """
        Constructeur
        :param selfNet: La référence de self de la classe supérieure
        """
        self.selfNet = selfNet
        Thread.__init__(self)
    
    def run(self):
        """
        Méthode à surcharger qui sera appelée quand on fera monThread.start()
        """
        while self.selfNet.start == True:
            #On dort une seconde...
            sleep(1)
            #On enregistre les messages et on clear
            messages = self.selfNet.mess
            self.selfNet.clearMess()
            #On envoi à chaque client
            if len(messages) != 0:
                for client in self.selfNet.clients:
                    #Envoi de chaque mess
                    for mess in messages:
                        client.send(mess)

class Reception(Thread):
    """
    La classe qui pourra recevoir les messages d'un client
    """
    def __init__(self, client, selfNet):
        """
        Constructeur
        :param client:  Le socket du client
        :param selfNet: La référence de self de la classe supérieure
        """
        self.client  = client
        self.db      = DbMessages()
        self.selfNet = selfNet
        Thread.__init__(self)
    
    def run(self):
        """
        Méthode à surcharger qui sera appelée quand on fera monThread.start()
        """
        while self.selfNet.start == True:
            message = self.client.recv(RECV)
            if len(message) == 0:
                self.selfNet.removeClient(self.client)
                break
            elif "BYEYB" in message.decode():
                self.selfNet.removeUser(message)
            elif message.decode() == "LISTSIL":
                liste = self.selfNet.showUsers()
                self.client.send(liste.encode())
            elif "HEYEH" in message.decode():
                self.selfNet.addUser(message)
            elif "HISTORY" in message.decode():
                mess = self.db.showAll()
                send = self.selfNet.db(mess)
                self.client.send(send.encode())
            else:
                self.selfNet.addMess(message)
                (user, mess) = message.decode().split(self.selfNet.sep)
                self.db.addMess((user, mess))

