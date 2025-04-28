from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.anchorlayout import MDAnchorLayout
from Database.Data_P_Servicio import agregar_prestador_servicio
from cryptography.fernet import Fernet
import bcrypt
import re
import os

# Cargar o generar clave de cifrado
if not os.path.exists("clave.key"):
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(Fernet.generate_key())

# Cargar la clave de cifrado
with open("clave.key", "rb") as clave_archivo:
    clave = clave_archivo.read()

fernet = Fernet(clave)

class registro_p_servicio_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "registropservicioscreen"
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        top_bar = MDTopAppBar(
            title="Registro de Servicio",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5
        )

        self.correo = MDTextField(hint_text="Correo electrónico", helper_text="", helper_text_mode="on_error")
        self.nombre = MDTextField(hint_text="Nombre")
        self.nit = MDTextField(hint_text="NIT", input_filter="int")
        self.razon = MDTextField(hint_text="Razón social")
        self.telefono = MDTextField(hint_text="Teléfono", input_filter="int")
        self.telefono.bind(text=self.validar_longitud_telefono)
        self.contraseña = MDTextField(hint_text="Contraseña", password=True, helper_text="", helper_text_mode="on_error")
        self.vcontraseña = MDTextField(hint_text="Confirmar contraseña", password=True, helper_text="", helper_text_mode="on_error")

        button_container = MDAnchorLayout(anchor_x="center")
        self.registro_button = MDRaisedButton(text="Registrar", pos_hint={"center_x": 0.5}, on_release=self.registrar)

        layout.add_widget(top_bar)
        layout.add_widget(self.correo)
        layout.add_widget(self.nombre)
        layout.add_widget(self.nit)
        layout.add_widget(self.razon)
        layout.add_widget(self.telefono)
        layout.add_widget(self.contraseña)
        layout.add_widget(self.vcontraseña)
        layout.add_widget(self.registro_button)

        self.add_widget(layout)

    def validar_correo(self, correo):
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(patron, correo))

    def validar_longitud_telefono(self, instance, value):
        if len(value) > 10:
            instance.text = value[:10]

    def registrar(self, instance):
        if not self.validar_correo(self.correo.text):
            self.correo.error = True
            self.correo.helper_text = "¡Correo inválido!"
            return

        if self.contraseña.text != self.vcontraseña.text:
            self.contraseña.error = True
            self.vcontraseña.error = True
            self.contraseña.helper_text = "¡Las contraseñas no coinciden!"
            self.vcontraseña.helper_text = "¡Las contraseñas no coinciden!"
            return

        try:
            # No cifrar el correo
            correo = self.correo.text

            # Cifrar los demás datos
            nombre_cifrado = fernet.encrypt(self.nombre.text.encode())
            nit_cifrado = fernet.encrypt(self.nit.text.encode())
            razon_cifrado = fernet.encrypt(self.razon.text.encode())
            telefono_cifrado = fernet.encrypt(self.telefono.text.encode())

            # Hashear la contraseña
            contraseña_bytes = self.contraseña.text.encode('utf-8')
            salt = bcrypt.gensalt()
            contraseña_hash = bcrypt.hashpw(contraseña_bytes, salt)

            agregar_prestador_servicio(
                correo_servicio=correo,
                nombre_propietario=nombre_cifrado,
                nit=nit_cifrado,
                razon_social=razon_cifrado,
                telefono_servicio=telefono_cifrado,
                contraseña_servicio=contraseña_hash.decode('utf-8')  # IMPORTANTE: guarda como string
            )

            print("Registro exitoso para:", self.nombre.text)

            # Limpiar campos
            self.correo.text = ""
            self.nombre.text = ""
            self.nit.text = ""
            self.razon.text = ""
            self.telefono.text = ""
            self.contraseña.text = ""
            self.vcontraseña.text = ""

        except Exception as e:
            print("Error al registrar:", e)

        #regresar a la pantalla de inicio de sesión
        self.manager.current = "loginscreen"

    def volver_atras(self):
        self.manager.current = "registroscreen"
