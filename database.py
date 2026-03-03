import mysql.connector
from mysql.connector import Error

# Connexion MySQL et initialisation
class PlanningDatabase:
    def __init__(
        self,
        host: str = "localhost",
        user: str = "planning_user",
        password: str = "MotDePassereserve123!",
        database: str = "reservation",
    ):
        # Parametres de connexion
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._connection = None

    def connecter(self):
        # Reutilise une connexion active pour eviter les reconnexions inutiles.
        if self._connection and self._connection.is_connected():
            return self._connection

        # Ouvre la connexion applicative vers la base cible.
        self._connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        return self._connection

    def fermer(self) -> None:
        # Ferme la connexion en fin d'application.
        if self._connection and self._connection.is_connected():
            self._connection.close()

    def initialiser_db(self, sql_file: str = "script.sql") -> bool:
        # Initialise la base/tables en executant le script SQL au demarrage.
        connexion_serveur = None
        cursor = None
        try:
            # Connexion sans selection de base pour permettre CREATE DATABASE.
            connexion_serveur = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
            )
            cursor = connexion_serveur.cursor()

            # Charge tout le script puis execute chaque instruction separement.
            with open(sql_file, "r", encoding="utf-8") as f:
                sql_content = f.read()

            for statement in [s.strip() for s in sql_content.split(";") if s.strip()]:
                try:
                    cursor.execute(statement)
                except Error as exc:
                    # Ignore les objets deja existants pour permettre un redemarrage propre.
                    if getattr(exc, "errno", None) in (1007, 1050):
                        continue
                    raise

            connexion_serveur.commit()
            return True
        except (Error, OSError) as exc:
            # Erreurs SQL ou lecture fichier.
            print(f"Erreur initialisation MySQL: {exc}")
            return False
        finally:
            # Nettoyage systematique des ressources SQL.
            if cursor:
                cursor.close()
            if connexion_serveur and connexion_serveur.is_connected():
                connexion_serveur.close()
