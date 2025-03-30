from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar

class Registro_Screen(MDScreen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "registroscreen"

        
        root_layout = MDBoxLayout(orientation="vertical")

        
        top_bar = MDTopAppBar(
            title="Registro",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]], 
            elevation=5,
            size_hint_y=None,  
            height="56dp"  
        )

        
        button_layout = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            padding=50,
        )

        # Botón de Usuario
        self.user_button = MDRaisedButton(
            text="Usuario", 
            size_hint=(None, None),
            size=(250, 50),
            pos_hint={"center_x": 0.5}  
        )
        self.user_button.bind(on_press=self.registro_usuario)

        # Botón de Prestador de Servicios
        self.service_button = MDRaisedButton(  
            text="Prestador de Servicios",
            size_hint=(None, None),
            size=(250, 50),
            pos_hint={"center_x": 0.5}  
        )
        self.service_button.bind(on_press=self.registro_servicio)

        
        button_layout.add_widget(self.user_button)
        button_layout.add_widget(self.service_button)

        root_layout.add_widget(top_bar)  # Se agrega primero para que esté arriba
        root_layout.add_widget(button_layout)  # Luego el contenido principal

        self.add_widget(root_layout)

    def registro_usuario(self, instance):
        self.manager.current = "registrousuarioscreen"

    def registro_servicio(self, instance):
        self.manager.current = "registropservicioscreen"

    def volver_atras(self):
        self.manager.current = "loginscreen"
