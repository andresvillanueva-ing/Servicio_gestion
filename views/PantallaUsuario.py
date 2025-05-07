# Importaciones necesarias de KivyMD y Kivy
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView 
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDRectangleFlatButton

# Función que simula la obtención de datos de servicios por tipo
def obtener_servicios_por_tipo(tipo):
    return [
        {
            "razon_social": f"{tipo.capitalize()} Ejemplo {i+1}",
            "administrador": f"Admin {i+1}",
            "ubicacion": f"Ubicación {i+1}",
            "imagen": None
        } for i in range(1)
    ]

# Clase base reutilizable para representar cada tab con servicios
class BaseTab(FloatLayout, MDTabsBase):
    def __init__(self, tipo, reservar_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = tipo.capitalize()  # Título del tab

        servicios = obtener_servicios_por_tipo(tipo)  # Obtener servicios simulados

        layout_scroll = ScrollView(size_hint=(1, 1))  # Área scrollable
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        for servicio in servicios:
            # Crear una tarjeta para cada servicio
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4)

            # Imagen del servicio
            img = Image(source="paisaje.png", size_hint=(None, None), size=(dp(80), dp(80)))
            card.add_widget(img)

            # Datos del servicio
            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"], bold=True))
            datos.add_widget(MDLabel(text="Administrador"))
            datos.add_widget(MDLabel(text="Ubicación"))
            card.add_widget(datos)

            # Botón para reservar el servicio
            boton = MDRaisedButton(text="Reservar", md_bg_color=(0.3, 0.3, 1, 1),
                                   pos_hint={"center_y": 0.5},
                                   on_release=lambda x, s=servicio: reservar_callback(s))
            card.add_widget(boton)

            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

# Clases para cada tipo de servicio, heredando de la clase base
class TabHotel(BaseTab):
    def __init__(self, reservar_callback, **kwargs):
        super().__init__('hotel', reservar_callback, **kwargs)

class TabParqueadero(BaseTab):
    def __init__(self, reservar_callback, **kwargs):
        super().__init__('parqueadero', reservar_callback, **kwargs)

class TabRestaurante(BaseTab):
    def __init__(self, reservar_callback, **kwargs):
        super().__init__('restaurante', reservar_callback, **kwargs)

# Pantalla principal donde se muestran los tabs de servicios
class PantallaServicios(MDScreen):
    def __init__(self, cambiar_pantalla, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantalla_servicios"
        self.reservas = []  # Lista para guardar los servicios reservados

        layout = MDBoxLayout(orientation="vertical")

        # Barra superior con título y botones
        self.toolbar = MDTopAppBar(title="SmartBooking", elevation=4,
                                   md_bg_color=(0.2, 0.2, 0.8, 1),
                                   left_action_items=[["arrow-left", lambda x: cambiar_pantalla("login")]],
                                   right_action_items=[["account", lambda x: print("Perfil")]])

        # Tabs para cada categoría de servicio
        self.tabs = MDTabs()
        self.tabs.add_widget(TabHotel(self.reservar_servicio))
        self.tabs.add_widget(TabParqueadero(self.reservar_servicio))
        self.tabs.add_widget(TabRestaurante(self.reservar_servicio))

        # Botones inferiores de navegación
        botones = MDBoxLayout(size_hint_y=None, height=dp(60), padding=dp(10), spacing=dp(10))
        botones.add_widget(MDRectangleFlatButton(text="Servicios", on_release=lambda x: None))
        botones.add_widget(MDRectangleFlatButton(text="Reserva", on_release=lambda x: cambiar_pantalla("reservas")))

        # Agregar componentes a la pantalla
        layout.add_widget(self.toolbar)
        layout.add_widget(self.tabs)
        layout.add_widget(botones)
        self.add_widget(layout)

    # Método para agregar un servicio a las reservas
    def reservar_servicio(self, servicio):
        if servicio not in self.reservas:
            self.reservas.append(servicio)
            print(f"Servicio reservado: {servicio['razon_social']}")

# Pantalla para mostrar los servicios que el usuario ha reservado
class PantallaReservas(MDScreen):
    def __init__(self, cambiar_pantalla, servicios=[], **kwargs):
        super().__init__(**kwargs)
        self.name = "reservas"
        self.servicios = servicios  # Servicios reservados

        layout = MDBoxLayout(orientation="vertical")

        # Barra superior
        toolbar = MDTopAppBar(title="Servicios reservados", elevation=4,
                              md_bg_color=(0.2, 0.2, 0.8, 1),
                              left_action_items=[["arrow-left", lambda x: cambiar_pantalla("pantalla_servicios")]],
                              right_action_items=[["account", lambda x: print("Perfil")]])
        layout.add_widget(toolbar)

        # Lista scrollable de servicios reservados
        self.scroll = ScrollView()
        self.lista = MDBoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter('height'))
        self.scroll.add_widget(self.lista)

        # Botones inferiores
        botones = MDBoxLayout(size_hint_y=None, height=dp(60), padding=dp(10), spacing=dp(10))
        botones.add_widget(MDRectangleFlatButton(text="Servicios", on_release=lambda x: cambiar_pantalla("pantalla_servicios")))
        botones.add_widget(MDRectangleFlatButton(text="Reservas", on_release=lambda x: None))

        layout.add_widget(self.scroll)
        layout.add_widget(botones)

        self.add_widget(layout)

    # Método llamado automáticamente al entrar a esta pantalla
    def on_pre_enter(self):
        self.lista.clear_widgets()  # Limpia la lista para evitar duplicados
        for servicio in self.servicios:
            # Crear tarjeta por cada reserva
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4)

            img = Image(source="paisaje.png", size_hint=(None, None), size=(dp(80), dp(80)))
            card.add_widget(img)

            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"], bold=True))
            datos.add_widget(MDLabel(text="Administrador"))
            datos.add_widget(MDLabel(text="Ubicación"))
            card.add_widget(datos)

            boton = MDRaisedButton(text="Ir", md_bg_color=(0.3, 0.3, 1, 1),
                                   pos_hint={"center_y": 0.5})
            card.add_widget(boton)

            self.lista.add_widget(card)

# Clase principal de la aplicación
class SmartBookingApp(MDApp):
    def build(self):
        self.sm = MDScreenManager()
        # Crear pantallas y compartir las reservas entre ellas
        self.pantalla_servicios = PantallaServicios(self.cambiar_pantalla)
        self.pantalla_reservas = PantallaReservas(self.cambiar_pantalla, self.pantalla_servicios.reservas)

        self.sm.add_widget(self.pantalla_servicios)
        self.sm.add_widget(self.pantalla_reservas)
        return self.sm

    # Método para cambiar entre pantallas
    def cambiar_pantalla(self, nombre):
        if nombre == "reservas":
            self.pantalla_reservas.servicios = self.pantalla_servicios.reservas
            self.pantalla_reservas.on_pre_enter()
        self.sm.current = nombre

# Ejecutar la aplicación
SmartBookingApp().run()