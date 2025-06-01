from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from Database.Data_P_Servicio import modificar_prestador
from kivy.metrics import dp
from cryptography.fernet import Fernet
import os


if not os.path.exists("clave.key"):
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(Fernet.generate_key())

# Cargar la clave de cifrado
with open("clave.key", "rb") as clave_archivo:
    clave = clave_archivo.read()

fernet = Fernet(clave)

class Modificarprestador(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "modificar_prestador"
        self.id_prestador = None



        layout = MDBoxLayout(orientation="vertical", spacing=dp(10))

        top_bar = MDTopAppBar(
            title="Registro de Servicio",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
            md_bg_color="#015551"
        )
        layout.add_widget(top_bar)
        self.campos = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            size_hint=(1, None),
            radius=[15],
        )

        self.txt_nombre = MDTextField(hint_text = "Nombre Completo", helper_text = "", helper_text_mode = "on_error", mode="rectangle", icon_right="account")
        self.txt_correo = MDTextField(hint_text = "correo Electronico", helper_text = "", helper_text_mode = "on_error", mode="rectangle", icon_right="email")
        self.txt_telefono = MDTextField(hint_text = "Telefono", input_filter = "int", helper_text = "", helper_text_mode = "on_error", mode="rectangle", icon_right="phone")
        self.txt_telefono.bind(text=self.validar_longitud_telefono)

        self.registro_button = MDRaisedButton(
            text="Registrar",
            pos_hint={"center_x": 0.5},
            md_bg_color="#FE4F2D",
            on_release=self.registrar
        )

        self.campos.add_widget(self.txt_nombre)
        self.campos.add_widget(self.txt_correo)
        self.campos.add_widget(self.txt_telefono)
        self.campos.add_widget(self.registro_button)
        layout.add_widget(self.campos)
        self.add_widget(layout)

    def validar_longitud_telefono(self, instance, value):
        if len(value) > 10:
            instance.text = value[:10]

    def registrar(self, instance):
        if not all([
            self.txt_nombre.text.strip(),
            self.txt_correo.text.strip(),
            self.txt_telefono.text.strip(),
          
        ]):
            print("⚠️ Todos los campos son obligatorios.")
            return

        try:
            nombre = fernet.encrypt(self.txt_nombre.text.encode())
            telefono = fernet.encrypt(self.txt_telefono.text.encode())
            correo = self.txt_correo.text

            modificar_prestador(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                id=self.id_prestador
            )
            from kivymd.uix.snackbar import Snackbar
            Snackbar(
                MDLabel(
                    text="!!Datos Modificados con exito.¡¡"
                )).open()

            # Limpiar campos
            self.txt_nombre.text = ""
            self.txt_correo.text = ""
            self.txt_telefono.text = ""
            

            self.manager.current = "pantallaPServicio"

        except Exception as e:
            import traceback
            traceback.print_exc()

    def set_datos_prestador(self, usuario):
        self.id_prestador = usuario["id"]
        self.txt_nombre.text = usuario["nombre"]
        self.txt_correo.text = usuario["correo"]
        self.txt_telefono.text = usuario["telefono"]

    def volver_atras(self):
        self.manager.current = "pantallaPServicio"