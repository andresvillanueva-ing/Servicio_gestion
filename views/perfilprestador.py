from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp

class Perfilprestador(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "perfil_prestador"
        self.prestador = None

        self.layout = MDBoxLayout(orientation='vertical')
        self.top_bar = MDTopAppBar(
            title="Información del Usuario",
            left_action_items=[["arrow-left", lambda x: self.regresar()]]
        )
        self.layout.add_widget(self.top_bar)
        self.informacion_usuario = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            height=dp(300),
            size_hint=(1, None),
            radius=[15],
        )
        self.label_nombre = MDLabel(text="[b]Nombre del usuario:[/b]",halign="left", markup=True)
        self.lbl_nombre = MDLabel(halign="left")
        self.label_email = MDLabel(text="[b]Correo del usuario:[/b]",halign="left",markup=True)
        self.lbl_email = MDLabel(halign="left")
        self.label_telefono = MDLabel(text="[b]Telefono del usuario:[/b]",halign="left",markup=True)
        self.lbl_telefono = MDLabel(halign="left")
        self.caja_botones = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            height=dp(300),
            size_hint=(1, None),
        )

        btn_Modificar = MDTextButton(
            text="Modificar datos",
            pos_hint={"center_x": 0.5},
            text_color=(1, 0, 0, 1),  
            on_release=self.modificar_datos
        )
        btn_eliminar = MDTextButton(
            text="Eliminar Cuenta",
            pos_hint={"center_x": 0.5},
            text_color=(1, 0, 0, 1),  # Rojo, RGBA
            on_release=self.eliminar_cuenta
        )
        btn_cerrar_sesion = MDTextButton(
            text="Cerrar Sesion",
            pos_hint={"center_x": 0.5},
            text_color=(1, 0, 0, 1),  # Rojo, RGBA
            on_release=self.cerrar_sesion
        )

        self.informacion_usuario.add_widget(self.label_nombre)
        self.informacion_usuario.add_widget(self.lbl_nombre)
        self.informacion_usuario.add_widget(self.label_email)
        self.informacion_usuario.add_widget(self.lbl_email)
        self.informacion_usuario.add_widget(self.label_telefono)
        self.informacion_usuario.add_widget(self.lbl_telefono)
        self.layout.add_widget(self.informacion_usuario)
        self.caja_botones.add_widget(btn_Modificar)
        self.caja_botones.add_widget(btn_eliminar)
        self.caja_botones.add_widget(btn_cerrar_sesion)
        self.layout.add_widget(self.caja_botones)

        self.add_widget(self.layout)


    def set_prestador(self, usuario):
        self.prestador = usuario
        self.lbl_nombre.text = f"Nombre: {usuario['nombre']}"
        self.lbl_email.text = f"Email: {usuario['correo']}"
        self.lbl_telefono.text = f"Teléfono: {usuario['telefono']}"

    def modificar_datos(self, *args):
        modificar_screen = self.manager.get_screen("modificar_prestador")
        modificar_screen.set_datos_prestador(self.prestador)
        self.manager.current = "modificar_prestador"

    def eliminar_cuenta(self):
        pass

    def cerrar_sesion(self, *args):
        self.manager.current = "loginscreen"
        self.manager.transition.direction = "right"

    def regresar(self):
        self.manager.current = "pantallaPServicio"  
