from PyQt5 import QtCore, QtGui, QtWidgets
from modeGUI.API.spotify import SpotifyApp  # Import de l'application Spotify
from modeGUI.GUI.musicmanager import Ui_MainWindow as musicmanagerWindow  # Interface de gestion musicale
import cv2  # Pour la gestion des vidéos
from ffpyplayer.player import MediaPlayer  # Pour la lecture audio des vidéos
from PyQt5.QtWidgets import QMessageBox, QInputDialog  # Pour les boîtes de dialogue et les interactions utilisateur

class Ui_MainWindow(object):
    """
    Classe qui définit l'interface principale de l'application musicale.
    
    Cette classe est responsable de la configuration de l'interface graphique de l'application, 
    du gestionnaire de musique, de l'intégration avec Spotify et de la gestion des vidéos.
    """
    def setupUi(self, MainWindow):
        """
         Configure l'interface utilisateur principale de l'application.
        
        Paramètres:
        MainWindow (QMainWindow): La fenêtre principale de l'application.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(786, 600)  # Taille fixe de la fenêtre
        # Définir le style de la fenêtre avec une image de fond et une bordure
        MainWindow.setStyleSheet("QWidget {\n"
                                 "    background-image: url('src/library/images/music_back.png');\n"
                                 "    background-position: center; \n"
                                 "    background-repeat: no-repeat;\n"
                                 "    background-size: cover;\n"
                                 "    border: 1px solid #ADD8E6;\n"
                                 "}\n"
                                 "")
        # Définir l'icône de l'application
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/library/logo/music_icone.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Configuration du bouton "MUSIC MANAGER"
        self.PrimaryPushButton_2 = PrimaryPushButton(self.centralwidget)
        self.PrimaryPushButton_2.setGeometry(QtCore.QRect(550, 400, 201, 32))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PrimaryPushButton_2.setFont(font)
        self.PrimaryPushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PrimaryPushButton_2.setIcon(icon)
        self.PrimaryPushButton_2.setIconSize(QtCore.QSize(25, 25))
        self.PrimaryPushButton_2.setObjectName("PrimaryPushButton_2")
        # Lier le clic à la méthode d'ouverture de l'interface de gestion musicale
        self.PrimaryPushButton_2.clicked.connect(self.open_music_manager_interface)

        # Configuration du bouton "SPOTIFY"
        self.PrimaryPushButton_3 = PrimaryPushButton(self.centralwidget)
        self.PrimaryPushButton_3.setGeometry(QtCore.QRect(550, 350, 201, 32))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PrimaryPushButton_3.setFont(font)
        self.PrimaryPushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("src/library/logo/spotify.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PrimaryPushButton_3.setIcon(icon1)
        self.PrimaryPushButton_3.setIconSize(QtCore.QSize(25, 25))
        # Lier le clic à la méthode d'ouverture de l'interface Spotify
        self.PrimaryPushButton_3.clicked.connect(self.open_spotify_interface)
        self.PrimaryPushButton_3.setObjectName("PrimaryPushButton_3")

        # Configuration du bouton "HELP"
        self.PrimaryPushButton_4 = PrimaryPushButton(self.centralwidget)
        self.PrimaryPushButton_4.setGeometry(QtCore.QRect(680, 30, 101, 32))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PrimaryPushButton_4.setFont(font)
        self.PrimaryPushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PrimaryPushButton_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("src/library/logo/help.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PrimaryPushButton_4.setIcon(icon2)
        self.PrimaryPushButton_4.setIconSize(QtCore.QSize(25, 25))
        # Lier le clic à la méthode de lecture vidéo
        self.PrimaryPushButton_4.clicked.connect(self.play_video)
        self.PrimaryPushButton_4.setObjectName("PrimaryPushButton_4")

        # Ajouter une étiquette de copyright en bas
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 530, 341, 20))
        self.label.setStyleSheet("QWidget {\n"
                                 "    background-image: url('src/library/images/blanc.png');\n"
                                 "    background-position: center; \n"
                                 "    background-repeat: no-repeat;\n"
                                 "    background-size: cover;\n"
                                 "}\n"
                                 "")
        self.label.setObjectName("label")

        # Configuration des menus et de la barre d'état
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 786, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Initialisation de la traduction des textes
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Ajouter un événement personnalisé pour gérer la fermeture de la fenêtre
        MainWindow.closeEvent = self.closeEvent

    def retranslateUi(self, MainWindow):
        """
        Configure les textes affichés dans l'interface.
        
        Paramètres:
        MainWindow (QMainWindow): La fenêtre principale de l'application.
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Music App"))
        self.PrimaryPushButton_2.setText(_translate("MainWindow", "MUSIC MANAGER"))
        self.PrimaryPushButton_3.setText(_translate("MainWindow", " SPOTIFY"))
        self.PrimaryPushButton_4.setText(_translate("MainWindow", "HELP "))
        self.label.setText(_translate("MainWindow", "© 2024 - Projet universitaire - CY Cergy Paris Université"))

    def open_music_manager_interface(self):
        """
        Ouvre l'interface de gestion musicale.
        """
        self.second_window = QtWidgets.QMainWindow()
        self.ui = musicmanagerWindow()
        self.ui.setupUi(self.second_window)
        self.second_window.show()

    def open_spotify_interface(self):
        """
        Ouvre l'interface de l'application Spotify.
        """
        self.spotify_app = SpotifyApp()
        self.spotify_app.show()

    def play_video(self):
        """
        Propose à l'utilisateur de choisir une vidéo et lance sa lecture.
        """
        choice, ok = QInputDialog.getItem(
            None, "Choisissez une vidéo", "Sélectionnez une vidéo:",
            ["Demo Spotify", "Demo Music Manager"], 0, False
        )
        if ok:
            if choice == "Demo Spotify":
                video_path = r"src\library\videos\demo_spotify.mp4"
            elif choice == "Demo Music Manager":
                video_path = r"src\library\videos\demo_music_manager.mp4"
            self._play_selected_video(video_path)

    def _play_selected_video(self, video_path):
        """
        Lit une vidéo avec l'audio en utilisant OpenCV et ffpyplayer.
        """
        video = cv2.VideoCapture(video_path)
        player = MediaPlayer(video_path)
        width = 1000
        height = 850

        while True:
            grabbed, frame = video.read()
            audio_frame, val = player.get_frame()
            if not grabbed:
                print("End of video")
                break
            frame_resized = cv2.resize(frame, (width, height))
            cv2.imshow("Demo", frame_resized)
            key = cv2.waitKey(28) & 0xFF
            if key == ord("q"):
                break
            if val != 'eof' and audio_frame is not None:
                img, t = audio_frame

        video.release()
        cv2.destroyWindow("Demo")

    def closeEvent(self, event):
        """
        Gère la fermeture de la fenêtre avec confirmation utilisateur.
        """
        reply = QMessageBox.question(
            None, "Confirmation", 
            "Êtes-vous sûr de vouloir fermer Music App?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

from qfluentwidgets import PrimaryPushButton  # Bouton personnalisé
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
