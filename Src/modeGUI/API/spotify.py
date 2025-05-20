import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, QCompleter, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QStringListModel
from .Ui_spotify_app2 import Ui_MainWindow  # Interface générée
from base64 import b64encode
import webbrowser

# Vos identifiants d'API Spotify
CLIENT_ID = '1d3fbcfe9c4a4c7ea401fca22cf051d6'
CLIENT_SECRET = '26a24436778b41f2adcaa3f7eb63c6bf'


class SpotifyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.search_results = []
        self.current_index = 0

      

        # Initialiser le QCompleter pour les suggestions
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.SearchLineEdit.setCompleter(self.completer)

        # Ajout d'une liste déroulante pour choisir le type de recherche
        self.search_type_combo = QComboBox(self)
        self.search_type_combo.addItems(["Album", "Chanson"])
        self.ui.verticalLayout.insertWidget(0, self.search_type_combo)

        # Connecter les interactions
        self.ui.SearchLineEdit.textChanged.connect(self.on_search)
        self.ui.previous_button.clicked.connect(self.prev_result)
        self.ui.next_button.clicked.connect(self.next_result)
        self.ui.listen_button.clicked.connect(self.listen_track)

        # Ajouter une icône de loupe pour la recherche
        search_action = QAction(self)
        search_action.triggered.connect(self.on_search)
        self.ui.SearchLineEdit.addAction(search_action, self.ui.SearchLineEdit.TrailingPosition)

        # Afficher une image par défaut
        self.display_default_image()

    def display_default_image(self):
        """Affiche une image par défaut à l'ouverture."""
        default_image_path = "src/library/images/musique.png"  # Chemin de l'image par défaut
        pixmap = QPixmap(default_image_path)
        if not pixmap.isNull():
            self.ui.album_image.setPixmap(pixmap)
            self.ui.album_image.setScaledContents(True)
        else:
            self.ui.result_text.setText("Image par défaut non trouvée.")

    def get_access_token(self):
        """Récupère un token d'accès pour l'API Spotify."""
        auth_header = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")).decode("utf-8")
        url = "https://accounts.spotify.com/api/token"
        data = {'grant_type': 'client_credentials'}
        headers = {'Authorization': f'Basic {auth_header}'}

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération du token: {response.status_code}")
            return None

    def search_spotify(self, term):
        """Effectue une recherche Spotify avec un terme donné."""
        token = self.get_access_token()
        if token is None:
            return

        # Déterminer le type de recherche (album ou chanson)
        search_type = "album" if self.search_type_combo.currentText() == "Album" else "track"
        url = f'https://api.spotify.com/v1/search?q={term}&type={search_type}&limit=20'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Récupérer uniquement les éléments pertinents
            self.search_results = data.get(f'{search_type}s', {}).get('items', [])

            # Mettre à jour les suggestions
            suggestions = [item['name'] for item in self.search_results]
            self.completer.setModel(QStringListModel(suggestions))

            if self.search_results:
                self.current_index = 0
                self.show_result(self.current_index)
            else:
                self.ui.result_text.setText("Aucun résultat trouvé.")
        else:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la recherche Spotify: {response.status_code}")

    def show_album_details(self, album):
        """Affiche les informations complètes d’un album."""
        album_name = album['name']
        artist = ", ".join([artist['name'] for artist in album['artists']])
        release_date = album['release_date']
        total_tracks = album['total_tracks']
        url_spotify = album['external_urls']['spotify']
        image_url = album['images'][0]['url'] if album.get('images') else None

        # Télécharger et afficher l'image de l'album
        if image_url:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_data = image_response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.ui.album_image.setPixmap(pixmap)
                self.ui.album_image.setScaledContents(True)
            else:
                self.ui.album_image.clear()

        # Afficher les informations de l'album
        self.ui.result_text.setText(
            f"Album: {album_name}\n"
            f"Artiste(s): {artist}\n"
            f"Date de sortie: {release_date}\n"
            f"Total des morceaux: {total_tracks}\n\n"
            f"Lien Spotify: {url_spotify}"
        )
        self.ui.listen_button.setProperty('url', url_spotify)

    def show_track_details(self, track):
        """Affiche les informations complètes d’un morceau."""
        track_name = track['name']
        artist = ", ".join([artist['name'] for artist in track['artists']])
        album = track['album']['name']
        duration_ms = track['duration_ms']
        duration_min, duration_sec = divmod(duration_ms // 1000, 60)
        url_spotify = track['external_urls']['spotify']
        image_url = track['album']['images'][0]['url'] if track['album'].get('images') else None

        # Télécharger et afficher l'image de l'album associé
        if image_url:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_data = image_response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.ui.album_image.setPixmap(pixmap)
                self.ui.album_image.setScaledContents(True)
            else:
                self.ui.album_image.clear()

        # Afficher les informations de la chanson
        self.ui.result_text.setText(
            f"Titre: {track_name}\n"
            f"Artiste(s): {artist}\n"
            f"Album: {album}\n"
            f"Durée: {duration_min}:{duration_sec:02d}\n\n"
            f"Lien Spotify: {url_spotify}"
        )
        self.ui.listen_button.setProperty('url', url_spotify)

    def show_result(self, index):
        """Affiche le résultat à un index spécifique."""
        if index < len(self.search_results):
            item = self.search_results[index]

            # Vérifier le type de l'élément (chanson ou album)
            if 'duration_ms' in item:  # Si c'est une chanson
                self.show_track_details(item)
            elif 'release_date' in item:  # Si c'est un album
                self.show_album_details(item)
        else:
            QMessageBox.information(self, "Fin des résultats", "Il n'y a plus de résultats.")

    def prev_result(self):
        """Affiche le résultat précédent."""
        if self.current_index - 1 >= 0:
            self.current_index -= 1
            self.show_result(self.current_index)
        else:
            QMessageBox.information(self, "Début des résultats", "Il n'y a pas de résultats précédents.")

    def next_result(self):
        """Affiche le résultat suivant dans la liste."""
        if self.current_index + 1 < len(self.search_results):
            self.current_index += 1
            self.show_result(self.current_index)
        else:
            QMessageBox.information(self, "Fin", "Aucun autre résultat.")

    def listen_track(self):
        """Ouvre le lien Spotify pour écouter la piste ou album sélectionné."""
        button = self.sender()
        url = button.property('url')
        if url:
            webbrowser.open(url)
        else:
            QMessageBox.warning(self, "Erreur", "Aucun lien Spotify disponible.")

    def on_search(self):
        """Effectue une recherche d'album ou de chanson lorsque l'utilisateur modifie le texte."""
        term = self.ui.SearchLineEdit.text().strip()
        if term:
            self.search_spotify(term)
        else:
            self.ui.result_text.setText("")  # Efface les résultats si le champ est vide


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SpotifyApp()
    main_window.show()
    sys.exit(app.exec_())