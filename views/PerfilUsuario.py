from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar

class PerfilUsuario(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "perfil_usuario"
        self.usuario = None

        self.layout = MDBoxLayout(orientation='vertical')
        self.top_bar = MDTopAppBar(
            title="Información del Usuario",
            left_action_items=[["arrow-left", lambda x: self.regresar()]]
        )
        self.layout.add_widget(self.top_bar)

        self.lbl_nombre = MDLabel(halign="center")
        self.lbl_email = MDLabel(halign="center")
        self.lbl_telefono = MDLabel(halign="center")

        self.layout.add_widget(self.lbl_nombre)
        self.layout.add_widget(self.lbl_email)
        self.layout.add_widget(self.lbl_telefono)

        btn_cerrar_sesion = MDRaisedButton(
            text="Cerrar sesión",
            pos_hint={"center_x": 0.5},
            on_release=self.cerrar_sesion
        )
        self.layout.add_widget(btn_cerrar_sesion)

        self.add_widget(self.layout)

    def set_usuario(self, usuario):
        self.usuario = usuario
        self.lbl_nombre.text = f"Nombre: {usuario['nombre']}"
        self.lbl_email.text = f"Email: {usuario['correo']}"
        self.lbl_telefono.text = f"Teléfono: {usuario['telefono']}"

    def cerrar_sesion(self, *args):
        self.manager.current = "loginscreen"
        self.manager.transition.direction = "right"

    def regresar(self):
        self.manager.current = "pantalla_anterior"  # Ajusta el nombre si es necesario
