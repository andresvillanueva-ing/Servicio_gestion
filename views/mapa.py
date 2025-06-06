"""Pantalla del mapa"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.toolbar import MDTopAppBar
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.uix.label import MDIcon


class IconMarker(MapMarkerPopup):
    """Clase personalizada del icono de marcado de ubicacion"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (dp(48), dp(48))
        self.anchor = (0.5, 0.5)

        self.icon = MDIcon(
            icon="map-marker",
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            font_size=dp(32),
        )
        self.add_widget(self.icon)


class Mapa_Screen(MDScreen):
    """Clase Principal de la pantalla del mapa"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "mapascreen"
        self.layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        self.add_widget(self.layout)
        self.dialog = None
        self.datos_servicio = None
        self.map_view = None

    def on_pre_enter(self):
        """Metodo que se ejecuta antes de entrar a la pantalla"""
        self.layout.clear_widgets()

        # Agregar barra superior
        self.layout.add_widget(
            MDTopAppBar(
                title="Ubicación del Servicio",
                left_action_items=[["arrow-left", lambda x: self.volver()]],
                elevation=4,
            )
        )

        # Validar que haya datos
        if self.datos_servicio:
            try:
                ubicacion = self.datos_servicio.get("ubicacion", "")
                lat_str, lon_str = ubicacion.split(",")
                lat = float(lat_str.strip())
                lon = float(lon_str.strip())
            except Exception:
                lat, lon = 9.2419, -74.4262  # valores por defecto si hay error

            # Crear mapa
            self.map_view = MapView(zoom=16, lat=lat, lon=lon)

            # Crear marcador con ícono
            marcador = IconMarker(lat=lat, lon=lon)
            self.map_view.add_marker(marcador)

            self.layout.add_widget(self.map_view)

    def recibir_servicio(self, datos_servicio):
        """Metodo para recibir los datos del servicio a mostrar en el mapa"""

        self.datos_servicio = datos_servicio

    def volver(self, *args):
        self.manager.current = "informacionservicios"
