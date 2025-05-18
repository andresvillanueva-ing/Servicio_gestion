from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.card import MDCard
from kivy.app import App
from Database.Data_sercivios import obtener_servicios


class Pantalla_P_Servicio(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantallaPServicio"
        self.info_layout = None  # Se define en otro método

        self.build_ui()

    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')

        # Top bar
        main_layout.add_widget(self.create_top_bar())

        # Navegación inferior
        bottom_nav = MDBottomNavigation(panel_color=(1, 1, 1, 1))
        bottom_nav.add_widget(self.create_reservas_tab())
        bottom_nav.add_widget(self.create_configuracion_tab())

        main_layout.add_widget(bottom_nav)
        self.add_widget(main_layout)

    def create_top_bar(self):
        return MDTopAppBar(
            title="Administrador",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            right_action_items=[["account", lambda x: self.abrir_usuario()]],
            elevation=5,
            size_hint_y=None,
            height="56dp"
        )

    def create_reservas_tab(self):
        tab = MDBottomNavigationItem(name="reservas", text="Reservas", icon="calendar")
        layout = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp"
        )
        layout.add_widget(MDLabel(text="En el momento no hay reservas", halign="center"))
        tab.add_widget(layout)
        return tab

    def create_configuracion_tab(self):
        tab = MDBottomNavigationItem(name="configuracion", text="Configuración", icon="cog")

        layout = MDBoxLayout(orientation="vertical", padding="10dp", spacing="10dp")

        layout.add_widget(MDLabel(
            text="Tu Servicio", halign="center", font_style="H5",
            size_hint=(1, None), height="50dp"
        ))

        self.info_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint=(1, None),
            pos_hint={"center_x": 0.5, "top": 0.8}
        )
        layout.add_widget(self.info_layout)

        # Botones
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing="20dp",
            padding="20dp",
            size_hint=(1, None),
            height="50dp"
        )
        button_layout.add_widget(MDRaisedButton(
            text="Modificar Información",
            size_hint=(None, None),
            size=("200dp", "40dp"),
            on_release=self.modificar_informacion
        ))
        button_layout.add_widget(MDRaisedButton(
            text="Crear Servicio",
            size_hint=(None, None),
            size=("200dp", "40dp"),
            on_release=self.ir_a_registrar_servicio
        ))

        layout.add_widget(button_layout)
        tab.add_widget(layout)
        return tab

    def on_pre_enter(self):
        self.datos_servicios()

    def datos_servicios(self):
        self.info_layout.clear_widgets()
        from kivy.app import App
        app = App.get_running_app()
        print("Tiene id_prestador?", hasattr(app, "id_prestador"))
        print("id_prestador =", getattr(app, "id_prestador", None))
        
        app = App.get_running_app()
        if not hasattr(app, "id_prestador") or not app.id_prestador:
            self.info_layout.add_widget(MDLabel(text="Por favor, inicie sesión primero.", halign="center"))
            return
        
        try:
            servicios = obtener_servicios(App.get_running_app().id_prestador)
            print("Servicios encontrados:", servicios)
        except Exception as e:
            print("Error al obtener servicios:", e)
            self.info_layout.add_widget(MDLabel(text="Error al cargar servicios", halign="center"))
            return

        if servicios:
            self.info_layout.add_widget(MDLabel(text="Servicios Registrados", halign="center", font_style="H5"))
            self.info_layout.add_widget(MDLabel(text="____________________", halign="center"))
            for servicio in servicios:
                self.info_layout.add_widget(self.crear_card_servicio(servicio))
        else:
            self.info_layout.add_widget(MDLabel(text="No hay servicios registrados.", halign="center"))

    def crear_card_servicio(self, servicio):
        card = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="300dp",
            pos_hint={"center_x": 0.5},
            padding="10dp",
            spacing="10dp"
        )
        for key, label in {
            "razon_social": "Razón Social",
            "administrador": "Administrador",
            "tipo_servicio": "Tipo de Servicio",
            "ubicacion": "Ubicación",
            "puestos": "Puestos"
        }.items():
            card.add_widget(MDLabel(text=f"{label}: {servicio.get(key, '')}", halign="left"))
        return card

    def modificar_informacion(self, instance):
        print("Modificar información presionado")
        # Aquí puedes navegar a la pantalla de edición o abrir un diálogo.

    def ir_a_registrar_servicio(self, instance):
        App.get_running_app().root.current = "registrarservicios"

    def volver_atras(self):
        self.manager.current = "loginscreen"

    def abrir_usuario(self):
        self.manager.current = "pantalla_usuario"
