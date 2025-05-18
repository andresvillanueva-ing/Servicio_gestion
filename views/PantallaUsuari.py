
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
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from Database.Data_sercivios import obtener_servicios_por_tipo


# Clase base reutilizable para representar cada tab con servicios
class BaseTab(FloatLayout, MDTabsBase):
    def __init__(self, tipo, reservar_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = tipo.capitalize()

        servicios = obtener_servicios_por_tipo()

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        for servicio in servicios:
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4)

            #img = Image(source="paisaje.png", size_hint=(None, None), size=(dp(80), dp(80)))
            #card.add_widget(img)

            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"], bold=True))
            datos.add_widget(MDLabel(text="Administrador"))
            datos.add_widget(MDLabel(text="Ubicación"))
            card.add_widget(datos)

            boton = MDRaisedButton(text="Reservar", md_bg_color=(0.3, 0.3, 1, 1),
                                   pos_hint={"center_y": 0.5},
                                   on_release=lambda x, s=servicio: reservar_callback(s))
            card.add_widget(boton)

            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

class TabHotel(BaseTab):
    def __init__(self, reservar_callback, **kwargs):
        super().__init__('hotel', reservar_callback, **kwargs)

class TabParqueadero(BaseTab):
    def __init__(self, reservar_callback, **kwargs):
        super().__init__('parqueadero', reservar_callback, **kwargs)

class TabRestaurante(BaseTab):
    def __init__(self, reservar_callback, **kwargs):
        super().__init__('restaurante', reservar_callback, **kwargs)

class PantallaServicios(MDScreen):
    def __init__(self, cambiar_pantalla, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantalla_servicios"
        self.reservas = []

        layout = MDBoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(title="SmartBooking", elevation=4,
                                   md_bg_color=(0.2, 0.2, 0.8, 1),
                                   left_action_items=[["arrow-left", lambda x: cambiar_pantalla("login")]],
                                   right_action_items=[["account", lambda x: print("Perfil")]])

        self.tabs = MDTabs()
        self.tabs.add_widget(TabHotel(self.reservar_servicio))
        self.tabs.add_widget(TabParqueadero(self.reservar_servicio))
        self.tabs.add_widget(TabRestaurante(self.reservar_servicio))

        # Bottom Navigation
        bottom_nav = MDBottomNavigation()

        tab_servicios = MDBottomNavigationItem(name='servicios', text='Servicios', icon='home')
        tab_reservas = MDBottomNavigationItem(name='reservas', text='Reservas', icon='calendar')

        tab_servicios.bind(on_tab_press=lambda x: cambiar_pantalla("pantalla_servicios"))
        tab_reservas.bind(on_tab_press=lambda x: cambiar_pantalla("reservas"))

        bottom_nav.add_widget(tab_servicios)
        bottom_nav.add_widget(tab_reservas)

        layout.add_widget(self.toolbar)
        layout.add_widget(self.tabs)
        layout.add_widget(bottom_nav)
        self.add_widget(layout)

    def reservar_servicio(self, servicio):
        if servicio not in self.reservas:
            self.reservas.append(servicio)
            print(f"Servicio reservado: {servicio['razon_social']}")

class PantallaReservas(MDScreen):
    def __init__(self, cambiar_pantalla, servicios=[], **kwargs):
        super().__init__(**kwargs)
        self.name = "reservas"
        self.servicios = servicios

        layout = MDBoxLayout(orientation="vertical")

        toolbar = MDTopAppBar(title="Servicios reservados", elevation=4,
                              md_bg_color=(0.2, 0.2, 0.8, 1),
                              left_action_items=[["arrow-left", lambda x: cambiar_pantalla("pantalla_servicios")]],
                              right_action_items=[["account", lambda x: print("Perfil")]])
        layout.add_widget(toolbar)

        self.scroll = ScrollView()
        self.lista = MDBoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter('height'))
        self.scroll.add_widget(self.lista)

        # Bottom Navigation
        bottom_nav = MDBottomNavigation()

        tab_servicios = MDBottomNavigationItem(name='servicios', text='Servicios', icon='home')
        tab_reservas = MDBottomNavigationItem(name='reservas', text='Reservas', icon='calendar')

        tab_servicios.bind(on_tab_press=lambda x: cambiar_pantalla("pantalla_servicios"))
        tab_reservas.bind(on_tab_press=lambda x: cambiar_pantalla("reservas"))

        bottom_nav.add_widget(tab_servicios)
        bottom_nav.add_widget(tab_reservas)

        layout.add_widget(self.scroll)
        layout.add_widget(bottom_nav)

        self.add_widget(layout)

    def on_pre_enter(self):
        self.lista.clear_widgets()
        for servicio in self.servicios:
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4)

            #img = Image(source="paisaje.png", size_hint=(None, None), size=(dp(80), dp(80)))
            #card.add_widget(img)

            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"], bold=True))
            datos.add_widget(MDLabel(text="Administrador"))
            datos.add_widget(MDLabel(text="Ubicación"))
            card.add_widget(datos)

            boton = MDRaisedButton(text="Ir", md_bg_color=(0.3, 0.3, 1, 1),
                                   pos_hint={"center_y": 0.5})
            card.add_widget(boton)

            self.lista.add_widget(card)





