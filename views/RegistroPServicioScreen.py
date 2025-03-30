from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.anchorlayout import MDAnchorLayout
import re
class registro_p_servicio_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name ="registropservicioscreen"
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        
        top_bar = MDTopAppBar(
            title="Registro de Servicio",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],  # Agregamos la flecha
            elevation=5
        )
        
        self.correo = MDTextField(hint_text="Correo electrónico")
        self.nombre = MDTextField(hint_text="Nombre")
        self.nit = MDTextField(hint_text="NIT")
        self.razon = MDTextField(hint_text="Razón social")
        self.contraseña = MDTextField(hint_text="Contraseña", password=True)
        self.vcontraseña = MDTextField(hint_text="Confirmar contraseña", password=True)
        
        button_container = MDAnchorLayout(anchor_x="center")
        self.registro_button = MDRaisedButton(text="Registrar", pos_hint = {"center_x": 0.5}, on_release=self.registrar)
        layout.add_widget(top_bar)
        layout.add_widget(self.correo)
        layout.add_widget(self.nombre)
        layout.add_widget(self.nit)
        layout.add_widget(self.razon)
        layout.add_widget(self.contraseña)
        layout.add_widget(self.vcontraseña)
        layout.add_widget(self.registro_button)
        
        self.add_widget(layout)
    
    def validar_correo(self, correo):
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(patron, correo):
            return True
        return False
    
    
    def registrar(self, instance):
        if not self.validar_correo(self.correo.text):
            print("Correo inválido. Introduce un correo válido.")
            return
        
        if self.contraseña.text != self.vcontraseña.text:
            print("Las contraseñas no coinciden")
            return
        
        print("Registro exitoso para:", self.nombre.text)

    def volver_atras(self):
        self.manager.current = "registroscreen" 