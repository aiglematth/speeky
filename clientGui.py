#Auteur --> aiglematth

#Imports
import tkinter              as tk
import tkinter.scrolledtext as scroll
from threading import Thread
from time      import sleep
from client    import *

#Classes
class ClientGui(tk.Tk):
    """
    Notre gui
    """
    def __init__(self, nom="Speeky client GUI", taille="720x640"):
        """
        Constructeur
        :param nom:    Le nom de notre screen
        :param taille: La taille de la fenetre
        """
        self.client = None
        tk.Tk.__init__(self)
        self.title(nom)
        self.geometry(taille)
        self.resizable(False, False)
        self.ip       = tk.StringVar()
        self.login    = tk.StringVar()
        self.password = tk.StringVar()
        self.invi     = tk.StringVar()
        self.invi.set("Visible")
        self.afficher = None
        self.envoyer  = None
        self.users    = None
        self.widgets  = []
        self.y        = 0
        self.update()
    
    def centerX(self, maitre, esclave, y):
        """
        On va centrer un widget
        :param maitre:  La fenêtre maître
        :param esclave: Le widget à passer
        :param y:       Le placement en y
        """
        x = maitre.winfo_width() // 2
        esclave.place(x=x, y=y, anchor=tk.CENTER)
    
    def place(self, widget, x, y):
        """
        On place un widgeet en partant de son centre
        :param widget: La widget
        :param x:      Le x
        :param y:      Le y
        """
        widget.place(x=x, y=y, anchor=tk.CENTER)

    def _connect(self, event=None):
        """
        On tente une connexion
        """
        client = Client(self.ip.get(), self.login.get(), self.password.get())
        if client.connect() == True:
            self.client = client
            self.tchat()
        else:
            error = tk.Label(self, text="Erreur...")
            self.widgets.append(error)
            self.centerX(self, error, self.y)

    def killWidgets(self):
        """
        Détruit tout les widgets
        """
        for widget in self.widgets:
            widget.destroy()
        try:
            self.unbind("<Return>")
        except:
            pass
        self.widgets = []

    def tchat(self):
        """
        Le tchat est lancé
        """
        self.killWidgets()

        w = 7
        ws = self.winfo_width()  // 12
        h = self.winfo_height() // 30


        toii = "Vous : \n" + self.client.user 
        toi  = tk.Label(self, text=toii, font=("", "10"))
        toi.grid(row=0)

        envoi = tk.Button(self, text="Envoyer", command=self.send)
        self.widgets.append(envoi)
        envoi.grid(row=0, column=1)

        actu = tk.Button(self, text="Actualiser", command=self.actu)
        self.widgets.append(actu)
        actu.grid(row=1)

        h2 = self.winfo_height() // 50
        self.envoyer = scroll.ScrolledText(self, width=ws, height=h2)
        self.widgets.append(self.envoyer)
        self.envoyer.grid(row=1, column=1)

        invi = tk.Button(self, textvariable=self.invi, command=self.invisible)
        self.widgets.append(invi)
        invi.grid(row=0, column=2)

        self.users = scroll.ScrolledText(self, width=w, height=5)
        self.widgets.append(self.users)
        self.users.grid(row=2)

        self.afficher = scroll.ScrolledText(self, width=ws, height=h)
        self.widgets.append(self.afficher)
        self.afficher.grid(row=2, column=1)

        hist = tk.Button(self, text="voir l'historique", command=self.hist)
        self.widgets.append(hist)
        hist.grid(row=1, column=2)

        clear = tk.Button(self, text="Effacer", command=self.clear)
        self.widgets.append(clear)
        clear.grid(row=2, column=2)

        self.bind("<Escape>", self.send)
        ThrAfficher(self).start()

    def actu(self, event=None):
        """
        On actualise les utilisateurs
        """
        self.client.wantList()
        liste = ""
        for user in self.client.listUsers:
            liste += f"{user},"
        liste = liste[0:len(liste)-1]
        self.afficherUsers(liste)

    def clear(self, event=None):
        """
        On clear les messages
        """
        self.afficher.delete(1.0, tk.END)

    def hist(self, event=None):
        """
        On recupere l'historique
        """
        self.client.wantHistory()
        sleep(1)
        self.afficher.insert(tk.END, "--- HISTORIQUE ---\n")
        for mess in self.client.history:
            format = self.format(mess)
            self.afficher.insert(tk.END, format)
        self.afficher.insert(tk.END, "\n--- ---------- ---\n")

    def format(self, mess):
        """
        On formate le mess à envoyer
        :param mess: Le message
        :return:     Le message
        """
        (user, mess) = mess.strip().split(self.client.sep)
        messFinal = f"### {user} ###\n"
        messFinal += mess
        messFinal += f"\n### {len(user)*'#'} ###\n\n"
        
        return messFinal

    def invisible(self, event=None):
        """
        On devient invisible
        """
        if self.invi.get().lower() == "invisible":
            self.client.hey()
            self.invi.set("Visible")
        else:
            self.client.invisible()
            self.invi.set("Invisible")

    def send(self, event=None):
        """
        Envoi un message
        """
        mess = self.envoyer.get(1.0, tk.END)
        if len(mess) == 0:
            return None
        self.envoyer.delete(1.0, tk.END)
        self.client.send(mess)

    def connect(self):
        """
        On affiche la page d'accueil
        """
        y = self.winfo_height() // 20

        labAccueil = tk.Label(self, text="Page de login", font=("", "50"))
        self.widgets.append(labAccueil)
        self.centerX(self, labAccueil, y*2)

        labIp = tk.Label(self, text="Ip du serveur")
        self.widgets.append(labIp)
        self.centerX(self, labIp, y*6)
        entIp = tk.Entry(self, textvariable=self.ip)
        self.widgets.append(entIp)
        self.centerX(self, entIp, y*7)
        
        labLogin = tk.Label(self, text="Nom d'utilisateur")
        self.widgets.append(labLogin)
        self.centerX(self, labLogin, y*8)
        entLogin = tk.Entry(self, textvariable=self.login)
        self.widgets.append(entLogin)
        self.centerX(self, entLogin, y*9)

        labPassword = tk.Label(self, text="Mot de passe")
        self.widgets.append(labPassword)
        self.centerX(self, labPassword, y*10)
        entPassword = tk.Entry(self, show="*", textvariable=self.password)
        self.widgets.append(entPassword)
        self.centerX(self, entPassword, y*11)

        confirm = tk.Button(self, text="Se connecter", command=self._connect)
        self.widgets.append(confirm)
        self.centerX(self, confirm, y*13)
        self.y = y*15

        self.bind("<Return>", self._connect)

    def afficherUsers(self, users):
        """
        On affiche les utilisateurs
        :param users: Les utilisateurs à affiicher
        """
        self.users.delete(1.0, tk.END)
        users = users.split(",")
        for user in users:
            self.users.insert(tk.END, f"\n{user}")

    def destroy(self):
        """
        A la destruction de la fenêtre, on surcharge destroy
        """
        try:
            self._variable.trace_vdelete('w', self.__tracecb)
        except AttributeError:
            pass
        else:
            del self._variable
        super().destroy()
        self.label = None
        self.scale = None
        if self.client != None:
            self.client.close()

class ThrAfficher(Thread):
    """
    Affichage des mess
    """
    def __init__(self, root):
        """
        Le constructeur
        :param root: La fenêtre juste au dessus
        """
        self.root = root
        Thread.__init__(self)

    def format(self, mess):
        """
        On formate le mess à envoyer
        :param mess: Le message
        :return:     Le message
        """
        (user, mess) = mess.decode().strip().split(self.root.client.sep)
        messFinal = f"### {user} ###\n"
        messFinal += mess
        messFinal += f"\n### {len(user)*'#'} ###\n\n"
        
        users = self.root.client.showUsers()
        self.root.afficherUsers(users)

        return messFinal

    def run(self):
        """
        On surcharge
        """
        while self.root.client.start == True:
            messages = self.root.client.mess
            self.root.client.clearMess()
            for mess in messages:
                m = self.format(mess)
                self.root.afficher.insert(tk.END, m)
            sleep(1)

if __name__ == "__main__":
    c = ClientGui()
    c.connect()
    c.mainloop()