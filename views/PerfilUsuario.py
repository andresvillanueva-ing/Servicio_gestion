from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.toolbar import MDTopAppBar

class PerfilUsuario(MDScreen):
    def __init__(self, usuario, **kwargs):
        super().__init__(**kwargs)
        self.name = "perfil_usuario"
        self.usuario = usuario

        layout = MDBoxLayout(orientation='vertical')

        # TopAppBar con flecha para regresar
        top_bar = MDTopAppBar(
            title="Información del Usuario",
            left_action_items=[["arrow-left", lambda x: self.regresar()]]
        )

        lbl_nombre = MDLabel(
            text=f"Nombre: {self.usuario.get('nombre')}",
            halign="center"
        )
        lbl_email = MDLabel(
            text=f"Email: {self.usuario.get('correo')}",
            halign="center"
        )
        lbl_rol = MDLabel(
            text=f"telefono: {self.usuario.get('telefono')}",
            halign="center"
        )
        
        # Boton de cerrar sesión
        btn_cerrar_sesion = MDFlatButton(
            text="Cerrar sesión",
            pos_hint={"center_x": 0.5},
            on_release=self.cerrar_sesion
        )

        layout.add_widget(top_bar)
        layout.add_widget(lbl_nombre)
        layout.add_widget(lbl_email)
        layout.add_widget(lbl_rol)
        layout.add_widget(btn_cerrar_sesion)

        # Agregar el layout principal a la pantalla
        self.add_widget(layout)

    def regresar(self):
        # Lógica para regresar a la pantalla anterior
        self.manager.current = "pantallaPServicio"
        

    def cerrar_sesion(self, *args):
        # Lógica para cerrar sesión
        self.manager.current = "loginscreen"
        self.manager.transition.direction = "right"