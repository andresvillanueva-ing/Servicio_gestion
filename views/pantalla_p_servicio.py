"""Pantalla principal del prestador de servicio"""

from kivy.metrics import dp
from kivy.app import App

from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

from ..Database.Data_servicios import eliminar_servicio, obtener_servicios
from ..Database.Data_Reservas import obtener_reservas
from ..Database.Data_P_Servicio import obtener_prestador

class Pantalla_P_Servicio(MDScreen):
    """Clase Principal de la pantalla de prestador de servicio"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantallaPServicio"
        self.dialog = None
        self.info_layout = None  # Se define en otro método
        self.md_bg_color = "#FFF2F2"
        self.build_ui()

    def build_ui(self):
        """Construye la interfaz de usuario de la pantalla del prestador de servicio"""

        # Layout principal
        main_layout = MDBoxLayout(orientation="vertical")

        # Top bar
        main_layout.add_widget(self.create_top_bar())

        # Navegación inferior
        bottom_nav = MDBottomNavigation(panel_color=("#02020262"))
        bottom_nav.add_widget(self.create_reservas_tab())
        bottom_nav.add_widget(self.create_configuracion_tab())

        main_layout.add_widget(bottom_nav)
        self.add_widget(main_layout)

    def create_top_bar(self):
        """Creacion del TopAppBar"""

        return MDTopAppBar(
            title="Administrador",
            right_action_items=[["account", lambda x: self.abrir_usuario()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
        )

    def create_reservas_tab(self):
        """Creacion de la pantalla de reservas"""

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

    # ----- Tab de configuracion de servicios----
    def create_configuracion_tab(self):
        """Creacion de la pantalla de configuracion de servicios"""

        tab = MDBottomNavigationItem(
            name="configuracion", text="Configuración", icon="cog"
        )

        layout = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp",
            md_bg_color="#FFF2F2",
        )

        layout.add_widget(
            MDLabel(
                text="Tu Servicio \n ____________________",
                halign="center",
                font_style="H5",
                size_hint=(1, None),
                height="50dp",
            )
        )

        # Layout para la información del servicio con ScrollView
        self.info_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint_y=None,
        )
        self.info_layout.bind(minimum_height=self.info_layout.setter("height"))

        scroll_view = ScrollView(size_hint=(1, 1), bar_width="8dp")
        scroll_view.add_widget(self.info_layout)

        layout.add_widget(scroll_view)
        # Botones
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing="20dp",
            padding="20dp",
            size_hint=(1, None),
            height="50dp",
        )

        button_layout.add_widget(
            MDRaisedButton(
                text="Crear Servicio",
                size_hint=(None, None),
                size=("200dp", "40dp"),
                font_style="Button",
                md_bg_color="#FE4F2D",
                on_release=self.ir_a_registrar_servicio,
            )
        )
        layout.add_widget(button_layout)
        tab.add_widget(layout)
        return tab

    def on_pre_enter(self):
        """Preparar la pantalla antes de que se muestre."""

        self.datos_servicios()
        self.datos_reservas()

    # --------Datos de las reservas hechas a los servicios del prestador--------------
    def datos_reservas(self):
        """Carga las reservas realizadas al prestador de servicio"""

        self.info_layout_res.clear_widgets()

        app = App.get_running_app()

        if not hasattr(app, "id_prestador") or not app.id_prestador:
            self.info_layout_res.add_widget(
                MDLabel(text="Por favor, inicie sesión primero.", halign="center")
            )
            return
        try:
            reservas = obtener_reservas(app.id_prestador)
        except Exception as e:
            self.add_widget(MDLabel(text="Error al cargar reservas", halign="center"))
            return

        if reservas:
            for reserva in reservas:
                self.info_layout_res.add_widget(self.crear_card_reserva(reserva))
        else:
            self.info_layout_res.add_widget(
                MDLabel(text="No hay reservas registradas.", halign="center")
            )

    # ----------- Datos de servicios creados por el prestador de servicio-----------
    def datos_servicios(self):
        """Carga los datos de los servicios prestados por el prestador de servicio"""

        self.info_layout.clear_widgets()
        app = App.get_running_app()

        if not hasattr(app, "id_prestador") or not app.id_prestador:
            self.info_layout.add_widget(
                MDLabel(text="Por favor, inicie sesión primero.", halign="center")
            )
            return

        try:
            servicios = obtener_servicios(app.id_prestador)
        except Exception as e:
            print("Error al obtener servicios:", e)
            self.info_layout.add_widget(
                MDLabel(text="Error al cargar servicios", halign="center")
            )
            return

        if servicios:
            for servicio in servicios:
                self.info_layout.add_widget(self.crear_card_servicio(servicio))
        else:
            self.info_layout.add_widget(
                MDLabel(text="No hay servicios registrados.", halign="center")
            )

    # ----------Targeta de reservas realizadas-------------------
    def crear_card_reserva(self, reserva):
        """Crea la tarjeta para mostrar los datos de las reservas."""

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
                text=reserva["nombre_cliente"].upper(),
                bold=True,
                font_style="H6",
                halign="center",
            )
        )
        datos.add_widget(
            MDLabel(
                text="[b]Telefono:[/b] " + reserva["telefono_cliente"],
                markup=True,
                font_style="Body2",
                font_size="16sp",
                theme_text_color="Custom",
            )
        )
        datos.add_widget(
            MDLabel(
                text=f"[b]correo_usuario:[/b] {reserva["correo_cliente"]}",
                font_style="Body2",
                font_size="16sp",
                markup=True,
                theme_text_color="Custom",
            )
        )
        datos.add_widget(
            MDLabel(
                text=f"[b]fecha de reserva:[/b] {reserva["fecha_reserva"]}",
                font_style="Body2",
                font_size="16sp",
                markup=True,
                theme_text_color="Custom",
            )
        )
        card.add_widget(datos)
        card.bind(
            on_touch_up=lambda instance, touch: self.on_card_touch(
                instance, touch, reserva
            )
        )
        return card

    def on_card_touch(self, instance, touch, reserva):
        if instance.collide_point(*touch.pos):
            self.mostrar_dialogo(reserva)

    def mostrar_dialogo(self, reserva):
        """Muestra un dialogo que dirige a la pantalla de informacion de reserva"""

        self.dialog = MDDialog(
            title="¿Ver información del servicio?",
            text=f"Nombre del cliente: {reserva['nombre_cliente']}\nTelefono: {reserva['telefono_cliente']}",
            buttons=[
                MDRaisedButton(
                    text="CANCELAR", on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="VER", on_release=lambda x: self.ir_a_informacion(reserva)
                ),
            ],
        )
        self.dialog.open()

    # ----------Targeta de servcios creados-------------------
    def crear_card_servicio(self, servicio):
        """Crea la tarjeta para mostrar los datos de los servicios."""

        card = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="300dp",
            pos_hint={"center_x": 0.5},
            padding="10dp",
            spacing="10dp",
        )
        for key, label in {
            "razon_social": "Razón Social",
            "administrador": "Administrador",
            "tipo_servicio": "Tipo de Servicio",
            "ubicacion": "Ubicación",
            "puestos": "Puestos",
        }.items():
            card.add_widget(
                MDLabel(
                    text=f"[b]{label}[/b]: {servicio.get(key, '')}",
                    markup=True,
                    halign="left",
                    theme_text_color="Custom",
                )
            )
        botones = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
            height=dp(50),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        modificar_btn = MDRaisedButton(
            text="Modificar",
            size_hint=(1, None),
        )
        modificar_btn.bind(
            on_release=lambda x, servicio=servicio: self.modificar_informacion_conf(
                servicio
            )
        )
        eliminar_btn = MDRaisedButton(
            text="Eliminar",
            size_hint=(1, None),
        )
        eliminar_btn.bind(
            on_release=lambda x, servicio=servicio: self.eliminar_servicio(servicio)
        )
        botones.add_widget(modificar_btn)
        botones.add_widget(eliminar_btn)
        card.add_widget(botones)
        return card

    def ir_a_informacion(self, reserva):
        """Dirige a la pantalla de informacion de reserva"""

        self.dialog.dismiss()
        if self.manager:
            pantalla_info = self.manager.get_screen("informacionreservaprestador")
            pantalla_info.reserva_actual = reserva
            self.manager.current = "informacionreservaprestador"

    def modificar_informacion_conf(self, servicios):
        """Dialogo para confirmar la modificacion de la informacion del servicio"""

        self.dialog = MDDialog(
            title="¿Desea modifiacar los datos del servicio?",
            buttons=[
                MDRaisedButton(
                    text="CANCELAR", on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="VER",
                    on_release=lambda x: self.modificar_informacion(servicios),
                ),
            ],
        )
        self.dialog.open()

    def eliminar_servicio(self, servicios):
        """Dialogo para confirmar la eliminacion del servicio"""

        self.dialog = MDDialog(
            title="¿Desea eliminar el servicio?",
            buttons=[
                MDRaisedButton(
                    text="CANCELAR", on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Eliminar",
                    on_release=lambda x: self.eliminar_servicios(servicios),
                ),
            ],
        )
        self.dialog.open()

    def modificar_informacion(self, servicios):
        """Navegacion a modificar la informacion del servicio"""

        self.dialog.dismiss()
        if self.manager:
            pantalla_info = self.manager.get_screen("modificar_servicio")
            pantalla_info.servicio_actual = servicios
            self.manager.current = "modificar_servicio"
            print(servicios)

    def eliminar_servicios(self, servicios):
        """Funcion para eliminar servicios"""

        self.dialog.dismiss()
        try:
            eliminar_servicio(servicios.get("id_prestador"))
            print(servicios.get("id_prestador"))
            self.info_layout.clear_widgets()
            Snackbar(MDLabel(text="¡¡Servicio Eliminado con éxito.!!")).open()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def datos(self):
        """obtener los datos de los servicios"""

        app = App.get_running_app().id_prestador
        servicios = obtener_servicios(app)
        return servicios

    def ir_a_registrar_servicio(self, instance):
        """Navegacion hacia la pantalla de registrar servicio"""

        App.get_running_app().root.current = "registrarservicios"

    def abrir_usuario(self):
        """Navegar hacia la pantalla de perfil de usaurio"""

        # Obtener datos del usuario desde el App

        app = App.get_running_app()
        usuario = obtener_prestador(app.id_prestador)
        if not usuario:
            print("usuario, iniciar sesion")
            return
        if self.manager:
            pantalla_usuario = self.manager.get_screen("perfil_prestador")
            pantalla_usuario.set_prestador(usuario)
            self.manager.current = "perfil_prestador"
