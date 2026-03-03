-- Creation de la base de données 
CREATE DATABASE IF NOT EXISTS reservation;
USE reservation;

-- Table des administrateurs (authentification).
CREATE TABLE IF NOT EXISTS admins (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    mot_de_passe VARBINARY(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- Table des groupes qui reservent la salle.
CREATE TABLE IF NOT EXISTS groupes (
    id_groupe INT AUTO_INCREMENT PRIMARY KEY,
    nom_groupe VARCHAR(120) NOT NULL UNIQUE,
    responsable VARCHAR(120) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des creneaux horaires de reference
CREATE TABLE IF NOT EXISTS creneaux (
    id_creneau INT AUTO_INCREMENT PRIMARY KEY,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    CONSTRAINT chk_creneau_valid CHECK (heure_fin > heure_debut),
    UNIQUE KEY uniq_creneau (heure_debut, heure_fin)
);

-- Table centrale des reservations (date + creneau + groupe + motif)
CREATE TABLE IF NOT EXISTS reservations (
    id_reservation INT AUTO_INCREMENT PRIMARY KEY,
    date_reservation DATE NOT NULL,
    creneau_id INT NOT NULL,
    groupe_id INT NOT NULL,
    motif VARCHAR(120) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reservation_creneau FOREIGN KEY (creneau_id) REFERENCES creneaux(id_creneau),
    CONSTRAINT fk_reservation_groupe FOREIGN KEY (groupe_id) REFERENCES groupes(id_groupe),
    CONSTRAINT uniq_reservation_jour_creneau UNIQUE (date_reservation, creneau_id)
);

-- Jeux de creneaux par defaut au demarrage
INSERT IGNORE INTO creneaux (heure_debut, heure_fin) VALUES
('09:00:00', '11:00:00'),
('11:00:00', '13:00:00'),
('14:00:00', '16:00:00'),
('16:00:00', '18:00:00'),
('18:00:00', '20:00:00');
