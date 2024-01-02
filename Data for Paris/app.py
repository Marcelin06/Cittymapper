import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QVBoxLayout, QPushButton
from paris.test_p import ParisWindow
from toulouse.test_t import ToulouseWindow

class CitySelectorDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sélection de la ville")
        self.setGeometry(150, 150, 400, 200)  # Définir la taille de la boîte de dialogue

        # Utilisation de feuilles de style pour définir les couleurs et autres propriétés
        self.setStyleSheet("""
            QDialog {
                background-color: #555; /* Gris foncé */
                color: white; /* Couleur du texte */
            }

            QComboBox {
                background-color: #777; /* Gris un peu plus foncé */
                color: white; /* Couleur du texte */
                border: 1px solid #777; /* Bordure */
                border-radius: 4px; /* Coins arrondis */
                padding: 2px;
            }

            QPushButton {
                background-color: #45a049; /* Vert légèrement plus foncé */
                color: white; /* Couleur du texte */
                border: 1px solid #45a049; /* Bordure */
                border-radius: 4px; /* Coins arrondis */
                padding: 5px 10px; /* Espacement du texte à l'intérieur du bouton */
            }
            
            QPushButton:hover {
                background-color: #357e3d; /* Changement de couleur au survol */
            }
        """)

        self.setLayout(QVBoxLayout())

        self.city_combobox = QComboBox()
        self.city_combobox.addItems(["Paris", "Toulouse"])
        self.layout().addWidget(self.city_combobox)

        confirm_button = QPushButton("Confirmer")
        confirm_button.clicked.connect(self.accept)
        self.layout().addWidget(confirm_button)

if __name__ == "__main__":
    app = QApplication([])

    city_selector_dialog = CitySelectorDialog()
    if city_selector_dialog.exec_() == QDialog.Accepted:
        selected_city = city_selector_dialog.city_combobox.currentText()

        if selected_city == "Paris":
            Paris_window = ParisWindow()
            Paris_window.show()
        elif selected_city == "Toulouse":
            toulouse_window = ToulouseWindow()
            toulouse_window.show()

    sys.exit(app.exec_())
