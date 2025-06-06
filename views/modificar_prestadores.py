"""Pantalla para modificar los datos del prestador de servicio"""

import os

from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from cryptography.fernet import Fernet

from Database.Data_P_Servicio import modificar_prestador

# Generar clave si no existe
if not os.path.exists("clave.key"):
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(Fernet.generate_key())

# Cargar la clave
with open("clave.key", "rb") as clave_archivo:
    clave = clave_archivo.read()

fernet = Fernet(clave)


class Modificarprestador(MDScreen):
    """Clase Principal de la pantalla para modificar los datos del prestador de servicio"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "modificar_prestador"
        self.id_prestador = None

        # Layout principal
        layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        self.add_widget(layout)

        # Barra superior
        top_bar = MDTopAppBar(
            title="Modificar Servicio",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
            md_bg_color="#015551",
        )
        layout.add_widget(top_bar)

        # ScrollView
        scroll = ScrollView()
        campos_container = MDBoxLayout(
            orientation="vertical", padding=dp(20), spacing=dp(20), size_hint_y=None
        )
        campos_container.bind(minimum_height=campos_container.setter("height"))

        self.txt_nombre = MDTextField(
            hint_text="Nombre Completo", mode="rectangle", icon_right="account"
        )
        self.txt_correo = MDTextField(
            hint_text="Correo Electrónico", mode="rectangle", icon_right="email"
        )
        self.txt_telefono = MDTextField(
            hint_text="Teléfono",
            input_filter="int",
            mode="rectangle",
            icon_right="phone",
        )
        self.txt_telefono.bind(text=self.validar_longitud_telefono)

        self.registro_button = MDRaisedButton(
            text="Modificar",
            pos_hint={"center_x": 0.5},
            md_bg_color="#FE4F2D",
            on_release=self.registrar,
        )

        # Agregar campos al contenedor
        campos_container.add_widget(self.txt_nombre)
        campos_container.add_widget(self.txt_correo)
        campos_container.add_widget(self.txt_telefono)
        campos_container.add_widget(self.registro_button)

        scroll.add_widget(campos_container)
        layout.add_widget(scroll)

    def validar_longitud_telefono(self, instance, value):
        """Metodo para validar la longitud del telefono"""

        if len(value) > 10:
            instance.text = value[:10]

    def registrar(self, instance):
        """Metodo para registrar los datos modificados del prestador"""

        if not all(
            [
                self.txt_nombre.text.strip(),
                self.txt_correo.text.strip(),
                self.txt_telefono.text.strip(),
            ]
        ):
            print("⚠️ Todos los campos son obligatorios.")
            return

        try:
            nombre = fernet.encrypt(self.txt_nombre.text.encode())
            telefono = fernet.encrypt(self.txt_telefono.text.encode())
            correo = self.txt_correo.text

            modificar_prestador(
                nombre=nombre, correo=correo, telefono=telefono, id=self.id_prestador
            )

            Snackbar(MDLabel(text="¡Datos modificados con éxito!")).open()

            # Limpiar campos
            self.txt_nombre.text = ""
            self.txt_correo.text = ""
            self.txt_telefono.text = ""

            self.manager.current = "pantallaPServicio"

        except Exception as e:
            import traceback

            traceback.print_exc()

    def set_datos_prestador(self, prestador):
        """Metodo para recibir los datos del prestador a modificar"""

        self.id_prestador = prestador["id"]
        self.txt_nombre.text = prestador["nombre"]
        self.txt_correo.text = prestador["correo"]
        self.txt_telefono.text = prestador["telefono"]

    def volver_atras(self):
        self.manager.current = "pantallaPServicio"
