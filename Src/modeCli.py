"""
Module de ligne de commande pour gérer l'interface de mode,
modification des tags audio, génération de playlists et lecture audio.

Ce module permet d'analyser des fichiers MP3 et FLAC, d'extraire leurs 
métadonnées, de modifier leurs tags ID3, de créer des playlists au format 
XSPF et de lire les fichiers audio.
"""

# Importation des bibliothèques nécessaires
import os  # Pour manipuler les chemins de fichiers et répertoires
import mimetypes  # Pour détecter les types MIME des fichiers
import argparse  # Pour gérer les arguments en ligne de commande
import sys  # Pour quitter le programme en cas d'erreur
import mutagen  # Pour manipuler les métadonnées des fichiers audio
from mutagen.easyid3 import EasyID3  # Pour modifier facilement les tags ID3
import xml.etree.ElementTree as ET  # Pour générer des fichiers XML pour les playlists
import pygame  # Pour lire des fichiers audio
import time  # Pour gérer les pauses durant la lecture audio

# Ajouter les types MIME manquants, ici pour le format FLAC
mimetypes.add_type('audio/flac', '.flac')

# Fonction pour vérifier si un fichier est un fichier audio pris en charge
def is_audio_file(filepath):
    """
    Vérifie si un fichier est un fichier audio pris en charge (MP3 ou FLAC).

    @param filepath: Le chemin du fichier à vérifier.
    @return: True si le fichier est un audio MP3 ou FLAC, sinon False.
    """
    # Vérifie l'extension et le type MIME du fichier
    if filepath.lower().endswith(('.mp3', '.flac')):
        mime_type, _ = mimetypes.guess_type(filepath)
        return mime_type in ['audio/mpeg', 'audio/flac']
    return False

# Fonction pour explorer un répertoire et lister les fichiers audio
def explore_folder(directory):
    """
    Explore un répertoire et retourne une liste de fichiers audio pris en charge (MP3 ou FLAC).

    @param directory: Le chemin du répertoire à explorer.
    @return: Liste des fichiers audio trouvés dans le répertoire.
    """
    audio_files = []
    # Parcourt tous les sous-répertoires et fichiers du répertoire donné
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Ajoute les fichiers audio détectés à la liste
            if is_audio_file(file_path):
                audio_files.append(file_path)
    return audio_files

# Fonction pour extraire et afficher les métadonnées d'un fichier audio
def extract_metadata(filepath):
    """
    Extrait et affiche les métadonnées d'un fichier audio (Titre, Artiste, Album, Durée).

    @param filepath: Le chemin du fichier audio dont les métadonnées sont extraites.
    """
    try:
        audio = mutagen.File(filepath)
        if audio:
            print(f"Fichier: {filepath}")
            # Affiche les tags si disponibles, sinon "Unknown"
            print(f"Title: {audio.get('TIT2', 'Unknown')}")
            print(f"Artist: {audio.get('TPE1', 'Unknown')}")
            print(f"Album: {audio.get('TALB', 'Unknown')}")
            print(f"Duration: {audio.info.length:.2f} seconds\n")
        else:
            print(f"Impossible de lire les métadonnées du fichier {filepath}")
    except Exception as e:
        print(f"Erreur lors de la lecture de {filepath}: {e}")

# Fonction pour modifier les tags ID3 d'un fichier audio
def modify_tags(filepath, title=None, artist=None, album=None):
    """
    Modifie les tags ID3 d'un fichier audio (Titre, Artiste, Album).

    @param filepath: Le chemin du fichier audio dont les tags doivent être modifiés.
    @param title: Le nouveau titre à assigner (ou None pour ne pas modifier).
    @param artist: Le nouvel artiste à assigner (ou None pour ne pas modifier).
    @param album: Le nouvel album à assigner (ou None pour ne pas modifier).
    """
    try:
        # Tente de charger les tags existants ou en crée de nouveaux
        try:
            audio = EasyID3(filepath)
        except mutagen.id3.ID3NoHeaderError:
            audio = mutagen.File(filepath, easy=True)
            if audio is None:
                print(f"Impossible de charger les métadonnées pour {filepath}.")
                return
            audio.add_tags()

        # Met à jour les tags si des valeurs sont spécifiées
        if title:
            audio['title'] = title
        if artist:
            audio['artist'] = artist
        if album:
            audio['album'] = album

        # Sauvegarde les modifications dans le fichier
        audio.save()
        print(f"Tags modifiés pour {filepath}")
        
        # Relit les tags pour vérifier les modifications
        updated_audio = EasyID3(filepath)
        print("Tags après modification :")
        print(f"Title: {updated_audio.get('title', ['Unknown'])[0]}")
        print(f"Artist: {updated_audio.get('artist', ['Unknown'])[0]}")
        print(f"Album: {updated_audio.get('album', ['Unknown'])[0]}")
    except Exception as e:
        print(f"Erreur lors de la modification des tags pour {filepath}: {e}")

