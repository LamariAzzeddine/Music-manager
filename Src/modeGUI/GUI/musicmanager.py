
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pygame
import threading
from .audio_manager import AudioManager
from .playlist_manager import PlaylistManager
from PIL import Image, ImageTk
import io
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget  # Ajoutez QListWidget ici
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PIL import Image
import cv2
from ffpyplayer.player import MediaPlayer       
from qfluentwidgets import PrimaryPushButton
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class Ui_MainWindow(object):
    """
    Cette classe définit l'interface utilisateur de l'application Music Manager.
    Elle permet de charger des fichiers audio, afficher des métadonnées,
    jouer des fichiers audio, générer des playlists et gérer l'interface graphique.
    """
    def setupUi(self, MainWindow):
        """
        Configure l'interface utilisateur du MainWindow.
        
        Initialise tous les éléments graphiques, les boutons, les étiquettes, 
        et connecte les signaux aux slots correspondants. Ce processus inclut 
        la configuration de la fenêtre, l'initialisation des composants audio 
        et la préparation des listes de musique.
        
        Args:
            MainWindow (QMainWindow): La fenêtre principale de l'application.
        """       
        self.playing_thread = None
        self.is_playing = False

        # Initialize audio_manager
        self.audio_manager = AudioManager()
        
        # Initialisez playlist_manager
        self.playlist_manager = PlaylistManager() 
        
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(834, 896)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"src\library\logo\musique.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setIconSize(QtCore.QSize(45, 45))
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.choixdudossier = PrimaryPushButton(self.centralwidget)
        self.choixdudossier.setGeometry(QtCore.QRect(380, 90, 191, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.choixdudossier.setFont(font)
        self.choixdudossier.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.choixdudossier.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(r"src\library\logo\dossier.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.choixdudossier.setIcon(icon1)
        self.choixdudossier.setIconSize(QtCore.QSize(30, 30))
        self.choixdudossier.setObjectName("choixdudossier")
        # Connexion du bouton "choixdudossier" à la fonction load_folder
        self.choixdudossier.clicked.connect(self.load_folder)
        self.Titrebienvenue = QtWidgets.QLabel(self.centralwidget)
        self.Titrebienvenue.setGeometry(QtCore.QRect(100, 20, 641, 51))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.Titrebienvenue.setFont(font)
        self.Titrebienvenue.setObjectName("Titrebienvenue")
        self.affichagemetadonnees = QtWidgets.QListWidget(self.centralwidget)
        self.affichagemetadonnees.setEnabled(True)
        self.affichagemetadonnees.setGeometry(QtCore.QRect(140, 290, 551, 131))
        self.affichagemetadonnees.setTabletTracking(False)
        self.affichagemetadonnees.setObjectName("affichagemetadonnees")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 90, 361, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 260, 331, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 660, 761, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.precedent = PrimaryPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.precedent.setFont(font)
        self.precedent.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(r"src\library\logo\previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.precedent.setIcon(icon2)
        self.precedent.setIconSize(QtCore.QSize(27, 27))
        self.precedent.setObjectName("precedent")
        self.precedent.clicked.connect(self.play_previous)
        self.horizontalLayout.addWidget(self.precedent)
        self.arreter = PrimaryPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.arreter.setFont(font)
        self.arreter.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(r"src\library\logo\pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arreter.setIcon(icon3)
        self.arreter.setIconSize(QtCore.QSize(26, 26))
        self.arreter.setObjectName("arreter")
        self.arreter.clicked.connect(self.stop_audio)
        self.horizontalLayout.addWidget(self.arreter)
        self.jouer = PrimaryPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.jouer.setFont(font)
        self.jouer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.jouer.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(r"src\library\logo\play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.jouer.setIcon(icon4)
        self.jouer.setIconSize(QtCore.QSize(27, 27))
        self.jouer.setObjectName("jouer")
        self.jouer.clicked.connect(self.play_audio)
        self.horizontalLayout.addWidget(self.jouer)
        self.suivant = PrimaryPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.suivant.setFont(font)
        self.suivant.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.suivant.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(r"src\library\logo\nextt.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.suivant.setIcon(icon5)
        self.suivant.setIconSize(QtCore.QSize(27, 27))
        self.suivant.setObjectName("suivant")
        self.suivant.clicked.connect(self.play_next)
        self.horizontalLayout.addWidget(self.suivant)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(70, 790, 711, 81))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 30)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fichiersplaylist = PrimaryPushButton(self.horizontalLayoutWidget_2)
        self.fichiersplaylist.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fichiersplaylist.setFont(font)
        self.fichiersplaylist.setObjectName("fichiersplaylist")
        self.fichiersplaylist.clicked.connect(self.select_audio_files)
        self.horizontalLayout_2.addWidget(self.fichiersplaylist)
        self.playlistspersonnalisee = PrimaryPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.playlistspersonnalisee.setFont(font)
        self.playlistspersonnalisee.setObjectName("playlistspersonnalisee")
        self.playlistspersonnalisee.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.playlistspersonnalisee.clicked.connect(self.generate_playlist)
        self.horizontalLayout_2.addWidget(self.playlistspersonnalisee)
        self.playlistpardefaut = PrimaryPushButton(self.horizontalLayoutWidget_2)
        self.playlistpardefaut.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.playlistpardefaut.setFont(font)
        self.playlistpardefaut.setObjectName("playlistpardefaut")
        self.playlistpardefaut.clicked.connect(self.generate_default_playlist)
        self.horizontalLayout_2.addWidget(self.playlistpardefaut)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(280, 740, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.affichelesmusiques = QtWidgets.QListWidget(self.centralwidget)
        self.affichelesmusiques.setGeometry(QtCore.QRect(140, 140, 541, 101))
        self.affichelesmusiques.setObjectName("affichelesmusiques")
        # Connexion du signal itemSelectionChanged à la méthode display_metadata
        self.affichelesmusiques.itemSelectionChanged.connect(self.display_metadata)
        self.cover_image_label = QtWidgets.QLabel(self.centralwidget)
        self.cover_image_label.setGeometry(QtCore.QRect(250, 450, 600, 200))
        self.cover_image_label.setText("")
        self.cover_image_label.setObjectName("cover_image_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 788, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Ajouter cette ligne pour lier la méthode closeEvent
        MainWindow.closeEvent = self.closeEvent

    def closeEvent(self, event):
        """
        Cette méthode est appelée lorsqu'on tente de fermer la fenêtre.
        Demande à l'utilisateur une confirmation avant de fermer l'application.
        
        Args:
            event (QCloseEvent): L'événement de fermeture de la fenêtre.
        """
        reply = QMessageBox.question(
            None, "Confirmation", 
            "Êtes-vous sûr de vouloir fermer Music Manager?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()  # Accepter la fermeture de la fenêtre
        else:
            event.ignore()  # Ignorer la fermeture de la fenêtre si l'utilisateur choisit Non

        
        if reply == QMessageBox.Yes:
            # Fermer proprement les threads ou arrêter les processus si nécessaire
            if self.playing_thread and self.playing_thread.is_alive():
                self.stop_audio()  # Appeler la fonction pour arrêter l'audio

            event.accept()  # Accepter la fermeture de la fenêtre
        else:
            event.ignore()  # Ignorer la fermeture de la fenêtre

    def retranslateUi(self, MainWindow):
        """
        Retraduction des textes de l'interface utilisateur après leur initialisation.
        
        Args:
            MainWindow (QMainWindow): La fenêtre principale de l'application.
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Music Manager"))
        self.choixdudossier.setText(_translate("MainWindow", "Charger un dossier  "))
        self.Titrebienvenue.setText(_translate("MainWindow", "Bienvenue dans le gestionnaire de musique "))
        self.label.setText(_translate("MainWindow", "Cliquez ici pour choisir votre musique: "))
        self.label_2.setText(_translate("MainWindow", "Métadonnées du morceau sellectionné "))
        self.precedent.setText(_translate("MainWindow", "  Précédent"))
        self.arreter.setText(_translate("MainWindow", "  Arrêter"))
        self.jouer.setText(_translate("MainWindow", "  Jouer"))
        self.suivant.setText(_translate("MainWindow", "Suivant  "))
        self.fichiersplaylist.setText(_translate("MainWindow", "Sélectionner des fichiers"))
        self.playlistspersonnalisee.setText(_translate("MainWindow", "Générer une playlist personnalisée"))
        self.playlistpardefaut.setText(_translate("MainWindow", "Générer une playlist par défaut"))
        self.label_3.setText(_translate("MainWindow", "Génération de Playlists"))
    
    
    def load_folder(self):
        """
        Charge un dossier et récupère les fichiers audio qu'il contient.
        Affiche les fichiers audio dans la liste des musiques disponibles.
        """
        folder = QFileDialog.getExistingDirectory(None, "Sélectionner un dossier")
        if folder:
            audio_files = self.audio_manager.explore_folder(folder)
            self.affichelesmusiques.clear()
            # Affichage des noms de fichiers dans le QListWidget
            for file_name, file_path in audio_files:
                self.affichelesmusiques.addItem(file_name)  # Ajouter seulement le nom du fichier
                # Vous pouvez stocker file_path si nécessaire pour y accéder plus tard
                self.affichelesmusiques.item(self.affichelesmusiques.count() - 1).setData(QtCore.Qt.UserRole, file_path)
                
                


    def play_audio(self):
        """
        Joue l'audio du fichier sélectionné dans la liste des musiques.
        Si un fichier est déjà en cours de lecture, il sera arrêté avant de commencer la nouvelle lecture.
        """
        selection = self.affichelesmusiques.selectedIndexes()
        if selection:
            file_path = self.affichelesmusiques.item(selection[0].row()).data(QtCore.Qt.UserRole)
            if self.is_playing:
                self.stop_audio()

            self.playing_thread = threading.Thread(target=self._play_audio_thread, args=(file_path,))
            self.playing_thread.start()
            self.is_playing = True

    def _play_audio_thread(self, file_path):
        """
        Fonction exécutée dans un thread pour jouer un fichier audio.
        
        Args:
            file_path (str): Le chemin du fichier audio à lire.
            
        Cette fonction utilise pygame pour charger et jouer le fichier audio
        dans un thread séparé, permettant à l'application de rester réactive pendant la lecture.
        """
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and self.is_playing:
                pass
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {file_path}: {e}")

    def stop_audio(self):
        """
        Arrête la lecture du fichier audio en cours.
        Si un fichier est en cours de lecture, il est stoppé, et le thread de lecture est terminé.
        """
        
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            if self.playing_thread:
                self.playing_thread.join()

    def display_metadata(self):
        """
        Affiche les métadonnées du fichier audio sélectionné dans la liste.
        Cette fonction est appelée chaque fois que l'utilisateur sélectionne un élément
        dans la liste des fichiers audio.
        
        La fonction extrait et affiche les métadonnées telles que le titre, l'artiste, 
        l'album, et la couverture de l'album (si disponible) dans l'interface graphique.
        """
        selected_item = self.affichelesmusiques.currentItem()  # Obtenir l'élément sélectionné
        if selected_item:
            
            file_path = selected_item.data(QtCore.Qt.UserRole) # Récupérer le chemin complet
            metadata = self.audio_manager.extract_metadata(file_path)  # Vous devez définir cette méthode dans AudioManager
            if metadata:
                self.affichagemetadonnees.clear()  # Effacer les anciennes métadonnées
                for key, value in metadata.items():  # Afficher les nouvelles métadonnées
                    self.affichagemetadonnees.addItem(f"{key}: {value}")
            else:
                self.affichagemetadonnees.addItem("Aucune métadonnée trouvée.")
                
            cover_image_data = self.audio_manager.get_cover_image(file_path)
            if cover_image_data:
                # Ouvrez l'image à partir des données binaires
                image = Image.open(io.BytesIO(cover_image_data))
                
                # Redimensionnez l'image
                image.thumbnail((150, 150))
                
                # Convertissez l'image en données binaires pour PyQt
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                qpixmap = QPixmap()
                qpixmap.loadFromData(img_byte_arr.getvalue(), "PNG")
                # Redimensionner l'image à la taille souhaitée
                qpixmap = qpixmap.scaled(340, 340, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                
                # Affichez l'image dans le QLabel
                self.cover_image_label.setPixmap(qpixmap)
            else:
                print(f"Aucune couverture trouvée pour {file_path}")
                # Si aucune couverture n'est trouvée, afficher une image par défaut
                default_image_path = r'src\library\images\no_image.jpg'  # Remplacez par le chemin de l'image par défaut
                default_image = QPixmap(default_image_path)
                default_image = default_image.scaled(340, 340, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.cover_image_label.setPixmap(default_image)
                    
            


    def play_next(self):
        """
        Joue la musique suivante dans la liste des musiques.
        Si la musique actuelle est la dernière, elle reste en cours de lecture.
        """
        current_selection = self.affichelesmusiques.currentRow()
        next_index = current_selection + 1
        if next_index < self.affichelesmusiques.count():
            self.affichelesmusiques.setCurrentRow(next_index)
            self.play_audio()

    def play_previous(self):
        """
        Joue la musique précédente dans la liste des musiques.
        Si la musique actuelle est la première, elle reste en cours de lecture.
        """
        current_selection = self.affichelesmusiques.currentRow()
        prev_index = current_selection - 1
        if prev_index >= 0:
            self.affichelesmusiques.setCurrentRow(prev_index)
            self.play_audio()
            

    def select_audio_files(self):
        """
        Permet à l'utilisateur de sélectionner plusieurs fichiers audio.
        Cette fonction met à jour la liste des fichiers audio sélectionnés
        et affiche les métadonnées du premier fichier sélectionné.
        """
        # Configurer le mode de sélection multiple
        self.affichelesmusiques.setSelectionMode(QListWidget.MultiSelection)
        
        # Récupérer les fichiers sélectionnés
        selected_items = self.affichelesmusiques.selectedItems()
        if selected_items:
            # Récupérer les noms des fichiers sélectionnés
            self.selected_files = [item.data(QtCore.Qt.UserRole) for item in selected_items]
            print(f"Fichiers sélectionnés : {self.selected_files}")
        else:
            print("Aucun fichier sélectionné dans la liste.")
        
        # Afficher les métadonnées du premier fichier sélectionné
        if self.select_audio_files:
            self.display_metadata()

    def generate_playlist(self):
        """
        Génère une playlist à partir des fichiers audio sélectionnés par l'utilisateur.
        La playlist est enregistrée sous un fichier XSPF spécifié par l'utilisateur.
        """
        if self.selected_files:
            print(f"Génération de la playlist avec les fichiers suivants : {self.selected_files}")
            output_file, _ = QFileDialog.getSaveFileName(
                            parent=None, 
                            caption="Enregistrer la playlist", 
                            directory="", 
                            filter="Fichiers XSPF (*.xspf)"
                                                        )

            if output_file:
                self.playlist_manager.create_xspf_playlist(self.selected_files, output_file)
                print(f"Playlist générée avec {len(self.selected_files)} fichiers.")
        else:
            print("Aucun fichier sélectionné pour générer la playlist.")
                

    def generate_default_playlist(self):
        """
        Génère une playlist par défaut avec tous les fichiers audio disponibles dans la liste.
        La playlist est enregistrée sous un fichier XSPF spécifié par l'utilisateur.
        """
        audio_files = [self.affichelesmusiques.item(i).data(QtCore.Qt.UserRole) for i in range(self.affichelesmusiques.count())]
        if audio_files:
            
            output_file, _ = QFileDialog.getSaveFileName(
                            parent=None, 
                            caption="Enregistrer la playlist", 
                            directory="", 
                            filter="Fichiers XSPF (*.xspf)"
                                                        )
            
            if output_file:
                self.playlist_manager.create_xspf_playlist(audio_files, output_file)
                print(f"Playlist par défaut générée avec {len(audio_files)} fichiers.")
        else:
            print("Aucun fichier audio dans le dossier.")
            
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())