from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivymd.uix.fitimage import FitImage
from Database.Data_sercivios import obtener_servicios_por_tipo

class TabParqueadero(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        servicios = obtener_servicios_por_tipo("parqueadero")

        if servicios:
            layout = MDBoxLayout(
                orientation="vertical",
                spacing=dp(10),
                padding=dp(10),
                size_hint_y=None,
            )
            layout.bind(minimum_height=layout.setter('height'))

            for servicio in servicios:
                card = MDCard(
                    orientation="horizontal",
                    size_hint=(1, None),
                    height=dp(150),
                    padding=dp(10),
                    spacing=dp(10),
                    ripple_behavior=True,
                    elevation=4,
                )

                # Imagen
                imagen = FitImage(
                    source=servicio["imagen"],
                    size_hint=(None, 1),
                    width=dp(100),
                    radius=[10, 0, 0, 10]
                )
                card.add_widget(imagen)

                # Información
                info_layout = MDBoxLayout(
                    orientation="vertical",
                    spacing=dp(5),
                    padding=(dp(10), 0),
                    size_hint=(0.6, 1),
                )
                info_layout.add_widget(MDLabel(text=f"Empresa: {servicio['razon_social']}", theme_text_color="Primary"))
                info_layout.add_widget(MDLabel(text=f"Administrador: {servicio['administrador']}", theme_text_color="Secondary"))
                info_layout.add_widget(MDLabel(text=f"Ubicación: {servicio['ubicacion']}", theme_text_color="Secondary"))
                card.add_widget(info_layout)

                # Botón Reservar
                boton = MDRaisedButton(
                    text="Reservar",
                    size_hint=(None, None),
                    size=(dp(100), dp(40)),
                    pos_hint={"center_y": 0.5},
                    on_release=lambda btn, s=servicio: self.reservar(s)
                )
                button_layout = MDBoxLayout(
                    size_hint=(None, 1),
                    width=dp(120),
                    padding=(dp(10), 0),
                    orientation='vertical'
                )
                button_layout.add_widget(boton)
                card.add_widget(button_layout)

                layout.add_widget(card)

            self.add_widget(layout)
        else:
            self.add_widget(MDLabel(text="No hay parqueaderos disponibles", halign="center"))


class TabRestaurante(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="No hay restaurantes disponibles", halign="center"))
    
class TabHotel(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text="No hay hoteles disponibles", halign="center"))

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

        tabs = MDTabs()
        tab1 = TabHotel()
        tab1.title = "Hoteles"
        tabs.add_widget(tab1)
        tab2 = TabParqueadero() 
        tab2.title = "Parqueaderos"
        tabs.add_widget(tab2)
        tab3 = TabRestaurante()
        tab3.title = "Restaurantes"
        tabs.add_widget(tab3)

        content_scroll = ScrollView()
        self.content_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )
        self.content_box.bind(minimum_height=self.content_box.setter('height'))
        content_scroll.add_widget(self.content_box)

        layout.add_widget(top_bar)
        layout.add_widget(tabs)

        self.add_widget(layout)

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