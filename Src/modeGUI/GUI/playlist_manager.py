# Importer la fonction create_xspf_playlist depuis le fichier modeCli.py.
# Cette fonction pourrait être utilisée pour créer une playlist XSPF.
from modeCli import create_xspf_playlist

import os  # Fournit des fonctionnalités pour interagir avec le système de fichiers.
import xml.etree.ElementTree as ET  # Permet de travailler avec des fichiers XML.

class PlaylistManager:
    """
    Classe pour gérer la création de playlists au format XSPF.
    """
    def create_xspf_playlist(self, audio_files, output_file='playlist.xspf'):
        """
        Génère une playlist XSPF à partir d'une liste de fichiers audio.
        
        :param audio_files: Liste des chemins des fichiers audio à inclure dans la playlist.
        :param output_file: Nom du fichier de sortie pour la playlist (par défaut 'playlist.xspf').
        """
        # Création de l'élément racine de la playlist avec les attributs nécessaires.
        playlist = ET.Element('playlist', version="1", xmlns="http://xspf.org/ns/0/")
        
        # Création d'un sous-élément trackList qui contiendra les pistes audio.
        tracklist = ET.SubElement(playlist, 'trackList')

        # Parcours de la liste des fichiers audio pour ajouter chaque fichier en tant que piste.
        for audio_file in audio_files:
            # Créer un élément track pour chaque fichier audio.
            track = ET.SubElement(tracklist, 'track')
            
            # Ajouter un sous-élément location pour spécifier le chemin du fichier audio.
            location = ET.SubElement(track, 'location')
            # Convertir le chemin du fichier en chemin absolu pour garantir sa validité.
            location.text = os.path.abspath(audio_file)

        # Créer l'arbre XML à partir de l'élément racine.
        tree = ET.ElementTree(playlist)
        # Écrire l'arbre XML dans le fichier de sortie avec l'encodage UTF-8 et une déclaration XML.
        tree.write(output_file, encoding='utf-8', xml_declaration=True)

        # Afficher un message pour confirmer que la playlist a été générée.
        print(f"Playlist générée: {output_file}")
