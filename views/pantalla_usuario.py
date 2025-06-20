"""Pantalla de cliente donde realiza las reservas y ve informacion."""

from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.app import App

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.fitimage import FitImage
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.tab import MDTabs
from kivymd.uix.dialog import MDDialog

from ..Database.Data_servicios import obtener_servicios_por_tipo
from ..Database.Data_Reservas import obtener_reservas_realizadas
from ..Database.Data_usuario import obtener_usuario


def formatear_ubicacion_decimal(ubicacion_str):
    """Formatea una cadena de ubicacion en forma de "latitud, longitud" a un formato legible."""

    try:
        lat_str, lon_str = ubicacion_str.split(",")
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())
        return f"Lat: {lat:.6f}, Lon: {lon:.6f}"
    except Exception as e:
        return "Ubicación inválida"


class TabHotel(FloatLayout, MDTabsBase):
    """Clase para crear la pantalla hotel en la pantalla de cliente."""

    def __init__(self, parent_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Hotel"
        self.icon = "city-variant"
        self.parent_screen = parent_screen
        self.build_ui()

    def build_ui(
        self,
    ):
        """Crea las cartas de los servicios de tipo Hoteles."""

        servicios = obtener_servicios_por_tipo("Hotel")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10), size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        for servicio in servicios:
            card = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(130),
                padding=dp(10),
                ripple_behavior=True,
                elevation=4,
                md_bg_color="#FFF2F26C",
            )
            imagen = FitImage(
                source=servicio["imagen"],
                radius=[
                    dp(75),
                    dp(75),
                    dp(75),
                    dp(75),
                ],  # Radios para los cuatro bordes (circular si alto=ancho)
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={"center_x": 0.5},
            )
            card.add_widget(imagen)
            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(
                MDLabel(
                    text=servicio["razon_social"].upper(),
                    bold=True,
                    font_style="H6",
                    halign="center",
                )
            )
            datos.add_widget(
                MDLabel(
                    text="[b]Admin:[/b] " + servicio["administrador"],
                    markup=True,
                    font_style="Body2",
                    font_size="16sp",
                    theme_text_color="Custom",
                )
            )
            ubicacion = formatear_ubicacion_decimal(servicio["ubicacion"])
            datos.add_widget(
                MDLabel(
                    text=f"[b]Ubicación:[/b] {ubicacion}",
                    font_style="Body2",
                    font_size="16sp",
                    markup=True,
                    theme_text_color="Custom",
                )
            )
            datos.add_widget(
                MDLabel(
                    text=f"[b]Puestos disponibles:[/b] {servicio["puestos"]}",
                    font_style="Body2",
                    font_size="16sp",
                    markup=True,
                    theme_text_color="Custom",
                )
            )
            card.add_widget(datos)
            card.bind(
                on_touch_up=lambda instance, touch, s=servicio: self.on_card_touch(
                    instance, touch, s
                )
            )
            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

    def on_card_touch(self, instance, touch, servicio):
        if instance.collide_point(*touch.pos):
            self.mostrar_dialogo(servicio)

    def mostrar_dialogo(self, servicio):

        self.dialog = MDDialog(
            title="¿Ver información del servicio?",
            text=f"{servicio['razon_social']}\nAdministrador: {servicio['administrador']}",
            buttons=[
                MDFlatButton(
                    text="CANCELAR", on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="VER", on_release=lambda x: self.ir_a_informacion(servicio)
                ),
            ],
        )
        self.dialog.open()

    def ir_a_informacion(self, servicio):
        """Dirige a la pantalla de informacion de servicio"""

        self.dialog.dismiss()
        if self.parent_screen and self.parent_screen.manager:
            sm = self.parent_screen.manager
            pantalla_info = sm.get_screen("informacionservicios")
            pantalla_info.servicio_actual = servicio  # asignar el servicio
            sm.current = "informacionservicios"