# Fonction pour créer une playlist XSPF contenant les fichiers audio
def create_xspf_playlist(playlist_file, audio_files):
    """
    Crée une playlist XSPF à partir d'une liste de fichiers audio.

    @param playlist_file: Le chemin du fichier de playlist XSPF à générer.
    @param audio_files: Liste des fichiers audio à ajouter à la playlist.
    """
    # Crée un élément XML pour la playlist
    playlist = ET.Element('playlist', version="1", xmlns="http://xspf.org/ns/0/")
    tracklist = ET.SubElement(playlist, 'trackList')

    # Ajoute chaque fichier audio à la playlist
    for audio_file in audio_files:
        track = ET.SubElement(tracklist, 'track')
        location = ET.SubElement(track, 'location')
        location.text = os.path.abspath(audio_file)

    # Sauvegarde la playlist dans un fichier
    tree = ET.ElementTree(playlist)
    tree.write(playlist_file, encoding='utf-8', xml_declaration=True)

    print(f"Playlist générée: {playlist_file}")

# Fonction pour lire un fichier audio
def play_audio(filepath):
    """
    Lit un fichier audio en utilisant le module Pygame.

    @param filepath: Le chemin du fichier audio à lire.
    """
    try:
        # Initialise le module mixer de Pygame
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()

        # Indique que la lecture a commencé
        print(f"Lecture de {filepath}... Appuyez sur Ctrl+C pour arrêter.")

        # Attend que la musique soit terminée ou interrompue
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nLecture interrompue.")
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Erreur lors de la lecture de {filepath}: {e}")
    finally:
        pygame.mixer.quit()

# Fonction principale pour gérer les arguments et exécuter les fonctionnalités
def main():
    """
    Point d'entrée du programme. Gère les arguments en ligne de commande et appelle les fonctions appropriées.
    """
    parser = argparse.ArgumentParser(description="Analyse des fichiers MP3 et FLAC, modification des tags, et génération de playlists.")
    
    # Définition des arguments disponibles
    parser.add_argument('-f', '--file', type=str, help="Analyser un fichier audio pour extraire ses métadonnées.")
    parser.add_argument('-d', '--directory', type=str, help="Explorer un répertoire pour créer une playlist.")
    parser.add_argument('-o', '--output', type=str, help="Fichier de sortie pour la playlist générée.")
    parser.add_argument('-p', '--play', type=str, help="Lire un fichier audio spécifié.")
    parser.add_argument('--set-tags', nargs='+', help="Modifier les tags d'un fichier audio. Format: title=<value> artist=<value> album=<value>")

    args = parser.parse_args()

    # Vérification des arguments et exécution des fonctionnalités correspondantes
    if not args.file and not args.directory and not args.play:
        print("Erreur: Vous devez spécifier un fichier (-f), un répertoire (-d), un fichier à jouer (-p), ou une modification de tags (--set-tags). Utilisez -h pour l'aide.")
        sys.exit(1)

    # Analyse d'un fichier audio
    if args.file:
        if os.path.exists(args.file) and is_audio_file(args.file):
            extract_metadata(args.file)
        else:
            print(f"Fichier {args.file} non trouvé ou non valide.")
    
    # Exploration d'un répertoire pour générer une playlist
    elif args.directory:
        if os.path.isdir(args.directory):
            audio_files = explore_folder(args.directory)
            if audio_files:
                if args.output:
                    create_xspf_playlist(args.output, audio_files)
                else:
                    print("Fichiers audio trouvés :")
                    for audio_file in audio_files:
                        print(audio_file)
            else:
                print("Aucun fichier MP3 ou FLAC trouvé dans le répertoire.")
        else:
            print(f"Le répertoire {args.directory} n'existe pas.")

    # Lecture d'un fichier audio
    if args.play:
        if os.path.exists(args.play) and is_audio_file(args.play):
            play_audio(args.play)
        else:
            print(f"Fichier {args.play} non trouvé ou non valide.")

    # Modification des tags d'un fichier audio
    if args.set_tags and args.file:
        if os.path.exists(args.file) and is_audio_file(args.file):
            tags = {tag.split('=')[0]: tag.split('=')[1] for tag in args.set_tags if '=' in tag}
            modify_tags(args.file, title=tags.get('title'), artist=tags.get('artist'), album=tags.get('album'))
        else:
            print(f"Fichier {args.file} non trouvé ou non valide pour modification des tags.")

# Point d'entrée du programme
if __name__ == "__main__":
    main()
