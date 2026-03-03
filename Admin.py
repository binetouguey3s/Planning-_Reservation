# Modele Admin: encapsule les donnees d'un administrateur connecte.
class Admin:
    def __init__(self, id_admin: int, nom: str, email: str):
        # Attributs prives exposes via des proprietes en lecture seule.
        self.__id_admin = id_admin
        self.__nom = nom
        self.__email = email

    @property
    def id_admin(self) -> int:
        # Identifiant unique de l'admin en base.
        return self.__id_admin

    @property
    def nom(self) -> str:
        # Nom de l'administrateur.
        return self.__nom

    @property
    def email(self) -> str:
        # Email de connexion de l'administrateur.
        return self.__email

    def __repr__(self) -> str:
        # Representation utile pour debug/logs.
        return f"Admin(id_admin={self.__id_admin}, nom='{self.__nom}', email='{self.__email}')"
