from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.app import App

class PantallaUsuario(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantalla_usuario"
        self.app = App.get_running_app()

        layout = MDBoxLayout(orientation="vertical")

        top_bar = MDTopAppBar(
            title="SmartBooking",
            elevation=4,
            md_bg_color=(0.2, 0.2, 0.8, 1),
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            right_action_items=[["account", lambda x: self.abrir_perfil()]]
        )

        content_scroll = ScrollView()
        self.content_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )
        self.content_box.bind(minimum_height=self.content_box.setter('height'))
        content_scroll.add_widget(self.content_box)

        self.tabs_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(56),
            spacing=dp(5),
            padding=[dp(5), dp(5), dp(5), dp(5)]
        )

        self.hotel_btn = MDRaisedButton(
            text="   Hotel   ",
            size_hint_x=1,
            md_bg_color=(1, 1, 1, 1),
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1",
            elevation=0,
            line_color=(0.2, 0.2, 0.8, 1),
            radius=[10, 10, 10, 10],
            on_release=lambda x: self.cambiar_tab("hotel")
        )

        self.parqueadero_btn = MDRaisedButton(
            text="Parqueadero",
            size_hint_x=1,
            md_bg_color=(0.2, 0.2, 0.8, 1),
            text_color=(1, 1, 1, 1),
            font_style="Subtitle1",
            elevation=0,
            line_color=(0.2, 0.2, 0.8, 1),
            radius=[10, 10, 10, 10],
            on_release=lambda x: self.cambiar_tab("parqueadero")
        )

        self.restaurante_btn = MDRaisedButton(
            text="Restaurante",
            size_hint_x=1,
            md_bg_color=(1, 1, 1, 1),
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1",
            elevation=0,
            line_color=(0.2, 0.2, 0.8, 1),
            radius=[10, 10, 10, 10],
            on_release=lambda x: self.cambiar_tab("restaurante")
        )

        self.tabs_layout.add_widget(self.hotel_btn)
        self.tabs_layout.add_widget(self.parqueadero_btn)
        self.tabs_layout.add_widget(self.restaurante_btn)

        self.content_box.add_widget(self.tabs_layout)

        bottom_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            spacing=dp(10),
            padding=[dp(10), dp(5), dp(10), dp(5)]
        )

        self.servicios_btn = MDRaisedButton(
            text="Servicios",
            size_hint_x=0.5,
            md_bg_color=(1, 1, 1, 1),
            text_color=(0, 0, 0, 1),
            on_release=lambda x: self.cambiar_vista("servicios")
        )

        self.reservas_btn = MDRaisedButton(
            text="Reserva",
            size_hint_x=0.5,
            md_bg_color=(0.2, 0.2, 0.8, 1),
            on_release=lambda x: self.cambiar_vista("reservas")
        )

        bottom_bar.add_widget(self.servicios_btn)
        bottom_bar.add_widget(self.reservas_btn)

        layout.add_widget(top_bar)
        layout.add_widget(content_scroll)
        layout.add_widget(bottom_bar)

        self.add_widget(layout)

        self.tab_actual = "hotel"
        self.vista_actual = "servicios"

        if not hasattr(self.app, 'reservas_usuario'):
            self.app.reservas_usuario = []

        self.cargar_hoteles()

    def cambiar_tab(self, tab):
        self.hotel_btn.md_bg_color = (1, 1, 1, 1)
        self.hotel_btn.text_color = (0, 0, 0, 1)
        self.parqueadero_btn.md_bg_color = (1, 1, 1, 1)
        self.parqueadero_btn.text_color = (0, 0, 0, 1)
        self.restaurante_btn.md_bg_color = (1, 1, 1, 1)
        self.restaurante_btn.text_color = (0, 0, 0, 1)

        if tab == "hotel":
            self.hotel_btn.md_bg_color = (0.2, 0.2, 0.8, 1)
            self.hotel_btn.text_color = (1, 1, 1, 1)
            self.cargar_hoteles()
        elif tab == "parqueadero":
            self.parqueadero_btn.md_bg_color = (0.2, 0.2, 0.8, 1)
            self.parqueadero_btn.text_color = (1, 1, 1, 1)
            self.cargar_parqueaderos()
        elif tab == "restaurante":
            self.restaurante_btn.md_bg_color = (0.2, 0.2, 0.8, 1)
            self.restaurante_btn.text_color = (1, 1, 1, 1)
            self.cargar_restaurantes()

        self.tab_actual = tab

    def cambiar_vista(self, vista):
        if vista == "servicios":
            self.servicios_btn.md_bg_color = (0.2, 0.2, 0.8, 1)
            self.servicios_btn.text_color = (1, 1, 1, 1)
            self.reservas_btn.md_bg_color = (1, 1, 1, 1)
            self.reservas_btn.text_color = (0, 0, 0, 1)
            self.tabs_layout.opacity = 1
            self.cambiar_tab(self.tab_actual)
        else:
            self.reservas_btn.md_bg_color = (0.2, 0.2, 0.8, 1)
            self.reservas_btn.text_color = (1, 1, 1, 1)
            self.servicios_btn.md_bg_color = (1, 1, 1, 1)
            self.servicios_btn.text_color = (0, 0, 0, 1)
            self.tabs_layout.opacity = 0
            self.cargar_reservas()

        self.vista_actual = vista

    def cargar_hoteles(self):
        self.content_box.clear_widgets()
        self.content_box.add_widget(self.tabs_layout)

        hoteles = [
            {"nombre": "Nombre del Hotel", "admin": "Administrador", "ubicacion": "Ubicación", "imagen": "hotel.png"},
        ]

        for hotel in hoteles:
            self.agregar_card_servicio(hotel)

    def cargar_parqueaderos(self):
        self.content_box.clear_widgets()
        self.content_box.add_widget(self.tabs_layout)

        parqueaderos = [
            {"nombre": "Nombre del Parqueadero", "admin": "Administrador", "ubicacion": "Ubicación", "imagen": "parking.png"},
        ]

        for parqueadero in parqueaderos:
            self.agregar_card_servicio(parqueadero)

    def cargar_restaurantes(self):
        self.content_box.clear_widgets()
        self.content_box.add_widget(self.tabs_layout)

        restaurantes = [
            {"nombre": "Nombre del Restaurante", "admin": "Administrador", "ubicacion": "Ubicación", "imagen": "restaurant.png"},
        ]

        for restaurante in restaurantes:
            self.agregar_card_servicio(restaurante)

    def cargar_reservas(self):
        self.content_box.clear_widgets()

        if not self.app.reservas_usuario:
            self.content_box.add_widget(
                MDLabel(
                    text="No hay reservas actualmente",
                    halign="center",
                    valign="middle",
                    size_hint_y=None,
                    height=dp(400)
                )
            )
            return

        for reserva in self.app.reservas_usuario:
            self.agregar_card_reserva(reserva)

    def agregar_card_servicio(self, servicio):
        card = MDCard(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(100),
            padding=dp(10),
            spacing=dp(10),
            radius=[5, 5, 5, 5],
            elevation=1,
            md_bg_color=(1, 1, 1, 1)
        )

        img = Image(
            source=servicio["imagen"],
            size_hint=(None, None),
            size=(dp(70), dp(70))
        )

        info_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2),
            size_hint_x=0.7
        )

        nombre_lbl = MDLabel(text=servicio["nombre"], size_hint_y=None, height=dp(20))
        admin_lbl = MDLabel(text="Administrador", font_style="Caption", size_hint_y=None, height=dp(20))
        ubicacion_lbl = MDLabel(text="Ubicación", font_style="Caption", size_hint_y=None, height=dp(20))

        info_box.add_widget(nombre_lbl)
        info_box.add_widget(admin_lbl)
        info_box.add_widget(ubicacion_lbl)

        reservar_btn = MDRaisedButton(
            text="Reservar",
            md_bg_color=(0.2, 0.2, 0.8, 1),
            on_release=lambda x, s=servicio: self.reservar_servicio(s)
        )

        card.add_widget(img)
        card.add_widget(info_box)
        card.add_widget(reservar_btn)

        self.content_box.add_widget(card)

    def agregar_card_reserva(self, reserva):
        card = MDCard(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(100),
            padding=dp(10),
            spacing=dp(10),
            radius=[5, 5, 5, 5],
            elevation=1,
            md_bg_color=(1, 1, 1, 1)
        )

        img = Image(
            source=reserva["imagen"],
            size_hint=(None, None),
            size=(dp(70), dp(70))
        )

        info_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2),
            size_hint_x=0.7
        )

        nombre_lbl = MDLabel(text=reserva["nombre"], size_hint_y=None, height=dp(20))
        admin_lbl = MDLabel(text="Administrador", font_style="Caption", size_hint_y=None, height=dp(20))
        ubicacion_lbl = MDLabel(text="Ubicación", font_style="Caption", size_hint_y=None, height=dp(20))

        info_box.add_widget(nombre_lbl)
        info_box.add_widget(admin_lbl)
        info_box.add_widget(ubicacion_lbl)

        ir_btn = MDRaisedButton(
            text="Ir",
            md_bg_color=(0.2, 0.2, 0.8, 1),
            on_release=lambda x, r=reserva: self.ver_detalle_reserva(r)
        )

        card.add_widget(img)
        card.add_widget(info_box)
        card.add_widget(ir_btn)

        self.content_box.add_widget(card)

    def reservar_servicio(self, servicio):
        if servicio not in self.app.reservas_usuario:
            self.app.reservas_usuario.append(servicio)
            self.cambiar_vista("reservas")

    def ver_detalle_reserva(self, reserva):
        print(f"Ver detalles de la reserva: {reserva['nombre']}")

    def volver_atras(self):
        self.manager.current = "loginscreen"

    def abrir_perfil(self):
        if self.manager.has_screen("perfil_usuario"):
            self.manager.current = "perfil_usuario"
        else:
            print("Pantalla de perfil no encontrada")