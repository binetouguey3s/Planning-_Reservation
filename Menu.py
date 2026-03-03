from Authentification import AuthentificationAdmin
from Planning import Planning
from Reservation import ReservationService
from database import PlanningDatabase


class Menu:
    """Menu principal de l'application de reservation."""

    def __init__(self):
        # Initialisation base + services
        self.db = PlanningDatabase()
        if not self.db.initialiser_db("script.sql"):
            raise RuntimeError("Impossible d'initialiser la base de donnees")
        self.auth = AuthentificationAdmin(self.db)
        self.reservation = ReservationService(self.db)
        self.planning = Planning(self.reservation)

    def _demander_entier(self, message):
        """Demande un entier. Retourne None si la saisie est invalide."""
        try:
            return int(input(message).strip())
        except ValueError:
            print("Valeur invalide : veuillez saisir un nombre entier.")
            return None

    def _inscription_admin_initiale(self):
        # Si aucun admin n'existe, creation obligatoire du premier compte.
        if not self.auth.existe_admin():
            print("\n=== Creation du premier administrateur (obligatoire) ===")
            while True:
                nom = input("Nom: ").strip()
                email = input("E-mail: ").strip()
                mot_de_passe = input("Mot de passe: ").strip()
                if self.auth.inscrire_admin(nom, email, mot_de_passe):
                    break
                print("Echec de creation de l'administrateur, veuillez recommencer.")
            return

        # Sinon : creation optionnelle d'un administrateur supplementaire.
        print("\n=== Creation d'un administrateur (optionnelle) ===")
        reponse = input("Creer un administrateur maintenant ? (o/n): ").strip().lower()
        if reponse == "o":
            nom = input("Nom: ").strip()
            email = input("E-mail: ").strip()
            mot_de_passe = input("Mot de passe: ").strip()
            self.auth.inscrire_admin(nom, email, mot_de_passe)

    def _connexion_obligatoire(self):
        while self.auth.admin_connecte is None:
            print("\n=== Connexion administrateur ===")
            email = input("E-mail: ").strip()
            mot_de_passe = input("Mot de passe: ").strip()
            self.auth.connecter_admin(email, mot_de_passe)

    def _afficher_creneaux_et_groupes(self):
        """Affiche les creneaux et les groupes pour aider la reservation."""
        print("\nCreneaux existants")
        for creneau in self.reservation.lister_creneaux():
            print(f"[{creneau['id_creneau']}] {creneau['heure_debut']} - {creneau['heure_fin']}")

        print("\nGroupes existants")
        groupes = self.reservation.lister_groupes()
        if not groupes:
            print("Aucun groupe.")
            return False

        for groupe in groupes:
            print(f"[{groupe['id_groupe']}] {groupe['nom_groupe']} (Responsable : {groupe['responsable']})")
        return True

    def _afficher_menu_principal(self):
        print("\n=== GESTION DE RESERVATION DES SALLES ===")
        print("1. Afficher le planning global")
        print("2. Afficher les disponibilites")
        print("3. Ajouter un groupe")
        print("4. Menu de reservation (choisir entre 4 et 5)")
        print("5. Exporter en CSV")
        print("6. Quitter")

    def _afficher_menu_reservation(self):
        """Sous-menu : choix entre les 2 modes de reservation."""
        print("\n=== MENU RESERVATION ===")
        print("4. Reserver un creneau")
        print("5. Reserver par intervalle d'heures")
        print("0. Retour au menu principal")

    def _option_planning_global(self):
        date_str = input("Date (YYYY-MM-DD): ").strip()
        self.planning.afficher_global(date_str)

    def _option_disponibilites(self):
        date_str = input("Date (YYYY-MM-DD): ").strip()
        self.planning.afficher_disponibilites(date_str)

    def _option_ajouter_groupe(self):
        nom = input("Nom du groupe: ").strip()
        responsable = input("Responsable: ").strip()
        self.reservation.ajouter_groupe(nom, responsable)

    def _option_reserver_creneau(self):
        if not self._afficher_creneaux_et_groupes():
            return

        date_str = input("Date (YYYY-MM-DD): ").strip()
        creneau_id = self._demander_entier("ID du creneau: ")
        if creneau_id is None:
            return

        groupe_id = self._demander_entier("ID du groupe: ")
        if groupe_id is None:
            return

        motif = input("Motif (conference/reunion/atelier...): ").strip()
        self.reservation.reserver(date_str, creneau_id, groupe_id, motif)

    def _option_reserver_intervalle(self):
        if not self._afficher_creneaux_et_groupes():
            return

        date_str = input("Date (YYYY-MM-DD): ").strip()
        heure_debut = input("Heure de debut (HH:MM:SS): ").strip()
        heure_fin = input("Heure de fin (HH:MM:SS): ").strip()

        groupe_id = self._demander_entier("ID du groupe: ")
        if groupe_id is None:
            return

        motif = input("Motif (conference/reunion/atelier...): ").strip()
        self.reservation.reserver_par_horaire(date_str, heure_debut, heure_fin, groupe_id, motif)

    def _menu_reservation(self):
        """Boucle du sous-menu de reservation (a ou b)"""
        while True:
            self._afficher_menu_reservation()
            choix = input("Votre choix (reservation): ").strip().lo

            if choix == "a":
                self._option_reserver_creneau()
            elif choix == "b":
                self._option_reserver_intervalle()
            elif choix == "z":
                break
            else:
                print("Choix invalide.")

    def run(self):
        self._inscription_admin_initiale()
        self._connexion_obligatoire()

        while True:
            self._afficher_menu_principal()
            choix = input("Votre choix: ").strip()

            if choix == "1":
                self._option_planning_global()
            elif choix == "2":
                self._option_disponibilites()
            elif choix == "3":
                self._option_ajouter_groupe()
            elif choix == "4":
                self._menu_reservation()
            elif choix == "5":
                fichier = self.reservation.exporter_csv("planning_journalier.csv")
                if fichier:
                    print(f"Export termine : {fichier}")
            elif choix == "6":
                self.db.fermer()
                print("Au revoir.")
                break
            else:
                print("Choix invalide.")


Menu().run()
