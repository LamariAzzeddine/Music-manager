from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import PrimaryPushButton, SearchLineEdit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 611)  # Taille fixe de la fenêtre
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"src/library/logo/spotify.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        
        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Barre de recherche
        self.SearchLineEdit = SearchLineEdit(self.centralwidget)
        self.SearchLineEdit.setObjectName("SearchLineEdit")
        self.SearchLineEdit.setPlaceholderText("Rechercher sur Spotify...")
        self.verticalLayout.addWidget(self.SearchLineEdit)
        
        # Zone de texte pour les résultats
        self.result_text = QtWidgets.QLabel(self.centralwidget)
        self.result_text.setStyleSheet("background-color: white; padding: 20px;")
        self.result_text.setObjectName("result_text")
        self.result_text.setWordWrap(True)
        self.result_text.setText("La musique donne une âme à nos cœurs et des ailes à la pensée. -Platon")
        self.verticalLayout.addWidget(self.result_text)
        
        # Image de l'album
        self.album_image = QtWidgets.QLabel(self.centralwidget)
        self.album_image.setStyleSheet("background-color: white;")
        self.album_image.setObjectName("album_image")
        self.album_image.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.album_image)
        
        # Boutons de navigation et action
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        
        # Bouton précédent
       
        self.previous_button = PrimaryPushButton(self.centralwidget)
        self.previous_button.setObjectName("previous_button")
        self.previous_button.setText("Précédent")
        self.buttonLayout.addWidget(self.previous_button)
        
        # Bouton écouter
        self.listen_button = PrimaryPushButton(self.centralwidget)
        self.listen_button.setObjectName("listen_button")
        self.listen_button.setText("Écouter")
        self.buttonLayout.addWidget(self.listen_button)
        
        # Bouton suivant
        self.next_button = PrimaryPushButton(self.centralwidget)
        self.next_button.setObjectName("next_button")
        self.next_button.setText("Suivant")
        self.buttonLayout.addWidget(self.next_button)
        
        self.verticalLayout.addLayout(self.buttonLayout)

        # Ajouter l'icône pour le bouton précédent
        previous_icon = QtGui.QIcon()
        previous_icon.addPixmap(QtGui.QPixmap(r"src/library/logo/previous.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previous_button.setIcon(previous_icon)

# Ajouter l'icône pour le bouton suivant
        next_icon = QtGui.QIcon()
        next_icon.addPixmap(QtGui.QPixmap(r"src/library/logo/next.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_button.setIcon(next_icon)

        # Ajouter l'icône pour le bouton écouter
        listen_icon = QtGui.QIcon()
        listen_icon.addPixmap(QtGui.QPixmap(r"src/library/logo/play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.listen_button.setIcon(listen_icon)


        
        # Définir le widget central
        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
