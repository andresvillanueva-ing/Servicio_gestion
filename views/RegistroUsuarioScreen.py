import re
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.anchorlayout import MDAnchorLayout

class registro_usuario_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name="registrousuarioscreen"
        
        layout = MDBoxLayout(
            orientation =  "vertical",
            padding = 20,
            spacing = 10)
    
        top_bar = MDTopAppBar(
            title="Registro de Usuario",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],  
            elevation=5,
            size_hint_y=None,  
            height="56dp"  
        )
        
        
        self.nombre_usuario = MDTextField(hint_text = "Nombre Completo")
        self.correo_usuario = MDTextField(hint_text = "Correo Electronico", helper_text = "", helper_text_mode = "on_error")
        self.telefono_usuario = MDTextField(hint_text = "Telefono", input_filter = "int")
        self.telefono_usuario.bind(text=self.validar_longitud_telefono)
        self.contraseña_usuario = MDTextField(hint_text = "Contraseña", password = True, helper_text = "", helper_text_mode = "on_error")
        self.v_contraseña_usuario = MDTextField(hint_text = "verificar contraseña", password = True, helper_text = "", helper_text_mode = "on_error")
        
        self.button_registro_usuario = MDRaisedButton(text = "Registrarse", pos_hint = {"center_x": 0.5})
        self.button_registro_usuario.bind(on_press=self.registrar_usuario)
        
        google_button = MDIconButton(icon="google", pos_hint={"center_x": 0.5})
        google_button.bind(on_press= self.google_sign_in)
        
        layout.add_widget(top_bar)
        layout.add_widget(self.nombre_usuario)
        layout.add_widget(self.correo_usuario)
        layout.add_widget(self.telefono_usuario)
        layout.add_widget(self.contraseña_usuario)
        layout.add_widget(self.v_contraseña_usuario)
        layout.add_widget(self.button_registro_usuario)
        layout.add_widget(MDLabel(text="0", halign="center"))
        layout.add_widget(google_button)
        layout.add_widget(Widget())
        
        self.add_widget(layout)

    def validar_correo(self, correo_usuario):
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(patron, correo_usuario):
            return True
        return False
    
    def validar_longitud_telefono(self, instance, value):
        if len(value) > 10:
            instance.text = value[:10] 
    
    def registrar_usuario(self, instance):
        nombre = self.nombre_usuario.text
        correo = self.correo_usuario.text
        telefono = self.telefono_usuario.text
        contraseña = self.contraseña_usuario.text
        verificacion_contraseña = self.v_contraseña_usuario.text
        
        if not self.validar_correo(self.correo_usuario.text):
            self.correo_usuario.error = True
            self.correo_usuario.helper_text = "¡¡Correo invalido!!"
            return
        
        if contraseña != verificacion_contraseña:
            self.contraseña_usuario.error = True
            self.v_contraseña_usuario.error = True
            self.contraseña_usuario.helper_text = "!!Las contraseñas no coiciden¡¡"
            self.v_contraseña_usuario.helper_text = "!!Las contraseñas no coiciden¡¡"
        else:
            self.contraseña_usuario.error = False
            self.v_contraseña_usuario.error = False
            self.contraseña_usuario.helper_text = ""
            self.v_contraseña_usuario.helper_text = ""
            print('contraseñas correctas, puede continuar')
        
    def google_sign_in(self, instance):
        print("Iniciar sesion con google")
    
    def show_error(self, message):
        print("Error:", message)
        
    def volver_atras(self):
        self.manager.current = "registroscreen" 