#Auteur --> aiglematth

""" Constantes de manageUsers """
PATH_USER = "users.db"

""" Constantes de dbMessages """
HOST     = "localhost"
USER     = "speeky"
PASSWORD = "speeky"
DB       = "messages"
#Le premier index de champs doit toujours être le champs des utiliateurs et le second le champ des messages
TABLE    = {
    "table"  : "messages",
    "champs" : ("user", "message")
}

""" Constantes de serveur """
SOCK = ("", 4444)
RECV = 1024
BITS = 2048