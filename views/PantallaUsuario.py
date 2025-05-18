from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.metrics import dp
from Database.Data_sercivios import obtener_servicios_por_tipo
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.tab import MDTabs

class TabHotel(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Hotel"
        self.build_ui()

    def build_ui(self, ):
        servicios = obtener_servicios_por_tipo("Hotel")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        for servicio in servicios:
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4)

            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"], bold=True))
            datos.add_widget(MDLabel(text="Administrador"))
            datos.add_widget(MDLabel(text="Ubicación"))
            card.add_widget(datos)

            boton = MDRaisedButton(text="Reservar", md_bg_color=(0.3, 0.3, 1, 1),
                                   pos_hint={"center_y": 0.5})
            card.add_widget(boton)

            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

class TabParqueadero(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Parqueadero"
        self.build_ui()

    def build_ui(self):
        servicios = obtener_servicios_por_tipo("Parqueadero")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        for servicio in servicios:
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4)

            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"], bold=True))
            datos.add_widget(MDLabel(text="Administrador"))
            datos.add_widget(MDLabel(text="Ubicación"))
            card.add_widget(datos)

            boton = MDRaisedButton(text="Reservar", md_bg_color=(0.3, 0.3, 1, 1),
                                   pos_hint={"center_y": 0.5})

            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

class TabRestaurante(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Restaurante"
        self.build_ui()

    def build_ui(self):
        servicios = obtener_servicios_por_tipo("Restaurante")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        for servicio in servicios:
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4)

            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"], bold=True))
            datos.add_widget(MDLabel(text="Administrador"))
            datos.add_widget(MDLabel(text="Ubicación"))
            card.add_widget(datos)

            boton = MDRaisedButton(text="Reservar", md_bg_color=(0.3, 0.3, 1, 1),
                                   pos_hint={"center_y": 0.5})
            card.add_widget(boton)

            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)


class Pantalla_Usuario(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantallaUsuario"
        self.build_ui()

    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')

        # Top bar
        main_layout.add_widget(self.create_top_bar())

        # Navegación inferior
        bottom_nav = MDBottomNavigation(panel_color=(1, 1, 1, 1))

        bottom_nav.add_widget(self.Servicios_tab())
        bottom_nav.add_widget(self.Reservas_tab())

        main_layout.add_widget(bottom_nav)
        self.add_widget(main_layout)

    def create_top_bar(self):
        return MDTopAppBar(
            title="Usuario",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            right_action_items=[["account", lambda x: self.abrir_usuario()]],
            elevation=5,
            size_hint_y=None,
            height="56dp"
        )
    
    def Servicios_tab(self):
        tab = MDBottomNavigationItem(name="servicios", text="Servicios", icon="home")

        layout = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp"
        )

         # Crear tabs y añadirlos
        tabs = MDTabs()

        tabs.add_widget(TabHotel())
        tabs.add_widget(TabParqueadero())
        tabs.add_widget(TabRestaurante())

        layout.add_widget(tabs)
        tab.add_widget(layout)
        return tab

    def reservas_tab(self):
        tab = MDBottomNavigationItem(name="servicios", text="reservas", icon="home")
        layout = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp"
        )
        tab.add_widget(layout)
        return tab