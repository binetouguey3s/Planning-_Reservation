# Modele Motif: encapsule le libelle textuel d'une reservation.
class Motif:
    def __init__(self, libelle: str):
        # Normalise l'entree utilisateur.
        self.__libelle = libelle.strip()

    @property
    def libelle(self) -> str:
        # Retourne le libelle du motif.
        return self.__libelle

    def __str__(self) -> str:
        # Affichage direct du motif.
        return self.__libelle