class TabParqueadero(FloatLayout, MDTabsBase):
    """Clase para crear la pantalla parqueadero en la pantalla de cliente."""

    def __init__(self, parent_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Parqueadero"
        self.icon = "car"
        self.parent_screen = parent_screen
        self.build_ui()
        # color de fondo

    def build_ui(self):
        """Crea las cartas de los servicios de tipo Parqueadero."""

        servicios = obtener_servicios_por_tipo("Parqueadero")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10), size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        for servicio in servicios:
            card = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(120),
                padding=dp(10),
                ripple_behavior=True,
                elevation=4,
                md_bg_color="#FFF2F26C",
            )
            imagen = FitImage(
                source=servicio["imagen"],
                radius=[
                    dp(75),
                    dp(75),
                    dp(75),
                    dp(75),
                ],  # Radios para los cuatro bordes (circular si alto=ancho)
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={"center_x": 0.5},
            )
            card.add_widget(imagen)
            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(
                MDLabel(
                    text=servicio["razon_social"].upper(),
                    bold=True,
                    font_style="H6",
                    halign="center",
                )
            )
            datos.add_widget(
                MDLabel(
                    text="[b]Admin:[/b] " + servicio["administrador"],
                    markup=True,
                    font_style="Body2",
                    font_size="16sp",
                    theme_text_color="Custom",
                )
            )
            ubicacion = formatear_ubicacion_decimal(servicio["ubicacion"])
            datos.add_widget(
                MDLabel(
                    text=f"[b]Ubicación:[/b] {ubicacion}",
                    font_style="Body2",
                    font_size="16sp",
                    markup=True,
                    theme_text_color="Custom",
                )
            )
            datos.add_widget(
                MDLabel(
                    text=f"[b]Puestos disponibles:[/b] {servicio["puestos"]}",
                    font_style="Body2",
                    font_size="16sp",
                    markup=True,
                    theme_text_color="Custom",
                )
            )
            card.add_widget(datos)

            card.bind(
                on_touch_up=lambda instance, touch, s=servicio: self.on_card_touch(
                    instance, touch, s
                )
            )

            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

    def on_card_touch(self, instance, touch, servicio):
        if instance.collide_point(*touch.pos):
            self.mostrar_dialogo(servicio)

    def mostrar_dialogo(self, servicio):
        """Dialogo para confirmar la vista de la informacion del servicio"""

        self.dialog = MDDialog(
            title="¿Ver información del servicio?",
            text=f"{servicio['razon_social']}\nAdministrador: {servicio['administrador']}",
            buttons=[
                MDFlatButton(
                    text="CANCELAR", on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="VER", on_release=lambda x: self.ir_a_informacion(servicio)
                ),
            ],
        )
        self.dialog.open()

    def ir_a_informacion(self, servicio):
        """Dirige a la pantalla de informacion de servicio"""

        self.dialog.dismiss()
        if self.parent_screen and self.parent_screen.manager:
            sm = self.parent_screen.manager
            pantalla_info = sm.get_screen("informacionservicios")
            pantalla_info.servicio_actual = servicio  # asignar el servicio
            sm.current = "informacionservicios"


class TabRestaurante(FloatLayout, MDTabsBase):
    """Clase para crear la pantalla de restaurante en la pantalla de clinete."""

    def __init__(self, parent_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Restaurante"
        self.icon = "chef-hat"
        self.parent_screen = parent_screen
        self.build_ui()
        # color de fondo
        self.md_bg_color = "#FFF2F2"

    def build_ui(self):
        """Crea las cartas de los servicios de tipo restaurante."""

        servicios = obtener_servicios_por_tipo("Restaurante")

        layout_scroll = ScrollView(size_hint=(1, 1))
        content = MDBoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10), size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        for servicio in servicios:
            card = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(120),
                padding=dp(10),
                ripple_behavior=True,
                elevation=4,
                md_bg_color="#FFF2F26C",
            )

            imagen = FitImage(
                source=servicio["imagen"],
                radius=[
                    dp(75),
                    dp(75),
                    dp(75),
                    dp(75),
                ],  # Radios para los cuatro bordes (circular si alto=ancho)
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={"center_x": 0.5},
            )
            card.add_widget(imagen)
            datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
            datos.add_widget(
                MDLabel(
                    text=servicio["razon_social"].upper(),
                    bold=True,
                    font_style="H6",
                    halign="center",
                )
            )
            datos.add_widget(
                MDLabel(
                    text="[b]Admin:[/b] " + servicio["administrador"],
                    markup=True,
                    font_style="Body2",
                    font_size="16sp",
                    theme_text_color="Custom",
                )
            )
            ubicacion = formatear_ubicacion_decimal(servicio["ubicacion"])
            datos.add_widget(
                MDLabel(
                    text=f"[b]Ubicación:[/b] {ubicacion}",
                    font_style="Body2",
                    font_size="16sp",
                    markup=True,
                    theme_text_color="Custom",
                )
            )
            datos.add_widget(
                MDLabel(
                    text=f"[b]Puestos disponibles:[/b] {servicio["puestos"]}",
                    font_style="Body2",
                    font_size="16sp",
                    markup=True,
                    theme_text_color="Custom",
                )
            )
            card.add_widget(datos)
            card.bind(
                on_touch_up=lambda instance, touch, s=servicio: self.on_card_touch(
                    instance, touch, s
                )
            )
            content.add_widget(card)

        layout_scroll.add_widget(content)
        self.add_widget(layout_scroll)

    def on_card_touch(self, instance, touch, servicio):
        if instance.collide_point(*touch.pos):
            self.mostrar_dialogo(servicio)

    def mostrar_dialogo(self, servicio):
        """Dialogo para confirmar la vista de la informacion del servicio"""

        self.dialog = MDDialog(
            title="¿Ver información del servicio?",
            text=f"""
                Nombre del servicio: {servicio['razon_social']}\nAdministrador: {servicio['administrador']}\n
            """,
            buttons=[
                MDFlatButton(
                    text="CANCELAR", on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="VER", on_release=lambda x: self.ir_a_informacion(servicio)
                ),
            ],
        )
        self.dialog.open()

    def ir_a_informacion(self, servicio):
        """Dirige a la pantalla de informacion de servicio"""

        self.dialog.dismiss()
        if self.parent_screen and self.parent_screen.manager:
            sm = self.parent_screen.manager
            pantalla_info = sm.get_screen("informacionservicios")
            pantalla_info.servicio_actual = servicio  # asignar el servicio
            sm.current = "informacionservicios"


