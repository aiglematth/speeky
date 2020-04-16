#Auteur --> aiglematth

#Imports
from pymysql.connections import Connection
from constantes          import HOST, USER, PASSWORD, DB, TABLE

#Classes
class Mysql(Connection):
    """
    Classe simplifiant les interractions simples avec une DB
    """
    def __init__(self, host, user, password, db):
        """
        Constructeur
        :param host:     L'adresse du serveur
        :param user:     Le nom d'utilisateur
        :param password: Le mot de passe
        :param db:       Le nom de la base de donnée
        """
        #Attributs
        Connection.__init__(self, host=host, user=user, password=password, db=db)

    """
    On se simplifie la vie
    """
    def split(self, liste):
        """
        on split une liste en mettant des virgules entre chaque item
        :param liste: La liste
        :return:      Une chaine de chars "item1,item2,...,itemn"
        """
        if type(liste) != list:
            liste = [liste]

        ret = ""
        for item in liste:
            ret += f"{item},"
        return ret[0:len(ret)-1]

    def splitDict(self, dico):
        """
        on split une liste en mettant des virgules entre chaque item
        :param dico: Le dico
        :return:     Une chaine de chars "item1,item2,...,itemn"
        """
        if type(dico) != dict:
            return "1 = 1"

        ret = ""
        for ((op, id), value) in dico.items():
            ret += f"{id} {op} '{value}',"

        return ret[0:len(ret)-1]

    def splitTuple(self, tupl, field=False):
        """
        on split une liste en mettant des virgules entre chaque item
        :param tupl:  Le tuple de tuples
        :param field: Si vrai, enleve les guillemets
        :return:      Une chaine de values a ajouter ou False
        """
        ret = ""
        if type(tupl) != tuple:
            return False
        
        if field == False:
            if type(tupl[0]) != tuple:
                return str(tupl)

            for values in tupl:
                ret += f"{str(values)},"
        else:
            ret += "("
            for fi in tupl:
                ret += f"{fi},"
            return ret[0:len(ret)-1] + ")"

        return ret[0:len(ret)-1]

    """
    Général
    """
    def exe(self, requete):
        """
        On retourne tout le nombre de lignes d'une requete
        :param requete: La requete
        :return:        Le nombre de lignes affectés
        """
        print(requete)
        lignes = self.query(requete)
        self.commit()
        return lignes

    """
    Selections
    """
    def _select(self, requete):
        """
        On retourne tout le contenu d'une requete
        :param requete: La requete
        :return:        Un tuple de tuples (chaque tuple étant une ligne de la table)
        """
        print(requete)
        with self.cursor() as doReq:
            doReq.execute(requete)
            return doReq.fetchall()

    
    def select(self, tables, ids="*", where=None):
        """
        On retourne le contenu d'une requete sans avoir besoin de créer la requete
        :param tables: Une table ou une liste de tables
        :param ids:    Un id ou une liste d'ids
        :param where:  Un dico de la forme {(op, id) : value}
        """
        requete = "SELECT " + self.split(ids) + " FROM " + self.split(tables) + " WHERE " + self.splitDict(where) + ";"
        return self._select(requete)

    """
    Insertions
    """
    def insert(self, table, values, ordre=""):
        """
        On insert des données dans une table
        :param table:  La table
        :param values: Un TUPLE de tuples des valeurs à ajouter
        :param ordre:  Un tuple donnant l'ordre des champs
        :return:       Le nombre de lignes affectées
        """
        if type(ordre) == tuple:
            requete = f"INSERT INTO {table} {self.splitTuple(ordre, field=True)} VALUES " + self.splitTuple(values) + ";"
        else:
            requete = f"INSERT INTO {table} VALUES " + self.splitTuple(values) + ";"
        return self.exe(requete)

    """
    Deletes
    """
    def delete(self, table, where=None):
        """
        On delete dans une table
        :param table: Une table
        :param where: Un dico de la forme {(op, id) : value}
        """
        requete = "DELETE FROM " + table + " WHERE " + self.splitDict(where) + ";"
        return self.exe(requete)

class DbMessages(Mysql):
    """
    On interragit avec la base de donnée
    """
    def __init__(self, host=HOST, user=USER, password=PASSWORD, db=DB, tableDef=TABLE):
        """
        Constructeur
        :param host:     L'adresse du serveur
        :param user:     Le nom d'utilisateur
        :param password: Le mot de passe
        :param db:       Le nom de la base de donnée
        :param tableDef: La definition de la table de la forme {"table" : "nom", "champs" : ("champ1", ..., "champn")}
        """
        #Attributs
        self.table = tableDef
        Mysql.__init__(self, host, user, password, db)
    
    def showAll(self):
        """
        On montre tous les messages
        :return: Un tuple de tuples
        """
        return self.select(self.table["table"])
    
    def showAllFrom(self, users):
        """
        On montre tous de certains utilisateurs
        :param users: Un utilisateur ou une liste d'utilisateurs
        :return:      La selection
        """
        where = {}
        if type(users) != list:
            users = [users]
        
        for user in users:
            where[("LIKE", self.table["champs"][0])] = user
        
        return self.select(self.table["table"], where=where)
    
    def addMess(self, infos):
        """
        On ajoute un mess dans la db
        :param infos: Un tuple dont les infos correspondent à chaque champ de self.table["champs"] DANS L'ORDRE (ou un tuple de tuples)
        :return: Un booléen
        """
        if type(infos[0]) != tuple:
            infos = (infos)

        if self.insert(self.table["table"], infos, ordre=self.table["champs"]) > 0:
            return True
        return False
    
    def delFrom(self, users):
        """
        On delete tous de certains utilisateurs
        :param users: Un utilisateur ou une liste d'utilisateurs
        :return: Le nombre de lignes affectées
        """
        where = {}
        if type(users) != list:
            users = [users]
        
        for user in users:
            where[("LIKE", self.table["champs"][0])] = user
        
        return self.delete(self.table["table"], where=where)
    
    def delAll(self):
        """
        On delete toute la table
        :return: Le nombre de lignes affectées
        """
        return self.delete(self.table["table"])

if __name__ == "__main__":
    from time import sleep
    db = DbMessages()
    print(db.showAll())
    print("")
    print(db.showAllFrom("toto"))
    print("")
    print(db.delFrom("toto"))
    print("")
    sleep(30)
    print(db.showAll())
    print("")
    print(db.addMess(("toto", "je suis de retour !!")))
    print("")
    print(db.showAll())