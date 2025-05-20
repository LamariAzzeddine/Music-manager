# 🎵 Music File Manager (MP3 & FLAC)

Une application Python complète pour la gestion de fichiers audio (MP3 et FLAC), avec interface en ligne de commande (CLI) **et** interface graphique (GUI).  
Elle permet l'extraction, la modification de métadonnées, la lecture de fichiers audio, la création de playlists XSPF, et bien plus.



## 📌 Fonctionnalités principales

✅ Extraction et affichage des métadonnées (titre, artiste, album, durée, image de couverture)  
✅ Exploration automatique d'un dossier pour détecter tous les fichiers audio MP3 et FLAC  
✅ Création de playlists personnalisées au format `.xspf` (XML Shareable Playlist Format)  
✅ Lecture des fichiers audio avec interface utilisateur graphique conviviale  
✅ Modification des tags/métadonnées des morceaux  
✅ Recherche d’informations via une API externe (Spotify ou autre)  

---

## 💻 Modes de fonctionnement

### 1. Mode CLI (Command Line Interface)
- Lancement via terminal
- Affiche les métadonnées des fichiers
- Génère des playlists automatiquement
- Permet d'explorer un répertoire

### 2. Mode GUI (Interface Graphique)
- Interface construite avec PyQt5
- Lecture audio
- Gestion des playlists
- Modification de tags
- Affichage des couvertures d’albums

---

## 🛠️ Technologies et bibliothèques utilisées

| Fonction                        | Bibliothèques utilisées                                      |
|---------------------------------|---------------------------------------------------------------|
| Extraction métadonnées         | `mutagen`, `mutagen.easyid3`, `mutagen.id3`                  |
| Lecture audio                  | `pygame`, `ffpyplayer`                                       |
| Interface graphique            | `PyQt5`, `QtWidgets`, `QtGui`, `QtCore`                      |
| Playlists XSPF                 | `xml.etree.ElementTree`                                      |
| Traitement d’images            | `Pillow`, `opencv-python (cv2)`                              |
| API externe                    | `requests` (pour récupérer les données enrichies)            |

---


## 🚀 Comment lancer le projet

```bash
git clone https://github.com/ton-nom-utilisateur/music-manager.git](https://github.com/LamariAzzeddine/Music-manager.git
cd Src

🎨 Mode GUI (interface graphique)
python main.py



🧑‍💻 Auteur
Azzeddine Lamari
