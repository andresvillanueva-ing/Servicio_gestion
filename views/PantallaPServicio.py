from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton
from kivy.app import App

class TabReservas(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(MDLabel(text="En el momento no hay reservas", halign="center"))

class TabConfiguracion(FloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Título
        self.add_widget(MDLabel(
            text="Tu Servicio",
            halign="center",
            font_style="H5",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5, "top": 1}
        ))

        # Información del servicio
        info_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="20dp",
            size_hint=(1, None),
            #height="200dp",
            pos_hint={"center_x": 0.5, "top": 0.8}
        )

        info_layout.add_widget(MDLabel(text="Razón Social: Mi Empresa", halign="left"))
        info_layout.add_widget(MDLabel(text="Administrador: Juan Pérez", halign="left"))
        info_layout.add_widget(MDLabel(text="Ubicación: Calle 123, Ciudad", halign="left"))
        info_layout.add_widget(MDLabel(text="Puestos: 10", halign="left"))

        self.add_widget(info_layout)

        # Botones
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing="20dp",
            padding="20dp",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5, "top": 0.5}
        )

        modify_button = MDRaisedButton(
            text="Modificar Información",
            size_hint=(None, None),
            size=("200dp", "40dp"),
            pos_hint={"center_x": 0.5},
            on_release=self.modificar_informacion
        )

        create_service_button = MDRaisedButton(
            text="Crear Servicio",
            size_hint=(None, None),
            size=("200dp", "40dp"),
            pos_hint={"center_x": 0.5},
            on_release=self.ir_a_registrar_servicio
        )

        button_layout.add_widget(modify_button)
        button_layout.add_widget(create_service_button)

        self.add_widget(button_layout)

    def modificar_informacion(self, instance):
        # Lógica para modificar la información
        print("Modificar información presionado")

    def ir_a_registrar_servicio(self, instance):
        # Lógica para ir a la pantalla de registrar servicio
        App.get_running_app().root.current = "registrarservicios"


class Pantalla_P_Servicio(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantallaPServicio"

        layout = MDBoxLayout(orientation='vertical')

        top_bar = MDTopAppBar(
            title="Administrador",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
            right_action_items=[["account", lambda x: self.abrir_usuario()]]
        )

        # Crear las pestañas
        tabs = MDTabs()
        tab1 = TabReservas()
        tab1.title = "Reservas"
        tabs.add_widget(tab1)
        tab2 = TabConfiguracion()
        tab2.title = "Configuración"
        tabs.add_widget(tab2)

        # Agregar la barra superior al diseño
        layout.add_widget(top_bar)

        # Agregar las pestañas al final del diseño
        layout.add_widget(tabs)

        self.add_widget(layout)
