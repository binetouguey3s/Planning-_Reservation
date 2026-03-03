# Room-Master Pro

Application terminale Python pour gerer les reservations de la salle polyvalente du Centre Culturel Douta Seck.

## Objectifs couverts
- Authentification administrateur obligatoire.
- Vue planning global journalier (creneaux occupes + `[LIBRE]`).
- Vue disponibilites (creneaux libres uniquement).
- Affectation de creneau a un groupe avec prevention des conflits:
  - verification metier Python,
  - contrainte SQL `UNIQUE (date_reservation, creneau_id)`.
- Export CSV des reservations valides.

## Prerequis
- Python 3
- MySQL Server
- Package Python: `mysql-connector-python`, `bcrypt`

## Structure modulaire
- `database.py` : connexion et initialisation DB.
- `Admin.py` : modele admin (encapsulation).
- `Groupe.py` : modele groupe (encapsulation).
- `Motif.py` : modele motif.
- `Authentification.py` : service d'inscription/connexion admin.
- `Reservation.py` : service de reservation, consultation et export CSV.
- `Planning.py` : affichage planning/disponibilites.
- `Menu.py` : interface terminale (point d'entree).
- `script.sql` : script SQL de creation de la base et des tables.

## Lancer l'application
1. Adapter les identifiants MySQL dans `database.py` si necessaire.
2. Executer:

```bash
python3 Menu.py
```

Le programme initialise la base avec `script.sql`, demande une connexion admin, puis affiche le menu.

## Livrables
- Script SQL: `script.sql`
- Code source modulaire Python: fichiers `.py`
- Exemple export CSV: `planning_journalier.csv`
