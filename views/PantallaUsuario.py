from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication

class PantallaUsuario(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Datos del Usuario")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Etiquetas para mostrar los datos del usuario
        lbl_titulo = QLabel("Información del Usuario")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold;")

        lbl_nombre = QLabel(f"Nombre: {self.usuario.get('nombre', 'N/A')}")
        lbl_email = QLabel(f"Email: {self.usuario.get('email', 'N/A')}")
        lbl_rol = QLabel(f"Rol: {self.usuario.get('rol', 'N/A')}")

        # Agregar etiquetas al layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_nombre)
        layout.addWidget(lbl_email)
        layout.addWidget(lbl_rol)

        self.setLayout(layout)

# Ejemplo de uso
if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Datos de ejemplo del usuario
    datos_usuario = {
        "nombre": "Andrés Pérez",
        "email": "andres.perez@example.com",
        "rol": "Administrador"
    }

    pantalla = PantallaUsuario(datos_usuario)
    pantalla.show()

    sys.exit(app.exec_())