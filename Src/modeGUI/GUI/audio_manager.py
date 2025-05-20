# Importation des modules nécessaires
from modeCli import is_audio_file, explore_folder, extract_metadata  # Importation de fonctions spécifiques depuis modeCli.py
import pygame  # Utilisé pour la gestion de l'audio (lecture, pause, arrêt)
import os  # Permet d'interagir avec le système de fichiers
import mimetypes  # Utilisé pour identifier les types MIME des fichiers
import mutagen  # Bibliothèque pour lire les métadonnées des fichiers audio
from mutagen.easyid3 import EasyID3  # Simplifie l'accès aux métadonnées ID3
from mutagen.id3 import ID3NoHeaderError  # Exception levée pour des fichiers ID3 mal formés

class AudioManager:
    """
    Classe pour gérer les fichiers audio : détection, exploration de dossiers,
    extraction de métadonnées, lecture audio, etc.
    """
    def __init__(self):
        """
        Initialise l'AudioManager. Ajoute un type MIME pour les fichiers FLAC
        et initialise le module mixer de Pygame pour la gestion audio.
        """
        mimetypes.add_type('audio/flac', '.flac')  # Ajoute FLAC comme type MIME audio
        pygame.mixer.init()  # Initialise le module mixer de Pygame

    def is_audio_file(self, filepath):
        """
        Vérifie si un fichier est un fichier audio pris en charge (.mp3 ou .flac).
        
        :param filepath: Chemin du fichier à vérifier
        :return: True si le fichier est audio, False sinon
        """
        # Vérifie l'extension du fichier
        if filepath.lower().endswith(('.mp3', '.flac')):
            # Devine le type MIME du fichier
            mime_type, _ = mimetypes.guess_type(filepath)
            # Vérifie si le type MIME correspond à un fichier audio valide
            return mime_type in ['audio/mpeg', 'audio/flac']
        return False

    def explore_folder(self, directory):
        """
        Explore un dossier et renvoie une liste des fichiers audio trouvés.
        
        :param directory: Chemin du dossier à explorer
        :return: Liste de tuples contenant le nom et le chemin complet des fichiers audio
        """
        audio_files = []  # Liste pour stocker les fichiers audio trouvés
        for root, _, files in os.walk(directory):  # Parcours récursif du dossier
            for file in files:
                file_path = os.path.join(root, file)  # Chemin complet du fichier
                if self.is_audio_file(file_path):  # Vérifie si c'est un fichier audio
                    audio_files.append((file, file_path))  # Ajoute le nom et le chemin
        return audio_files

    def extract_metadata(self, filepath):
        """
        Extrait les métadonnées d'un fichier audio.
        
        :param filepath: Chemin du fichier audio
        :return: Dictionnaire contenant les métadonnées ou None en cas d'erreur
        """
        try:
            # Charge les métadonnées du fichier avec Mutagen
            audio = mutagen.File(filepath, easy=True)
            if audio:
                # Calcule la durée du fichier audio (arrondie en secondes)
                duration_in_seconds = round(audio.info.length) if audio.info else 'Unknown'
                # Ajoute "secondes" pour une meilleure lisibilité
                duration = f"{duration_in_seconds} secondes" if duration_in_seconds != 'Unknown' else 'Unknown'
                return {
                    "Title": audio.get('title', ['Unknown'])[0],
                    "Artist": audio.get('artist', ['Unknown'])[0],
                    "Album": audio.get('album', ['Unknown'])[0],
                    "Duration": duration
                }
            else:
                print(f"Impossible de lire les métadonnées du fichier {filepath}")
                return None
        except Exception as e:
            # Capture les erreurs liées à l'extraction des métadonnées
            print(f"Erreur lors de la lecture de {filepath}: {e}")
            return None

    def play_audio(self, filepath):
        """
        Joue un fichier audio.
        
        :param filepath: Chemin du fichier audio à jouer
        """
        try:
            pygame.mixer.music.load(filepath)  # Charge le fichier audio
            pygame.mixer.music.play()  # Commence la lecture
        except Exception as e:
            print(f"Erreur lors de la lecture de {filepath}: {e}")

    def pause_audio(self):
        """
        Met en pause la lecture audio en cours.
        """
        pygame.mixer.music.pause()  # Pause la lecture audio

    def stop_audio(self):
        """
        Arrête la lecture audio en cours.
        """
        pygame.mixer.music.stop()  # Arrête complètement la lecture

    def get_cover_image(self, filepath):
        """
        Extrait l'image de couverture d'un fichier audio, si disponible.
        
        :param filepath: Chemin du fichier audio
        :return: Données binaires de l'image de couverture ou None
        """
        try:
            # Charge les données du fichier audio avec Mutagen
            audio = mutagen.File(filepath)
            # Vérifie si le fichier contient une image de couverture (APIC)
            if audio and "APIC:" in audio.tags:
                cover_art = audio.tags["APIC:"].data  # Extrait les données de l'image
                return cover_art
            else:
                print(f"Aucune couverture trouvée pour {filepath}")
                return None
        except (ID3NoHeaderError, KeyError, IOError) as e:
            # Capture les erreurs liées à l'extraction de l'image
            print(f"Erreur lors de l'extraction de la couverture : {e}")
            return None
