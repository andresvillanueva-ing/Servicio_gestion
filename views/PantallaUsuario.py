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
from kivy.app import App
from kivymd.uix.fitimage import FitImage
from Database.Data_sercivios import obtener_servicios_por_tipo
import os

# Crear carpeta temporal si no existe
if not os.path.exists("temp"):
    os.makedirs("temp")

def guardar_imagen_temp(imagen_bytes, nombre_archivo):
    ruta = os.path.join("temp", nombre_archivo)
    with open(ruta, "wb") as archivo:
        archivo.write(imagen_bytes)
    return ruta

class TabParqueadero(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        servicios = obtener_servicios_por_tipo("parqueadero")
        if servicios:
            for servicio in servicios:
                ruta_imagen = guardar_imagen_temp(servicio["imagen"], f"{servicio['razon_social']}.png") if servicio["imagen"] else ""

                card = MDCard(
                    orientation="horizontal",
                    size_hint=(None, None),
                    size=(dp(350), dp(150)),
                    padding=dp(10),
                    ripple_behavior=True,
                    elevation=4,
                    pos_hint={"center_x": 0.5}
                )

                # Imagen a la izquierda
                if ruta_imagen:
                    imagen = FitImage(
                        source=ruta_imagen,
                        size_hint=(None, None),
                        size=(dp(100), dp(100))
                    )
                    card.add_widget(imagen)

                # Info en el centro
                info_layout = MDBoxLayout(orientation="vertical", padding=dp(10), spacing=dp(5))
                info_layout.add_widget(MDLabel(text=servicio["razon_social"], font_style="H6", halign="left"))
                info_layout.add_widget(MDLabel(text=f"Administrador: {servicio['administrador']}", halign="left"))
                info_layout.add_widget(MDLabel(text=f"Ubicación: {servicio['ubicacion']}", halign="left"))
                card.add_widget(info_layout)

                # Botón a la derecha
                boton_reservar = MDIconButton(
                    icon="calendar-check",
                    pos_hint={"center_y": 0.5},
                    on_release=lambda x, nombre=servicio["razon_social"]: self.reservar(nombre)
                )
                card.add_widget(boton_reservar)

                self.add_widget(card)
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