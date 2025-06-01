# views/ReservasScreen.py
from kivymd.uix.screen import MDScreen
from Database.Data_Reservas import agregar_reserva # Asegúrate de que esta importación sea correcta
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.fitimage import FitImage
from kivy.app import App
from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.dialog import MDDialog 
from cryptography.fernet import Fernet
from kivy.metrics import dp
import os
import re


# Cargar o generar clave de cifrado
if not os.path.exists("clave.key"):
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(Fernet.generate_key())

# Cargar la clave de cifrado
with open("clave.key", "rb") as clave_archivo:
    clave = clave_archivo.read()

fernet = Fernet(clave)

class reservas_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "reservasscreen"
        self.datos_servicio = None # Inicializa esta propiedad para almacenar el servicio
        self.selected_date = None # Para almacenar la fecha seleccionada
        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        scroll = ScrollView()
        content = MDBoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        self.imagen_servicio = FitImage(
            radius=[dp(75), dp(75), dp(75), dp(75)],
            size_hint=(None, None),
            size=(dp(150), dp(150)),
            pos_hint={"center_x": 0.5},
            spacing = 10
        )
        
        self.nombre_usuario = MDTextField(
            hint_text="Nombre completo",
            helper_text="Ingresa un nombre valido",
            helper_text_mode="on_error",
            mode="rectangle", 
            icon_right="account"
            )

        # Solo permite numeros y la validacion de longitud
        
        self.telefono = MDTextField(
            hint_text="Telefono", 
            helper_text="",
            helper_text_mode="on_error",
            mode="rectangle",
            icon_right="phone",
            input_filter="int",
        )
        self.telefono.bind(text=self.validar_longitud_telefono) # Limita a 10 caracteres 
        
        self.correo_usuario = MDTextField(
            hint_text="Correo electrónico",
            helper_text="Ingresa un correo valido",
            helper_text_mode="on_error",
            mode="rectangle",
            icon_right="email"
            )

        self.boton_fecha = MDRaisedButton(
            text="Seleccionar fecha",
            pos_hint={"center_x": 0.5},
            on_release=self.show_date_picker
        )
        self.label_fecha_seleccionada = MDLabel(
            text="Fecha no seleccionada",
            halign="center",
            theme_text_color="Secondary"
        )


        self.boton_reservar = MDRaisedButton(
            text="Reservar",
            pos_hint={"center_x": 0.5},
            on_release=self.reservar
        )

        content.add_widget(MDLabel(text="Datos de la reserva", halign="center", theme_text_color="Primary", font_style="H5"))
        content.add_widget(self.imagen_servicio) 
        content.add_widget(self.nombre_usuario)
        content.add_widget(self.telefono)
        content.add_widget(self.correo_usuario)
        content.add_widget(self.boton_fecha)
        content.add_widget(self.label_fecha_seleccionada) # Mostrar la fecha seleccionada
        content.add_widget(self.boton_reservar)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def on_pre_enter(self):
        self.recibir_servicio_imagen()

    #Límite de caracteres del campo de telefono
    def validar_longitud_telefono(self, instance, value):
        if len(value) > 10:
            instance.text = value[:10]

    def validar_correo_usuario(self, correo_usuario):
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(patron, correo_usuario):
            return True
        return False

    def show_date_picker(self, *args):
        date_dialog = MDDatePicker(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.selected_date = value
        self.label_fecha_seleccionada.text = f"Fecha seleccionada: {value.strftime('%d/%m/%Y')}"

    def recibir_servicio_imagen(self):
        servicio = self.datos_servicio
        ruta_imagen = servicio.get("imagen")
        if ruta_imagen and os.path.exists(ruta_imagen):
            self.imagen_servicio.source = ruta_imagen
        else:
            self.imagen_servicio.source = "image/error.png"

    def reservar(self, instance):

        servicio = self.datos_servicio

        if not self.validar_correo_usuario(self.correo_usuario.text):
            self.correo_usuario.error = True
            self.correo_usuario.helper_text = "¡¡correo_usuario invalido!!"
            return

        if servicio and isinstance(servicio, dict):
            # Recopilar los datos del usuario
            nombre = self.nombre_usuario.text
            telefono = self.telefono.text
            correo_usuario = self.correo_usuario.text
            fecha_reserva = self.selected_date
            fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Aquí se toma la fecha y hora juntas
            
            # Validacion del numero de telefono
            if not telefono.isdigit() or len(telefono) != 10:
                self.show_message_dialog("Error", "El número de telefono debe tener 10 dígitos.")
                return

            # Validar que todos los campos necesarios estén llenos
            if not all([nombre, telefono, correo_usuario, fecha_hora_actual, fecha_reserva, servicio, ]):
                self.show_message_dialog("Error", "Por favor, complete todos los campos y seleccione una fecha.")
                return

            # Aquí podrías llamar a tu función para agregar la reserva a la base de datos
            try:

                # Datos cifrados
                nombre_cifrado = fernet.encrypt(nombre.encode())
                telefono_cifrado = fernet.encrypt(str(telefono).encode())
                razon_social_cifrado = fernet.encrypt(servicio.get("razon_social").encode())
                nit_cifrado = fernet.encrypt(servicio.get("nit").encode())
                administrador_cifrado = fernet.encrypt(servicio.get("administrador").encode())

                agregar_reserva(
                    id_prestador = servicio.get("id_prestador",""),
                    razon_social=razon_social_cifrado,
                    nit=nit_cifrado,
                    administrador=administrador_cifrado,
                    ubicacion=servicio.get("ubicacion", ""),
                    tipo_servicio=servicio.get("tipo_servicio"),
                    imagen=str(servicio.get("imagen")),
                    id_usuario= App.get_running_app().id_usuario,
                    nombre_cliente=nombre_cifrado,
                    telefono_cliente=telefono_cifrado,
                    correo_cliente=correo_usuario,
                    hora_reserva=fecha_hora_actual, 
                    fecha_reserva=fecha_reserva, 
                )
                
                self.show_message_dialog("Reserva Exitosa", f"Has reservado en {servicio['razon_social']} para el {fecha_reserva.strftime('%d/%m/%Y')}.")

                # Limpiar campos después de la reserva
                self.nombre_usuario.text = ""
                self.telefono.text = ""
                self.correo_usuario.text = ""
                self.selected_date = None
                self.label_fecha_seleccionada.text = "Fecha no seleccionada"

                # Opcional: Volver a la pantalla de servicios o a una pantalla de confirmación
                app = MDApp.get_running_app()
                app.root.current = "pantallaUsuario" # O a donde quieras ir después de reservar

            except Exception as e:
                self.show_message_dialog("Error de Reserva", f"Ocurrió un error al intentar reservar: {e}")

        else:
            self.show_message_dialog("Error", "No se ha seleccionado un servicio para reservar.")


    def recibir_servicio(self, datos_servicio):
        self.datos_servicio = datos_servicio


    def show_message_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()

    def validar_longitud_telefono(self, instance, value):
        if len(value) > 10:
            instance.text = value[:10] 
    