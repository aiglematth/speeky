#Auteur --> aiglematth

#Imports
import tkinter              as tk
import tkinter.scrolledtext as scroll
from manageUsers import *
from dbMessages  import *

#Classes
class AdminGui(tk.Tk):
    """
    Notre gui
    """
    def __init__(self, nom="Panel d'administration de Speeky"):
        """
        Constructeur
        :param nom:    Le nom de notre screen
        """
        self.users = ManageUsers()
        self.db    = DbMessages()
        tk.Tk.__init__(self)
        self.title(nom)
        self.resizable(False, False)

        self.addLogin = tk.StringVar()
        self.addPass  = tk.StringVar()
        self.addReus  = tk.StringVar()

        self.remLogin = tk.StringVar()
        self.remReus  = tk.StringVar()

        self.login        = tk.StringVar()
        self.newPass      = tk.StringVar()
        self.changereussi = tk.StringVar()

        self.dbUser = tk.StringVar()
        self.dbDel  = tk.StringVar()
        self.lignes = tk.StringVar()
        
        titre = ("", 20)

        #Les widgets
        """ USERS MANAGE """
        us = tk.Label(self, text="Administrer les utilisateurs", font=titre)
        us.grid(row=0, column=0, columnspan=3)

        adduser = tk.Label(self, text="Ajouter un utilisateur")
        adduser.grid(row=1, column=0)

        addLogin = tk.Entry(self, textvariable=self.addLogin)
        addLogin.grid(row=2, column=0)

        addPass = tk.Entry(self, textvariable=self.addPass, show="*")
        addPass.grid(row=3, column=0)

        addButton = tk.Button(self, text="Ajouter", command=self.add)
        addButton.grid(row=4, column=0)

        reussi = tk.Label(self, textvariable=self.addReus)
        reussi.grid(row=5, column=0)

        remuser = tk.Label(self, text="Retirer un utilisateur")
        remuser.grid(row=1, column=1)

        remlogin = tk.Entry(self, textvariable=self.remLogin)
        remlogin.grid(row=2, column=1, rowspan=2)

        remButton = tk.Button(self, text="Retirer", command=self.rem)
        remButton.grid(row=4, column=1)

        remReussi = tk.Label(self, textvariable=self.remReus)
        remReussi.grid(row=5, column=1)
        
        changeUser = tk.Label(self, text="Changer de mot de passe")
        changeUser.grid(row=1, column=2)

        login = tk.Entry(self, textvariable=self.login)
        login.grid(row=2, column=2)

        newPass = tk.Entry(self, textvariable=self.newPass, show="*")
        newPass.grid(row=3, column=2)

        change = tk.Button(self, text="Changer", command=self.change)
        change.grid(row=4, column=2)

        changereussi = tk.Label(self, textvariable=self.changereussi)
        changereussi.grid(row=5, column=2)

        voirUsers = tk.Button(self, text="Voir les utilisateurs", command=self.voirUsers)
        voirUsers.grid(row=6, column=0, columnspan=3)

        self.textUsers = scroll.ScrolledText(self, height=10)
        self.textUsers.grid(row=7, column=0, columnspan=3)

        """ DB MANAGE """
        dbL = tk.Label(self, text="Gestion de la base de données", font=titre)
        dbL.grid(row=0, column=4, columnspan=4)

        voirDb = tk.Button(self, text="Voir le contenu de la base", command=self.voirDb)
        voirDb.grid(row=3, column=4)

        dbEntry = tk.Entry(self, textvariable=self.dbUser)
        dbEntry.grid(row=1, column=4)

        voirDbU = tk.Button(self, text="Voir le contenu de la base selon un user", command=self.voirDbU)
        voirDbU.grid(row=2, column=4)

        viderDb = tk.Button(self, text="Vider la base", command=self.viderDb)
        viderDb.grid(row=3, column=5)

        dbDel = tk.Entry(self, textvariable=self.dbDel)
        dbDel.grid(row=1, column=5)

        voirDbU = tk.Button(self, text="Vider les messages d'un utilisateur", command=self.viderDbU)
        voirDbU.grid(row=2, column=5)

        lignes = tk.Label(self, textvariable=self.lignes)
        lignes.grid(row=4, rowspan=2, columnspan=2, column=4)

        self.textDb = scroll.ScrolledText(self, height=10)
        self.textDb.grid(row=7, column=4, columnspan=5)

    def viderDbU(self, event=None):
        """
        On vide un utilisateur
        """
        lignes = self.db.delFrom(self.dbDel.get())
        self.lignes.set(f"{lignes} lignes affectées")

    def viderDb(self, event=None):
        """
        Vider le contenu de la base de donnée
        """
        lignes = self.db.delAll()
        self.lignes.set(f"{lignes} lignes affectées")

    def voirDbU(self, event=None):
        """
        Voir selon un user
        """
        index = 0
        self.textDb.delete(1.0, tk.END)
        for tupl in self.db.showAllFrom(self.dbUser.get()):
            self.textDb.insert(tk.END, str(tupl))
            index += 1
        self.lignes.set(f"{index} résultats affichés")

    def voirDb(self, event=None):
        """
         On montre le contenu de la base de données
        """
        index = 0
        self.textDb.delete(1.0, tk.END)
        for tupl in self.db.showAll():
            self.textDb.insert(tk.END, str(tupl))
            index += 1
        self.lignes.set(f"{index} résultats affichés")

    def voirUsers(self, event=None):
        """
        On affiche les utilisateurs
        """
        self.textUsers.delete(1.0, tk.END)
        for user in self.users.showComptes():
            self.textUsers.insert(tk.END, user + "\n")

    def change(self, event=None):
        """
        On change le mot de passe d'un user
        """
        if self.users.changePassword(self.login.get(), self.newPass.get()) == True:
            self.changereussi.set("Mot de passe changé")
        else:
            self.changereussi("Utilisateur inconnu")
        self.voirUsers()

    def add(self, event=None):
        """
        On ajoute un utilisateur
        """
        if self.users.addCompte(self.addLogin.get(), self.addPass.get()) == True:
            self.addReus.set("Compte ajouté")
        else:
            self.addReus.set("Le nom d'utilisateur est déjà attribué")
        self.voirUsers()

    def rem(self, event=None):
        """
        On retire un compte
        """
        if self.users.remCompte(self.remLogin.get()) == True:
            self.remReus.set("Compte retiré")
        else:
            self.remReus.set("Compte inexistant")    
        self.voirUsers()

if __name__ == "__main__":
    AdminGui().mainloop()