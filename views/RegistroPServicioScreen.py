from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp
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
        main_layout = MDBoxLayout(orientation='vertical')

        # Color de fondo
        main_layout.md_bg_color = ("#FFF2F2")
        top_bar = MDTopAppBar(
            title="Registro de P.S",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5,
            size_hint_y=None,
            md_bg_color=("#015551"),  
            height="56dp"
        )

        scroll_view = ScrollView()
        scroll_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=dp(10))
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        imagen=FitImage(
                source="image/usuario.png",
                radius=[dp(75), dp(75), dp(75), dp(75)],  # Radios para los cuatro bordes (circular si alto=ancho)
                size_hint=(None, None),
                size=(dp(150), dp(150)),
                pos_hint={"center_x": 0.5}
            )
        self.correo = MDTextField(hint_text="Correo electrónico", helper_text="", helper_text_mode="on_error", mode="rectangle", icon_right="email")
        self.nombre = MDTextField(hint_text="Nombre", mode="rectangle", icon_right="account")
        self.telefono = MDTextField(hint_text="Teléfono", input_filter="int", mode="rectangle", icon_right="phone")
        self.telefono.bind(text=self.validar_longitud_telefono)
        self.contraseña = MDTextField(hint_text="Contraseña", password=True, helper_text="", helper_text_mode="on_error", mode="rectangle", icon_right="lock")
        self.vcontraseña = MDTextField(hint_text="Confirmar contraseña", password=True, helper_text="", helper_text_mode="on_error", mode="rectangle", icon_right="lock")

        button_container = MDAnchorLayout(anchor_x="center", ) 
        self.registro_button = MDRaisedButton(text="Registrar",  pos_hint={"center_x": 0.5}, on_release=self.registrar, md_bg_color=("#FE4F2D"), size_hint=(None, None), size=(200, 50))

        # Add widgets to the scrollable layout
        
        scroll_layout.add_widget(self.correo)
        scroll_layout.add_widget(self.nombre)
        scroll_layout.add_widget(self.telefono)
        scroll_layout.add_widget(self.contraseña)
        scroll_layout.add_widget(self.vcontraseña)
        scroll_layout.add_widget(self.registro_button)

        # Add the scrollable layout to the ScrollView
        scroll_view.add_widget(scroll_layout)

        # Add the top bar and ScrollView to the main layout
        main_layout.add_widget(top_bar)
        main_layout.add_widget(imagen)
        main_layout.add_widget(scroll_view)

        self.add_widget(main_layout)

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
            telefono_cifrado = fernet.encrypt(str(self.telefono.text).encode())

            # Hashear la contraseña
            contraseña_bytes = self.contraseña.text.encode('utf-8')
            salt = bcrypt.gensalt()
            contraseña_hash = bcrypt.hashpw(contraseña_bytes, salt)

            agregar_prestador_servicio(
                correo_servicio=correo,
                nombre_propietario=nombre_cifrado,
                telefono_servicio=telefono_cifrado,
                contraseña_servicio=contraseña_hash.decode('utf-8')  # IMPORTANTE: guarda como string
            )

            print("Registro exitoso para:", self.nombre.text)

            # Limpiar campos
            self.correo.text = ""
            self.nombre.text = ""
            self.telefono.text = ""
            self.contraseña.text = ""
            self.vcontraseña.text = ""

        except Exception as e:
            print("Error al registrar:", e)

        # Regresar a la pantalla de inicio de sesión
        self.manager.current = "loginscreen"

    def volver_atras(self):
        self.manager.current = "registroscreen"
