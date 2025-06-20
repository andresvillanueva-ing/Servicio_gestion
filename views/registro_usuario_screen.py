"""Pantalla de registro del cliente."""

import re
import bcrypt
import os

from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.fitimage import FitImage
from kivymd.uix.snackbar import Snackbar

from cryptography.fernet import Fernet

from ..Database.Data_usuario import agregar_usuario

# Cargar o generar clave de cifrado
if not os.path.exists("clave.key"):
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(Fernet.generate_key())

# Cargar la clave de cifrado
with open("clave.key", "rb") as clave_archivo:
    clave = clave_archivo.read()

fernet = Fernet(clave)


class registro_usuario_screen(MDScreen):
    """Clase Principal de la pantalla de registro de cliente"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "registrousuarioscreen"

        # color de fondo
        self.md_bg_color = "#FFF2F2"

        # Layout principal
        layout = MDBoxLayout(
            orientation="vertical",
        )

        top_bar = MDTopAppBar(
            title="Registro de Usuario",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
            md_bg_color=("#015551"),  # Color morado
        )

        imagen = FitImage(
            source="image/usuario.png",
            radius=[
                dp(75),
                dp(75),
                dp(75),
                dp(75),
            ],  # Radios para los cuatro bordes (circular si alto=ancho)
            size_hint=(None, None),
            size=(dp(150), dp(150)),
            pos_hint={"center_x": 0.5},
        )

        scrollView = ScrollView()
        scroll_layout = MDBoxLayout(
            orientation="vertical", size_hint_y=None, spacing=dp(10), padding=dp(10)
        )
        scroll_layout.bind(minimum_height=scroll_layout.setter("height"))

        # Campos de texto
        self.nombre_usuario = MDTextField(
            hint_text="Nombre Completo",
            helper_text="",
            helper_text_mode="on_error",
            mode="rectangle",
            icon_right="account",
        )
        self.correo_usuario = MDTextField(
            hint_text="correo Electronico",
            helper_text="",
            helper_text_mode="on_error",
            mode="rectangle",
            icon_right="email",
        )
        self.telefono_usuario = MDTextField(
            hint_text="Telefono",
            input_filter="int",
            helper_text="",
            helper_text_mode="on_error",
            mode="rectangle",
            icon_right="phone",
        )
        self.telefono_usuario.bind(text=self.validar_longitud_telefono)
        self.contraseña_usuario = MDTextField(
            hint_text="Contraseña",
            password=True,
            helper_text="",
            helper_text_mode="on_error",
            mode="rectangle",
            icon_right="lock",
        )
        self.v_contraseña_usuario = MDTextField(
            hint_text="verificar contraseña",
            password=True,
            helper_text="",
            helper_text_mode="on_error",
            mode="rectangle",
            icon_right="lock",
        )

        self.button_registro_usuario = MDRaisedButton(
            text="Registrarse",
            md_bg_color="#FE4F2D",
            font_style="Button",
            pos_hint={"center_x": 0.5},
        )
        self.button_registro_usuario.bind(on_press=self.registrar_usuario)

        # Agregar widgets al scroll layout
        scroll_layout.add_widget(self.nombre_usuario)
        scroll_layout.add_widget(self.correo_usuario)
        scroll_layout.add_widget(self.telefono_usuario)
        scroll_layout.add_widget(self.contraseña_usuario)
        scroll_layout.add_widget(self.v_contraseña_usuario)
        scroll_layout.add_widget(self.button_registro_usuario)
        scrollView.add_widget(scroll_layout)

        # Agregar widgets al layout principal
        layout.add_widget(top_bar)
        layout.add_widget(imagen)
        layout.add_widget(scrollView)

        self.add_widget(layout)

    def validar_correo_usuario(self, correo_usuario):
        """Metodo para permitir formato del correo."""

        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(patron, correo_usuario):
            return True
        return False

    def validar_longitud_telefono(self, instance, value):
        """Metodo para limitarla cantidad de numeros en el campo de telefono."""

        if len(value) > 10:
            instance.text = value[:10]

    def registrar_usuario(self, instance):
        """Metodo para registrar los datos del cliente."""

        if not self.validar_correo_usuario(self.correo_usuario.text):
            self.correo_usuario.error = True
            self.correo_usuario.helper_text = "¡¡correo_usuario invalido!!"
            return

        if self.contraseña_usuario.text != self.v_contraseña_usuario.text:
            self.contraseña_usuario.error = True
            self.v_contraseña_usuario.error = True
            self.contraseña_usuario.helper_text = "!!Las contraseñas no coiciden¡¡"
            self.v_contraseña_usuario.helper_text = "!!Las contraseñas no coiciden¡¡"
            return

        try:
            # No cifrar el correo_usuario
            correo_usuario = self.correo_usuario.text

            # Cifrar los demás datos
            nombre_encriptado = fernet.encrypt(self.nombre_usuario.text.encode())
            telefono_encriptado = fernet.encrypt(
                str(self.telefono_usuario.text).encode()
            )

            # Hashear la contraseña
            contraseña_bytes = self.contraseña_usuario.text.encode("utf-8")
            salt = bcrypt.gensalt()
            contraseña_hash = bcrypt.hashpw(contraseña_bytes, salt)

            # Guarda los datos en la base de datos encriptados.
            agregar_usuario(
                nombre_encriptado,
                correo_usuario,
                telefono_encriptado,
                contraseña_usuario=contraseña_hash.decode("utf_8"),
            )

            Snackbar(
                MDLabel(text=f"!Registros éxito¡. {self.nombre_usuario.text}")
            ).open()

            # Limpia los campos despues de enviar los datos
            self.nombre_usuario.text = ""
            self.correo_usuario.text = ""
            self.telefono_usuario.text = ""
            self.contraseña_usuario.text = ""
            self.v_contraseña_usuario.text = ""

        except Exception as e:
            import traceback

            traceback.print_exc()

        # regresar a la pantalla de inicio de sesión
        self.manager.current = "loginscreen"

    def volver_atras(self):
        self.manager.current = "registroscreen"
