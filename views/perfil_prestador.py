"""Pantalla de perfil de prestador de servicio"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton, MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from Database.Data_P_Servicio import eliminar_prestador


class Perfilprestador(MDScreen):
    """Clase Principal de la pantalla de prestador de servicio"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "perfil_prestador"
        self.prestador = None

        # Layout principal
        self.layout = MDBoxLayout(orientation="vertical")
        self.add_widget(self.layout)

        # Barra superior
        self.top_bar = MDTopAppBar(
            title="Información del Usuario",
            left_action_items=[["arrow-left", lambda x: self.regresar()]],
            elevation=4,
        )
        self.layout.add_widget(self.top_bar)

        # Scroll para que funcione bien en pantallas pequeñas
        self.scroll = ScrollView()
        self.scroll_layout = MDBoxLayout(
            orientation="vertical", padding=dp(20), spacing=dp(20), size_hint_y=None
        )
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter("height"))
        self.scroll.add_widget(self.scroll_layout)

        # Sección de información del usuario
        self.informacion_usuario = MDBoxLayout(
            orientation="vertical", spacing=dp(10), size_hint=(1, None)
        )
        self.label_nombre = MDLabel(
            text="[b]Nombre del usuario:[/b]", halign="left", markup=True
        )
        self.lbl_nombre = MDLabel(halign="left")
        self.label_email = MDLabel(
            text="[b]Correo del usuario:[/b]", halign="left", markup=True
        )
        self.lbl_email = MDLabel(halign="left")
        self.label_telefono = MDLabel(
            text="[b]Teléfono del usuario:[/b]", halign="left", markup=True
        )
        self.lbl_telefono = MDLabel(halign="left")

        self.informacion_usuario.add_widget(self.label_nombre)
        self.informacion_usuario.add_widget(self.lbl_nombre)
        self.informacion_usuario.add_widget(self.label_email)
        self.informacion_usuario.add_widget(self.lbl_email)
        self.informacion_usuario.add_widget(self.label_telefono)
        self.informacion_usuario.add_widget(self.lbl_telefono)

        # Botones de acción
        self.caja_botones = MDBoxLayout(
            orientation="vertical", spacing=dp(10), size_hint=(1, None)
        )
        btn_Modificar = MDTextButton(
            text="Modificar datos",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            on_release=self.modificar_datos,
        )
        btn_eliminar = MDTextButton(
            text="Eliminar Cuenta",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            on_release=self.eliminar_cuenta,
        )
        btn_cerrar_sesion = MDTextButton(
            text="Cerrar Sesión",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            on_release=self.cerrar_sesion,
        )

        self.caja_botones.add_widget(btn_Modificar)
        self.caja_botones.add_widget(btn_eliminar)
        self.caja_botones.add_widget(btn_cerrar_sesion)

        # Agregar widgets al scroll
        self.scroll_layout.add_widget(self.informacion_usuario)
        self.scroll_layout.add_widget(self.caja_botones)

        # Añadir el scroll al layout principal
        self.layout.add_widget(self.scroll)

    def set_prestador(self, usuario):
        """Metodo que recibe los datos del prestador de servicio"""

        self.prestador = usuario
        self.lbl_nombre.text = f"{usuario['nombre']}"
        self.lbl_email.text = f"{usuario['correo']}"
        self.lbl_telefono.text = f"{usuario['telefono']}"

    def modificar_datos(self, *args):
        """Metodo para mostrar la pantalla de modificar datos del prestador de servicio."""

        modificar_screen = self.manager.get_screen("modificar_prestador")
        modificar_screen.set_datos_prestador(self.prestador)
        self.manager.current = "modificar_prestador"

    def eliminar_cuenta(self, *args):
        """Dialogo para confirmar la eliminacion de la cuenta"""

        self.dialog = MDDialog(
            title="¿Desea eliminar la cuenta?",
            buttons=[
                MDRaisedButton(
                    text="CANCELAR", on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Eliminar",
                    on_release=lambda x: self.eliminar_servicios(self.prestador),
                ),
            ],
        )
        self.dialog.open()

    def eliminar_servicios(self, prestador):
        """Metodo para eliminar la cuenta del prestador de servicio"""

        self.dialog.dismiss()
        try:
            eliminar_prestador(prestador.get("id"))
            print(prestador.get("id"))
            self.cerrar_sesion()
            from kivymd.uix.snackbar import Snackbar

            Snackbar(MDLabel(text="¡¡Cuenta eliminada con exito.!!")).open()
        except Exception as e:
            import traceback

            traceback.print_exc()

    def cerrar_sesion(self, *args):
        """Metodo para cerrar la sesion del prestador de servicio"""

        self.manager.current = "loginscreen"
        self.manager.transition.direction = "right"

    def regresar(self):
        self.manager.current = "pantallaPServicio"
