from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.scrollview import ScrollView
from Database.Data_sercivios import agregar_servicio
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

class registrar_servicio_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "registrarservicios"

        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')

        # TopAppBar
        top_bar = MDTopAppBar(
            title="Registro de Servicio",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5,
            size_hint_y=None,
            height="56dp"
        )
        main_layout.add_widget(top_bar)

        # ScrollView para el contenido
        scroll_view = ScrollView()
        content_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        self.razon_social = MDTextField(hint_text="Razón social")
        self.nit = MDTextField(hint_text="NIT", input_filter="int")
        self.Administrador = MDTextField(hint_text="Nombre del administrador")
        self.Puestos = MDTextField(hint_text="Puestos disponibles")
        self.Ubicacion = MDTextField(hint_text="Ubicación")
        self.imagen = MDTextField(hint_text="Imagen")

        # ComboBox opciones para tipo de servicios
        self.tipo_servicios_button = MDFlatButton(
            text="Tipo de servicio", pos_hint={"center_x": 0.5}
        )

        menu_items = [
            {"text": "Parqueadero", "on_release": lambda x="Parqueadero": self.set_tipo_servicio(x)},
            {"text": "Hotel", "on_release": lambda x="Hotel": self.set_tipo_servicio(x)},
            {"text": "Restaurante", "on_release": lambda x="Restaurante": self.set_tipo_servicio(x)}
        ]

        self.tipo_servicio_menu = MDDropdownMenu(
            caller=self.tipo_servicios_button,
            items=menu_items,
            width_mult=4
        )

        self.tipo_servicios_button.bind(on_release=lambda *args: self.tipo_servicio_menu.open())
        self.registro_button = MDRaisedButton(text="Registrar", pos_hint={"center_x": 0.5}, on_release=self.registrar)

        # Agregar widgets al layout de contenido
        content_layout.add_widget(self.razon_social)
        content_layout.add_widget(self.nit)
        content_layout.add_widget(MDLabel(text="Seleccionar Tipo de servicio", halign="center"))
        content_layout.add_widget(self.tipo_servicios_button)
        content_layout.add_widget(self.Administrador)
        content_layout.add_widget(self.Puestos)
        content_layout.add_widget(self.Ubicacion)
        content_layout.add_widget(self.imagen)
        content_layout.add_widget(self.registro_button)

        # Agregar el layout de contenido al ScrollView
        scroll_view.add_widget(content_layout)

        # Agregar el ScrollView al layout principal
        main_layout.add_widget(scroll_view)

        # Agregar el layout principal a la pantalla
        self.add_widget(main_layout)

    def registrar(self, instance):
        # Validar que todos los campos estén llenos
        if not all([
            self.razon_social.text.strip(),
            self.nit.text.strip(),
            self.Administrador.text.strip(),
            self.Puestos.text.strip(),
            self.Ubicacion.text.strip(),
            self.imagen.text.strip(),
            self.tipo_servicios_button.text != "Tipo de servicio"
        ]):
            print("⚠️ Todos los campos son obligatorios, incluyendo el tipo de servicio.")
            return

        try:
            # Cifrar los datos
            razon_social_cifrado = fernet.encrypt(self.razon_social.text.encode())
            nit_cifrado = fernet.encrypt(self.nit.text.encode())
            tipo_servicio_cifrado = fernet.encrypt(self.tipo_servicios_button.text.encode())
            administrador_cifrado = fernet.encrypt(self.Administrador.text.encode())
            puestos_cifrado = fernet.encrypt(self.Puestos.text.encode())
            ubicacion_cifrado = fernet.encrypt(self.Ubicacion.text.encode())
            imagen_cifrado = fernet.encrypt(self.imagen.text.encode())

            agregar_servicio(
                razon_social=razon_social_cifrado,
                nit=nit_cifrado,
                tipo_servicio=tipo_servicio_cifrado,
                administrador=administrador_cifrado,
                puestos=puestos_cifrado,
                ubicacion=ubicacion_cifrado,
                imagen=imagen_cifrado
            )

            print("✅ Registro exitoso para:", self.razon_social.text)

            # Limpiar campos
            self.razon_social.text = ""
            self.nit.text = ""
            self.Administrador.text = ""
            self.Puestos.text = ""
            self.Ubicacion.text = ""
            self.imagen.text = ""
            self.tipo_servicios_button.text = "Tipo de servicio"

            self.manager.current = "pantallaPServicio"

        except Exception as e:
            print("❌ Error al registrar:", e)

        # Regresar a la pantalla de inicio de sesión
        self.manager.current = "pantallaPServicio"

    def set_tipo_servicio(self, tipo):
        self.tipo_servicios_button.text = tipo
        self.tipo_servicio_menu.dismiss()

    def volver_atras(self):
        self.manager.current = "registroscreen"
