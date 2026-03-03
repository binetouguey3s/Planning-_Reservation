# Modele Groupe: structure simple pour decrire un groupe reservant la salle.
class Groupe:
    def __init__(self, id_groupe: int, nom_groupe: str, responsable: str):
        # Attributs prives exposes via proprietes.
        self.__id_groupe = id_groupe
        self.__nom_groupe = nom_groupe
        self.__responsable = responsable

    @property
    def id_groupe(self) -> int:
        # Identifiant du groupe.
        return self.__id_groupe

    @property
    def nom_groupe(self) -> str:
        # Libelle du groupe.
        return self.__nom_groupe

    @property
    def responsable(self) -> str:
        # Nom du responsable du groupe.
        return self.__responsable

    def __repr__(self) -> str:
        return (
            f"Groupe(id_groupe={self.__id_groupe}, "
            f"nom_groupe='{self.__nom_groupe}', responsable='{self.__responsable}')"
        )

