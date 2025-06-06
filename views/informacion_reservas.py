"""Pantalla de informacion de reserva mostrada al cliente"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp

from Database.Data_Reservas import eliminar_reserva


class Informacion_Reserva_Screen(MDScreen):
    """Clase principal de la pantalla de Informacion de reserva mostrada al cliente"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "informacionreserva"
        self.reserva_actual = None
        self.dialog = None
        self.layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.layout.clear_widgets()
        self.mostrar_info()

    def mostrar_info(self):
        """Metodo que recibe y muestra la informacion de la reserva"""

        self.layout.clear_widgets()

        if not self.reserva_actual:
            self.layout.add_widget(
                MDLabel(text="No hay información para mostrar", halign="center")
            )
            return

        # --------Encabezado de la pantalla-------
        encabezado = MDCard(
            size_hint=(1, None),
            height=dp(250),
            radius=[0, 0, 20, 20],
            elevation=6,
            padding=0,
            orientation="vertical",
            md_bg_color="#01555100",
        )
        top_bar = MDTopAppBar(
            left_action_items=[["arrow-left", lambda x: self.volver()]],
            elevation=5,
            size_hint_y=None,
            height="40dp",
            md_bg_color=("#FFFFFF00"),
        )
        imagen = Image(
            source=self.reserva_actual["imagen"],
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
        )
        titulo = MDLabel(
            text="Informacion de la reserva",
            markup=True,
            font_style="H5",
            size_hint=(1, None),
            height=dp(40),
            pos_hint={"center_x": 0.5},
            theme_text_color="Primary",
            halign="center",
            valign="middle",
        )
        encabezado.add_widget(top_bar)
        encabezado.add_widget(imagen)
        encabezado.add_widget(titulo)
        self.layout.add_widget(encabezado)

        # --- Botones ---
        botones = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
            height=dp(50),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        cancelar_btn = MDRectangleFlatIconButton(
            text="cancelar",
            icon="delete",
            on_release=self.confirmar_cancelacion_reserva,
            size_hint=(1, None),
        )
        ir_btn = MDRectangleFlatIconButton(
            text="ir a mapa",
            icon="bus-marker",
            on_release=self.sitio_reserva,
            size_hint=(1, None),
        )
        botones.add_widget(cancelar_btn)
        botones.add_widget(ir_btn)

        self.layout.add_widget(botones)

        scroll_view = ScrollView()
        content_layout = MDBoxLayout(
            orientation="vertical", padding=10, size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter("height"))

        informacion_box = MDCard(
            orientation="vertical",
            padding=dp(10),
            height=dp(300),
            size_hint=(1, None),
            elevation=2,
            radius=[15],
        )
        razon_social_box = MDBoxLayout(orientation="horizontal", spacing=10)
        razon_social_box.add_widget(
            MDIcon(icon="office-building", size_hint=(None, None))
        )
        razon_social_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "razon_social",
                ),
                halign="left",
            )
        )
        nit_box = MDBoxLayout(orientation="horizontal", spacing=10)
        nit_box.add_widget(MDIcon(icon="numeric", size_hint=(None, None)))
        nit_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "nit",
                ),
                halign="left",
            )
        )
        admin_box = MDBoxLayout(orientation="horizontal", spacing=10)
        admin_box.add_widget(
            MDIcon(icon="account-box", size_hint=(None, None), size=(dp(24), dp(24)))
        )
        admin_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "administrador",
                ),
                halign="left",
            )
        )
        ubicacion_box = MDBoxLayout(orientation="horizontal", spacing=5)
        ubicacion_box.add_widget(
            MDIcon(icon="map-marker", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        ubicacion_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "ubicacion",
                ),
                halign="left",
            )
        )
        nombre_box = MDBoxLayout(orientation="horizontal", spacing=5)
        nombre_box.add_widget(
            MDIcon(icon="account", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        nombre_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "nombre_cliente",
                ),
                halign="left",
            )
        )
        telefono_box = MDBoxLayout(orientation="horizontal", spacing=5)
        telefono_box.add_widget(
            MDIcon(icon="cellphone", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        telefono_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "telefono_cliente",
                ),
                halign="left",
            )
        )
        correo_usuario_box = MDBoxLayout(orientation="horizontal", spacing=5)
        correo_usuario_box.add_widget(
            MDIcon(icon="email", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        correo_usuario_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "correo_cliente",
                ),
                halign="left",
            )
        )
        fecha_reserva_box = MDBoxLayout(orientation="horizontal", spacing=5)
        fecha_reserva_box.add_widget(
            MDIcon(icon="calendar-today", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        fecha_reserva_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "fecha_reserva",
                ),
                halign="left",
            )
        )
        hora_reserva_box = MDBoxLayout(orientation="horizontal", spacing=5)
        hora_reserva_box.add_widget(
            MDIcon(icon="calendar", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        hora_reserva_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get(
                    "hora_reserva",
                ),
                halign="left",
            )
        )
        informacion_box.add_widget(
            MDLabel(text="Informacion de servicio", halign="center", font_style="H6")
        )
        informacion_box.add_widget(razon_social_box)
        informacion_box.add_widget(nit_box)
        informacion_box.add_widget(admin_box)
        informacion_box.add_widget(ubicacion_box)
        informacion_box.add_widget(
            MDLabel(text="informacion del cliente", halign="center", font_style="H6")
        )
        informacion_box.add_widget(nombre_box)
        informacion_box.add_widget(telefono_box)
        informacion_box.add_widget(correo_usuario_box)
        informacion_box.add_widget(fecha_reserva_box)
        informacion_box.add_widget(hora_reserva_box)
        content_layout.add_widget(informacion_box)
        scroll_view.add_widget(content_layout)
        self.layout.add_widget(scroll_view)

    def cancelar_reserva(self, *args):
        """Metodo para cancelar la reserva"""

        id_usuario = self.reserva_actual["id_usuario"]
        eliminar = eliminar_reserva(id_usuario)
        # mensaje de exito en pantalla
        self.layout.clear_widgets()
        # dialogo de exito
        self.dialogo = MDDialog(
            title="Reserva Cancelada",
            text="La reserva ha sido cancelada exitosamente.",
            buttons=[
                MDRaisedButton(
                    text="Aceptar",
                    on_release=self.volver,
                    size_hint=(1, None),
                    height=dp(48),
                )
            ],
        )
        self.dialogo.open()

    def sitio_reserva(self, *args):
        """Metodo para ir al mapa que muestra la ubicacion del servicio"""

        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        pantalla_mapa = app.root.get_screen("mapascreen")
        pantalla_mapa.recibir_servicio(self.reserva_actual)
        app.root.current = "mapascreen"

    def confirmar_cancelacion_reserva(self, *args):
        """Dialogo de confirmacion de cancelacion de reserva"""

        if not self.dialog:
            self.dialog = MDDialog(
                title="¿Cancelar reserva?",
                text="¿Deseas cancelar la reserva de este servicio?",
                buttons=[
                    MDRaisedButton(text="Cancelar", on_release=self.cancelar_dialogo),
                    MDRaisedButton(text="Confirmar", on_release=self.cancelar_reserva),
                ],
            )
        self.dialog.open()

    def cancelar_dialogo(self, *args):
        """Cancelar dialogo de cancelacion de reserva"""

        self.dialog.dismiss()

    def volver(self, *args):
        self.manager.current = "pantallaUsuario"
