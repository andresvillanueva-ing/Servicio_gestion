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

# cargar o generar clave de cifrado
if not os.path.exists("clave.key"):
    with open ("clave.key", "wb") as clave_archivo:
        clave_archivo.write(Fernet.generate_key())

#carga la clave de cifrado desde el archivo
with open("clave.key", "rb") as clave_archivo:
    clave = clave_archivo.read()


# Crea un objeto Fernet con la clave para cifrar/descifrar datos
    fernet = Fernet(clave)

class registro_p_servicio_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name ="registropservicioscreen"
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Etiqueta de título
        top_bar = MDTopAppBar(
            title="Registro de Servicio",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],  # Agregamos la flecha
            elevation=5
        )

        # Campos de texto donde el usuario ingresa los datos
        self.correo = MDTextField(hint_text="Correo electrónico", helper_text = "", helper_text_mode = "on_error")
        self.nombre = MDTextField(hint_text="Nombre")
        self.nit = MDTextField(hint_text="NIT", input_filter = "int")
        self.razon = MDTextField(hint_text="Razón social")
        self.telefono = MDTextField(hint_text="Telefono", input_filter = "int")
        self.telefono.bind(text=self.validar_longitud_telefono)
        self.contraseña = MDTextField(hint_text="Contraseña", password=True, helper_text = "", helper_text_mode="on_error")
        self.vcontraseña = MDTextField(hint_text="Confirmar contraseña", password=True, helper_text = "", helper_text_mode="on_error")
        
        #boton de registro
        button_container = MDAnchorLayout(anchor_x="center")
        self.registro_button = MDRaisedButton(text="Registrar", pos_hint = {"center_x": 0.5}, on_release=self.registrar)
        
        #los widgets se añaden al layout
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
        #Valida si el correo electrónico tiene un formato válido
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(patron, correo):
            return True
        return False
    
    def validar_longitud_telefono(self, instance, value):
        if len(value) > 10:
            instance.text = value[:10] 

    def registrar(self, instance):
        # Validar que el correo no esté vacío
        if not self.validar_correo(self.correo.text):
            self.correo.error=True
            self.correo.helper_text = "!!Correo invalido¡¡"
            return
        # Validar que las contraseñas coinciden
        if self.contraseña.text != self.vcontraseña.text:
            self.contraseña.error= True
            self.vcontraseña.error= True
            self.contraseña.helper_text = "!!Las contraseñas no coinciden¡¡"
            self.vcontraseña.helper_text = "!!Las contraseñas no coinciden¡¡"
            return
        try:
            # 🔐 Cifrar los datos normales
            correo_cifrado = fernet.encrypt(self.correo.text.encode())
            nombre_cifrado = fernet.encrypt(self.nombre.text.encode())
            nit_cifrado = fernet.encrypt(self.nit.text.encode())
            razon_cifrado = fernet.encrypt(self.razon.text.encode())
            telefono_cifrado = fernet.encrypt(self.telefono.text.encode())

            # Hashear la contraseña
            contraseña_bytes = self.contraseña.text.encode('utf-8')
            salt = bcrypt.gensalt()
            contraseña_hash = bcrypt.hashpw(contraseña_bytes, salt)

        # Guardar los datos cifrados y la contraseña hasheada en la base de datos
            agregar_prestador_servicio(
                correo_servicio=correo_cifrado,
                nombre_propietario=nombre_cifrado,
                nit=nit_cifrado,
                razon_social=razon_cifrado,
                telefono_servicio=telefono_cifrado,
                contraseña_servicio=contraseña_hash
            )
            print("Registro exitoso para:", self.nombre.text)
            self.correo.text = ""
            self.nombre.text = ""
            self.nit.text = ""
            self.razon.text = ""
            self.telefono.text = ""
            self.contraseña.text = ""
            self.vcontraseña.text = ""

        except Exception as e:
                    print("Error al registrar:", e)

    def volver_atras(self):
        self.manager.current = "registroscreen" 