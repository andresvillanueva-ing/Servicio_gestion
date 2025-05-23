from kivymd.uix.screen import MDScreen
from Database.Data_Reservas import agregar_reserva
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.lang import Builder
from datetime import datetime



class reservas_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "reservasscreen"

        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        scroll = ScrollView()
        content = MDBoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Campos de entrada
        self.nombre_usuario = MDTextField(hint_text="Nombre completo")
        self.telefono = MDTextField(hint_text="Teléfono")
        self.correo = MDTextField(hint_text="Correo electrónico")

        self.boton_fecha = MDRaisedButton(
            text="Seleccionar fecha",
            pos_hint={"center_x": 0.5},
            on_release=self.show_date_picker
        )

        # Botón para agregar la reserva
        self.boton_reservar = MDRaisedButton(
            text="Reservar",
            pos_hint={"center_x": 0.5},
            on_release=self.reservar
        )

        
        # Agregar widgets al contenido
        content.add_widget(MDLabel(text="Datos de la reserva", halign="center"))
        content.add_widget(self.nombre_usuario)
        content.add_widget(self.telefono)
        content.add_widget(self.correo)
        content.add_widget(self.boton_fecha)
        

        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def show_date_picker(self, *args):
        date_dialog = MDDatePicker(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        
        date_dialog.open()
