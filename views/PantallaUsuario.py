from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
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
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage
import os


class TabHotel(FloatLayout, MDTabsBase):
    def __init__(self, parent_screen=None,**kwargs):
        super().__init__(**kwargs)
        self.title = "Hotel"
        self.icon = "city-variant"
        self.parent_screen = parent_screen
        self.build_ui()
        #color de fondo

    def build_ui(self, ):
        servicios = obtener_servicios_por_tipo("Hotel")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        for servicio in servicios:
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(130),
                          padding=dp(10), ripple_behavior=True, elevation=4, md_bg_color="#FFF2F26C")
            imagen=FitImage(
                source=servicio["imagen"],
                radius=[dp(75), dp(75), dp(75), dp(75)],  # Radios para los cuatro bordes (circular si alto=ancho)
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={"center_x": 0.5}
            )
            card.add_widget(imagen)
            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"].upper(), bold=True, font_style="H6", halign="center"))
            datos.add_widget(MDLabel(text="[b]Admin:[/b] " + servicio['administrador'], markup=True, font_style="Body2", font_size="16sp", theme_text_color="Custom"))
            datos.add_widget(MDLabel(text=f"[b]Ubicación:[/b] {servicio["ubicacion"]}", font_style="Body2", font_size="16sp",markup=True, theme_text_color="Custom"))
            datos.add_widget(MDLabel(text=f"[b]Puestos disponibles:[/b] {servicio["puestos"]}", font_style="Body2", font_size="16sp", markup=True, theme_text_color="Custom"))
            card.add_widget(datos)
            card.on_touch_up = lambda touch, servicio=servicio, card=card: self.mostrar_dialogo(servicio) if card.collide_point(*touch.pos) else None
            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

    def mostrar_dialogo(self, servicio):
        self.dialog = MDDialog(
            title="¿Ver información del servicio?",
            text=f"{servicio['razon_social']}\nAdministrador: {servicio['administrador']}",
            buttons=[
                MDFlatButton(
                     text="CANCELAR", 
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="VER",
                    on_release=lambda x: self.ir_a_informacion(servicio)
                ),
            ],
        )
        self.dialog.open()

    def ir_a_informacion(self, servicio):
        self.dialog.dismiss()
        if self.parent_screen and self.parent_screen.manager:
            sm = self.parent_screen.manager
            pantalla_info = sm.get_screen("informacionservicios")
            pantalla_info.servicio_actual = servicio  # asignar el servicio
            sm.current = "informacionservicios"


class TabParqueadero(FloatLayout, MDTabsBase):
    def __init__(self, parent_screen=None,**kwargs):
        super().__init__(**kwargs)
        self.title = "Parqueadero"
        self.icon= "car"
        self.parent_screen = parent_screen
        self.build_ui()
        #color de fondo
        

    def build_ui(self):
        servicios = obtener_servicios_por_tipo("Parqueadero")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        for servicio in servicios:
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4, md_bg_color="#FFF2F26C")
            imagen=FitImage(
                source=servicio["imagen"],
                radius=[dp(75), dp(75), dp(75), dp(75)],  # Radios para los cuatro bordes (circular si alto=ancho)
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={"center_x": 0.5}
            )
            card.add_widget(imagen)
            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"].upper(), bold=True, font_style="H6", halign="center"))
            datos.add_widget(MDLabel(text="[b]Admin:[/b] " + servicio['administrador'], markup=True, font_style="Body2", font_size="16sp", theme_text_color="Custom"))
            datos.add_widget(MDLabel(text=f"[b]Ubicación:[/b] {servicio["ubicacion"]}", font_style="Body2", font_size="16sp",markup=True, theme_text_color="Custom"))
            datos.add_widget(MDLabel(text=f"[b]Puestos disponibles:[/b] {servicio["puestos"]}", font_style="Body2", font_size="16sp", markup=True, theme_text_color="Custom"))
            card.add_widget(datos)

            card.on_touch_up = lambda touch, servicio=servicio, card=card: self.mostrar_dialogo(servicio) if card.collide_point(*touch.pos) else None
            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

    def mostrar_dialogo(self, servicio):
        self.dialog = MDDialog(
            title="¿Ver información del servicio?",
            text=f"{servicio['razon_social']}\nAdministrador: {servicio['administrador']}",
            buttons=[
                MDFlatButton(
                     text="CANCELAR", 
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="VER",
                    on_release=lambda x: self.ir_a_informacion(servicio)
                ),
            ],
        )
        self.dialog.open()

    def ir_a_informacion(self, servicio):
        self.dialog.dismiss()
        if self.parent_screen and self.parent_screen.manager:
            sm = self.parent_screen.manager
            pantalla_info = sm.get_screen("informacionservicios")
            pantalla_info.servicio_actual = servicio  # asignar el servicio
            sm.current = "informacionservicios"


