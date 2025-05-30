from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import  MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from Database.Data_Reservas import eliminar_reserva

from kivy.metrics import dp

class Informacion_Reserva_Screen(MDScreen):
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
        self.layout.clear_widgets()

        if not self.reserva_actual:
            self.layout.add_widget(MDLabel(text="No hay información para mostrar", halign="center"))
            return
        
        self.topapp = MDTopAppBar(
            title="",
            left_action_items=[["arrow-left", lambda x: self.volver()]],
            elevation=4,
            pos_hint={"top": 1},
            specific_text_color="#FFFFFF"
        )
        self.layout.add_widget(self.topapp)

        #--------Encabezado de la pantalla-------
        encabezado = MDCard(
            size_hint=(1, 1),
            height=dp(260),
            radius=[0, 0, 20, 20],
            elevation=6,
            padding=0,
            orientation="vertical",
            md_bg_color="#015551",
        )
        imagen = Image(
            source=self.reserva_actual['imagen'],
            size_hint=(1,1),
            allow_stretch=True,
            keep_ratio=False
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

        encabezado.add_widget(imagen)
        encabezado.add_widget(titulo)
        self.layout.add_widget(encabezado)

        botones = MDBoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, None),
            height=dp(60),
            padding =(dp(20), 0)
        )
        cancelar_btn = MDRaisedButton(
            text="Reservar",
            icon="calendar-plus",
            on_release=self.confirmar_cancelacion_reserva,
            size_hint=(1, None),
        )
        ir_btn = MDRaisedButton(
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
            orientation="vertical", padding=10, spacing=10, size_hint_y=None
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
                text=self.reserva_actual.get("razon_social",), halign="left"
            )
        )
        nit_box = MDBoxLayout(orientation="horizontal", spacing=10)
        nit_box.add_widget(
            MDIcon(icon="numeric", size_hint=(None, None))
        )
        nit_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get("nit",), halign="left"
            )
        )
        admin_box = MDBoxLayout(orientation="horizontal", spacing=10)
        admin_box.add_widget(
            MDIcon(icon="account-box", size_hint=(None, None), size=(dp(24), dp(24)))
        )
        admin_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get("administrador",), halign="left"
            )
        )
        ubicacion_box = MDBoxLayout(orientation="horizontal", spacing=5)
        ubicacion_box.add_widget(
            MDIcon(icon="map-marker", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        ubicacion_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get("ubicacion",), halign="left"
            )
        )
        nombre_box = MDBoxLayout(orientation="horizontal", spacing=5)
        nombre_box.add_widget(
            MDIcon(icon="account", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        nombre_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get("nombre_cliente",), halign="left"
            )
        )
        telefono_box = MDBoxLayout(orientation="horizontal", spacing=5)
        telefono_box.add_widget(
            MDIcon(icon="cellphone", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        telefono_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get("telefono_cliente",), halign="left"
            )
        )
        correo_box = MDBoxLayout(orientation="horizontal", spacing=5)
        correo_box.add_widget(
            MDIcon(icon="email", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        correo_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get("correo_cliente",), halign="left"
            )
        )
        fecha_reserva_box = MDBoxLayout(orientation="horizontal", spacing=5)
        fecha_reserva_box.add_widget(
            MDIcon(icon="calendar-today", size_hint=(1, None), size=(dp(24), dp(24)))
        )
        fecha_reserva_box.add_widget(
            MDLabel(
                text=self.reserva_actual.get("fecha_reserva",), halign="left"
            )
        )
        informacion_box.add_widget(MDLabel(text="Informacion de servicio", halign="center", font_style="H6"))
        informacion_box.add_widget(razon_social_box)
        informacion_box.add_widget(nit_box)
        informacion_box.add_widget(admin_box)
        informacion_box.add_widget(ubicacion_box)
        informacion_box.add_widget(MDLabel(text="informacion del cliente", halign="center", font_style="H6"))
        informacion_box.add_widget(nombre_box)
        informacion_box.add_widget(telefono_box)
        informacion_box.add_widget(correo_box)
        informacion_box.add_widget(fecha_reserva_box)
        content_layout.add_widget(informacion_box)
        scroll_view.add_widget(content_layout)
        self.layout.add_widget(scroll_view)

    def cancelar_reserva(self, *args):
        id_usuario = self.reserva_actual['id_usuario']
        eliminar = eliminar_reserva(id_usuario)
        self.dialog.dismiss()
            # mensaje de exito en pantalla
        self.layout.clear_widgets()
            # dialogo de exito
        self.dialogo = MDDialog(
            title="Reserva Cancelada",
            text="La reserva ha sido cancelada exitosamente.",
            buttons=[
                MDRaisedButton(
                    text="Aceptar", on_release=self.volver, size_hint=(1, None), height=dp(48)
                )
            ]
        )
        self.dialogo.open()

    def sitio_reserva(self):
        pass

    def confirmar_cancelacion_reserva(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                title="¿Cancelar reserva?",
                text="¿Deseas realizar cancelacion de la reserva de este servicio?",
                buttons=[
                    MDRaisedButton(text="Cancelar", on_release=self.cancelar_dialogo),
                    MDRaisedButton(text="Confirmar", on_release=self.cancelar_reserva),
                ],
            )
        self.dialog.open()

    def cancelar_dialogo(self, *args):
        self.dialog.dismiss()

    def volver(self, *args):
        self.manager.current = "pantallaUsuario"