class Pantalla_Usuario(MDScreen):
    """Clase Principal de la pantalla del cliente"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantallaUsuario"
        self.build_ui()
        self.dialog = None
        # color de fondo
        self.md_bg_color = "#FFF2F2"

    def build_ui(self):
        """Construye la interfaz de usuario de la pantalla del cliente"""

        main_layout = MDBoxLayout(orientation="vertical")
        main_layout.add_widget(self.create_top_bar())

        self.bottom_nav = MDBottomNavigation(panel_color = ("#02020262"))

        self.bottom_nav.add_widget(self.Servicios_tab())
        self.bottom_nav.add_widget(self.Reservas_tab())

        main_layout.add_widget(self.bottom_nav)
        self.add_widget(main_layout)

    def on_pre_enter(self):
        """Preparar la pantalla antes de que se muestre."""
        
        self.Servicios_tab()
        self.datos_reservas()

    def create_top_bar(self):
        """Creacion del TopAppBar"""

        return MDTopAppBar(
            title="ReservaFacil",
            right_action_items=[["account", lambda x: self.abrir_usuario()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
            md_bg_color="#015551",
        )

    def Servicios_tab(self):
        """Carga los servicios que estan disponibles."""

        tab = MDBottomNavigationItem(name="servicios", text="Servicios", icon="home")

        layout = MDBoxLayout(orientation="vertical", spacing="10dp")

        # Crear tabs y añadirlos
        tabs = MDTabs(
            md_bg_color="#FFF2F2",
            indicator_color="#FF0000",
            text_color_normal="#FFFFFF",
            text_color_active="#015551",
        )

        tabs.add_widget(TabHotel(parent_screen=self))
        tabs.add_widget(TabParqueadero(parent_screen=self))
        tabs.add_widget(TabRestaurante(parent_screen=self))

        layout.add_widget(tabs)
        tab.add_widget(layout)
        return tab

    def Reservas_tab(self):
        """Carga las reservas realizadas del usuario"""

        tab = MDBottomNavigationItem(name="reservas", text="Reservas", icon="calendar")

        layout_reservas = MDBoxLayout(
            orientation="vertical", spacing="10dp", md_bg_color="#FFF2F2"
        )

        # Layout para la información del servicio con ScrollView
        self.info_layout_res = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="10dp",
            size_hint_y=None,
        )
        self.info_layout_res.bind(minimum_height=self.info_layout_res.setter("height"))

        scroll_view = ScrollView(size_hint=(1, 1), bar_width="8dp")
        scroll_view.add_widget(self.info_layout_res)

        layout_reservas.add_widget(scroll_view)

        tab.add_widget(layout_reservas)
        return tab

    def datos_reservas(self):
        """Obtiene los datos de la reservas realizadas"""

        self.info_layout_res.clear_widgets()

        app = App.get_running_app()

        if not hasattr(app, "id_usuario") or not app.id_usuario:
            self.info_layout_res.add_widget(
                MDLabel(text="Por favor, inicie sesión primero.", halign="center")
            )
            return
        try:
            reservas = obtener_reservas_realizadas(app.id_usuario)
        except Exception as e:
            print("Error al obtener reservas:", e)
            self.add_widget(MDLabel(text="Error al cargar reservas", halign="center"))
            return

        if reservas:
            for reserva in reservas:
                self.info_layout_res.add_widget(self.crear_card_reserva(reserva))
        else:
            self.info_layout_res.add_widget(
                MDLabel(text="No hay reservas registradas.", halign="center")
            )

    def formatear_ubicacion_decimal(self, ubicacion_str):
        """Formatea una cadena de ubicacion en forma de "latitud, longitud" a un formato legible."""

        try:
            lat_str, lon_str = ubicacion_str.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            return f"Lat: {lat:.6f}, Lon: {lon:.6f}"
        except Exception as e:
            return "Ubicación inválida"

    def crear_card_reserva(self, reserva):
        """Crea una tarjeta para mostrar la informacion de la reserva"""

        card = MDCard(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(130),
            padding=dp(10),
            ripple_behavior=True,
            elevation=4,
            md_bg_color="#FFF2F26C",
        )
        imagen = FitImage(
            source=reserva["imagen"],
            radius=[
                dp(75),
                dp(75),
                dp(75),
                dp(75),
            ],  # Radios para los cuatro bordes (circular si alto=ancho)
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={"center_x": 0.5},
        )
        card.add_widget(imagen)
        datos = MDBoxLayout(orientation="vertical", padding=(dp(10), 0))
        datos.add_widget(
            MDLabel(
                text="[b]Admin:[/b] " + reserva["administrador"],
                markup=True,
                font_style="Body2",
                font_size="16sp",
                theme_text_color="Custom",
            )
        )

        ubicacion = self.formatear_ubicacion_decimal(reserva["ubicacion"])
        datos.add_widget(
            MDLabel(
                text=f"[b]Ubicación:[/b] {ubicacion}",
                font_style="Body2",
                font_size="16sp",
                markup=True,
                theme_text_color="Custom",
            )
        )

        datos.add_widget(
            MDLabel(
                text=f"[b]Fecha:[/b] {reserva['fecha_reserva']}",
                font_style="Body2",
                font_size="16sp",
                markup=True,
                theme_text_color="Custom",
            )
        )

        datos.add_widget(
            MDLabel(
                text=f"[b]Hora:[/b] {reserva['hora_reserva']}",
                font_style="Body2",
                font_size="16sp",
                markup=True,
                theme_text_color="Custom",
            )
        )
        card.bind(
            on_touch_up=lambda instance, touch, s=reserva: self.on_card_touch(
                instance, touch, s
            )
        )

        card.add_widget(datos)
        return card

    def on_card_touch(self, instance, touch, reserva):
        if instance.collide_point(*touch.pos):
            self.mostrar_dialogo(reserva)

    def mostrar_dialogo(self, reserva):
        """Dialogo para confirmar ver informacion de la reserva"""

        self.dialog = MDDialog(
            title = "¿Ver información de la reserva?",
            text = f"""
                Nombre del servicio: {reserva['razon_social']}\nAdministrador: {reserva['administrador']}
            """,
            buttons=[
                MDRaisedButton(
                    text="CANCELAR", on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="VER", on_release=lambda x: self.ir_a_informacion_reserva(reserva)
                ),
            ],
        )
        self.dialog.open()

    def ir_a_informacion_reserva(self, reserva):
        """Dirige a la pantalla de informacion de reserva"""

        self.dialog.dismiss()
        if self.manager:
            pantalla_info = self.manager.get_screen("informacionreserva")
            pantalla_info.reserva_actual = reserva
            self.manager.current = "informacionreserva"
            self.dialog.dismiss()


    def abrir_usuario(self):
        """Abrir la pantalla de perfil del usuario."""

        # Obtener datos del usuario desde el App

        app = App.get_running_app()
        usuario = obtener_usuario(app.id_usuario)
        if not usuario:
            print("usuario, iniciar sesion")
            return

        if self.manager:
            pantalla_usuario = self.manager.get_screen("perfil_usuario")
            pantalla_usuario.set_usuario(usuario)
            self.manager.current = "perfil_usuario"
