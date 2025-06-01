from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.widget import Widget
from kivymd.uix.floatlayout import MDFloatLayout

class Registro_Screen(MDScreen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "registroscreen"

        # Layout principal vertical
        root_layout = MDBoxLayout(orientation="vertical")
        # Color de fondo
        root_layout.md_bg_color = ("#FDFBEE")
        # Barra superior
        top_bar = MDTopAppBar(
            title="Registro",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]], 
            elevation=5,
            size_hint_y=None,  
            height="56dp",
            md_bg_color=("#015551"),  # Color morado

        )
        # Layout flotante para centrar botones
        float_layout = MDFloatLayout()

        # Botón de Usuario
        self.user_button = MDRaisedButton(
            text="Usuario", 
            size_hint=(None, None),
            size=(250, 50),
            font_style="Button",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            md_bg_color=("#FE4F2D") 
        )
        self.user_button.bind(on_press=self.registro_usuario)

        # Botón de Prestador de Servicios
        self.service_button = MDRaisedButton(  
            text="Prestador de Servicios",
            size_hint=(None, None),
            size=(250, 50),
            font_style="Button",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            md_bg_color=("#FE4F2D")  
        )
        self.service_button.bind(on_press=self.registro_servicio)

        # Agregar botones al layout flotante
        float_layout.add_widget(self.user_button)
        float_layout.add_widget(self.service_button)

        # Agregar widgets al layout principal
        root_layout.add_widget(top_bar)
        root_layout.add_widget(float_layout)

        self.add_widget(root_layout)

    def registro_usuario(self, instance):
        self.manager.current = "registrousuarioscreen"

    def registro_servicio(self, instance):
        self.manager.current = "registropservicioscreen"

    def volver_atras(self):
        self.manager.current = "loginscreen"
