#Auteur --> aiglematth

#Imports
from hashlib    import *
from constantes import PATH_USER

#Classes
class ManageUsers():
    """
    Permet le mannagement des utilisateurs
    """
    def __init__(self, file=PATH_USER):
        """
        Constructeur de la classe
        :param file: Str du fichier où on va allr chercher / écrire les comptes
        """
        #Attributs
        self.file      = file
        self.separator = "\n" 
        self.spl       = ":" 
        #Exe
        with open(self.file, "a") as file:
            pass

    def hash(self, password, algo=sha256):
        """
        Hash une chaine de chars
        :param password: Le mot de passe à hash str
        :param algo:     L'algorithme utilisé pour hasher
        :return:         String
        """
        return algo(password.encode()).hexdigest()

    def format(self, user, password):
        """
        On formatte une ligne de ce fichier
        :param user:     Le nom d'utilisateur
        :param password: Le mot de passe
        :return:         La ligne (str)
        """
        return f"{user}{self.spl}{self.hash(password)}{self.separator}"

    def addCompte(self, user, password):
        """
        Permet d'ajouter un compte
        :param user:     Le nom de l'utilisateur à ajouter
        :param password: Le mot dee passe de cet utilisateur
        :return: Boolean (True tout c'est bien passé, False sinon)
        """
        with open(self.file, "r") as file:
            for usr in file.readlines():
                if usr.split(self.spl)[0] == user: 
                    return False
        
        with open(self.file, "a") as file:
            file.write(self.format(user, password))
    
        return True
    
    def remCompte(self, user):
        """
        On retire un compte
        :param user: L'utilisateur qu'on veut enlever
        :return: Boolean (True si fait, sinon False)
        """
        #Variables
        avant = None
        apres = []
        with open(self.file, "r") as file:
            avant = file.readlines()
        
        for line in avant:
            if user != line.split(self.spl)[0]:
                apres.append(line)
        
        with open(self.file, "w") as file:
            file.writelines(apres)
        
        return True

    
    def changePassword(self, user, newPass):
        """
        On change le password d'un utilisateur
        :param user:    Le nom d'utilisateur
        :param newPass: Le nouveau mot de passe
        :return:        Boolean
        """
        change = False
        actual  = None
        toWrite = []
        with open(self.file, "r") as file:
            actual = file.readlines()
        
        for usr in actual:
            if usr.split(self.spl)[0] != user:
                toWrite.append(usr)
            else:
                toWrite.append(self.format(user, newPass))
                change = True
        
        with open(self.file, "w") as file:
            file.writelines(toWrite)
        
        return change


    def showComptes(self):
        """
        On voit les comptes présents
        :return: Une liste de chaines de chars
        """
        toRet = None
        with open(self.file, "r") as file:
            toRet = file.readlines()
        
        for x in range(len(toRet)):
            toRet[x] = toRet[x].replace(self.separator, "")
                    
        return toRet
    
    def verifCompte(self, user, passwd):
        """
        On va vérifier si un compte existe
        :param user:   Le nom d'user
        :param passwd: Le mot de passe hashé
        :return:       Un booléen
        """
        ligne = self.format(user, passwd)
        if ligne.strip() in self.showComptes():
            return True
        return False

    def clearAll(self):
        """
        On clear tout
        :return Boolean:
        """
        with open(self.file, "w") as file:
            file.write("")

        return True
        
if __name__ == "__main__":
    """
    TESTZONE
    """
    db      = ManageUsers()
    usrPass = [("toto", "pass"), ("titi", "pass"), ("alfred", "compta"), ("toto", "password")]
    print("### AJOUT ###")
    for u in usrPass:
        if db.addCompte(u[0], u[1]) == True:
            print(f"User {u[0]} ajouté")
        else:
            print(f"User {u[0]} refusé")
    
    print("### VISION ###")
    for usr in db.showComptes():
        print(usr)
