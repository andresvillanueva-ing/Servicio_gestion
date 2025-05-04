from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

class PantallaUsuario(MDScreen):
    def __init__(self, usuario, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantalla_usuario"
        self.usuario = usuario
        self.init_ui()

    def init_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        lbl_titulo = MDLabel(
            text="Información del Usuario",
            halign="center",
            font_style="H5"
        )

        lbl_nombre = MDLabel(
            text=f"Nombre: {self.usuario.get('nombre')}",
            halign="center"
        )
        lbl_email = MDLabel(
            text=f"Email: {self.usuario.get('email')}",
            halign="center"
        )
        lbl_rol = MDLabel(
            text=f"Rol: {self.usuario.get('rol')}",
            halign="center"
        )

        layout.add_widget(lbl_titulo)
        layout.add_widget(lbl_nombre)
        layout.add_widget(lbl_email)
        layout.add_widget(lbl_rol)

        self.add_widget(layout)

# Ejemplo de uso dentro de una app KivyMD
class TestApp(MDApp):
    def build(self):
        datos_usuario = {
            "nombre": "Andrés Pérez",
            "email": "andres.perez@example.com",
            "rol": "Administrador"
        }
        return PantallaUsuario(datos_usuario)

if __name__ == "__main__":
    TestApp().run()