class TabRestaurante(FloatLayout, MDTabsBase):
    def __init__(self, parent_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Restaurante"
        self.icon="chef-hat"
        self.parent_screen = parent_screen
        self.build_ui()
        #color de fondo
        md_bg_color="#FFF2F2"

    def build_ui(self):
        servicios = obtener_servicios_por_tipo("Restaurante")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        for servicio in servicios:
            card = MDCard(orientation="horizontal", size_hint_y=None, height=dp(120),
                          padding=dp(10), ripple_behavior=True, elevation=4, md_bg_color="#FFF2F26C")

            imagen=FitImage(
                source=servicio["imagen"],
                radius=[dp(75), dp(75), dp(75), dp(75)],  # Radios para los cuatro bordes (circular si alto=ancho)
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={"center_x": 0.5}
            )
            card.add_widget(imagen)
            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(MDLabel(text=servicio["razon_social"].upper(), bold=True, font_style="H6", halign="center"))
            datos.add_widget(MDLabel(text="[b]Admin:[/b] " + servicio['administrador'], markup=True, font_style="Body2", font_size="16sp", theme_text_color="Custom"))
            datos.add_widget(MDLabel(text=f"[b]Ubicación:[/b] {servicio["ubicacion"]}", font_style="Body2", font_size="16sp",markup=True, theme_text_color="Custom"))
            datos.add_widget(MDLabel(text=f"[b]Puestos disponibles:[/b] {servicio["puestos"]}", font_style="Body2", font_size="16sp", markup=True, theme_text_color="Custom"))
            card.add_widget(datos)
            card.on_touch_up = lambda touch, servicio=servicio, card=card: self.mostrar_dialogo(servicio) if card.collide_point(*touch.pos) else None
            
            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

    def mostrar_dialogo(self, servicio):
        self.dialog = MDDialog(
            title="¿Ver información del servicio?",
            text=f"Nombre del servicio: {servicio['razon_social']}\nAdministrador: {servicio['administrador']}",
            buttons=[
                MDFlatButton(
                     text="CANCELAR", 
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="VER",
                    on_release=lambda x: self.ir_a_informacion(servicio)
                ),
            ],
        )
        self.dialog.open()

    def ir_a_informacion(self, servicio):
        self.dialog.dismiss()
        if self.parent_screen and self.parent_screen.manager:
            sm = self.parent_screen.manager
            pantalla_info = sm.get_screen("informacionservicios")
            pantalla_info.servicio_actual = servicio  # asignar el servicio
            sm.current = "informacionservicios"
        
class Pantalla_Usuario(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantallaUsuario"
        self.build_ui()
        #color de fondo
        md_bg_color="#FFF2F2"

    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')

        # Top bar
        main_layout.add_widget(self.create_top_bar())

        # Navegación inferior
        bottom_nav = MDBottomNavigation(panel_color=("#02020262"))

        bottom_nav.add_widget(self.Servicios_tab())
        bottom_nav.add_widget(self.Reservas_tab())

        main_layout.add_widget(bottom_nav)
        self.add_widget(main_layout)

    def create_top_bar(self):
        return MDTopAppBar(
            title="ReservaFacil",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            right_action_items=[["account", lambda x: self.abrir_usuario()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
            md_bg_color="#015551"
        )
    
    def Servicios_tab(self):
        tab = MDBottomNavigationItem(name="servicios", text="Servicios", icon="home")

        layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp"
        )

         # Crear tabs y añadirlos
        tabs = MDTabs(
            md_bg_color="#FFF2F2",# Color de fondo de la barra de pestañas (Ejemplo: el mismo de la TopAppBar)
            indicator_color="#FF0000", # Color del indicador de la pestaña activa (Ejemplo: rojo vibrante)
            text_color_normal="#FFFFFF", # Color del texto/ícono de las pestañas inactivas (Ejemplo: blanco)
            text_color_active="#015551", # Color del texto/ícono de la pestaña activa (Ejemplo: amarillo)
            )

        tabs.add_widget(TabHotel(parent_screen=self))
        tabs.add_widget(TabParqueadero(parent_screen=self))
        tabs.add_widget(TabRestaurante(parent_screen=self))

        layout.add_widget(tabs)
        tab.add_widget(layout)
        return tab
    
    def Reservas_tab(self):
        tab = MDBottomNavigationItem(name="reservas", text="Reservas", icon="calendar")
        layout = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp"
        )

        layout.add_widget(MDLabel(text="En el momento no hay reservas", halign="center"))
        tab.add_widget(layout)
        return tab
    

    def volver_atras(self):
        self.manager.current = "loginscreen"

    def abrir_usuario(self):
        self.manager.current = "pantalla_usuario"

