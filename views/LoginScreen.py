from kivy.core.text import LabelBase

from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from Database.Data_P_Servicio import Verificar_datos
from Database.Data_usuario import Verificar_datos_usuario
from kivymd.uix.dialog import MDDialog
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp


class login_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "loginscreen"
        self.md_bg_color = "#FFF2F2"

        layout = RelativeLayout()
        # Color de fondo


        # Toptoolbar
        top_bar = MDBoxLayout(
            orientation="horizontal",
            pos_hint={"top": 1},
            size_hint_y=None,
            height=dp(120), 
            md_bg_color=("#015551"),  
            radius=[0, 0, dp(25), dp(25)],
        )

        titulo = MDLabel(
            text="ReservaFacil®",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H3",
            
        )

        top_bar.add_widget(titulo)
        layout.add_widget(top_bar)

        form_container = MDBoxLayout(
            orientation="vertical",
            padding=[20, 20, 20, 20],
            spacing=20,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, 0.6),
        )

        # Título
        title = MDLabel(
            text="[b][i]Iniciar sesión[/i][/b]",
            markup=True,
            font_style="H4",
            halign="center",
            theme_text_color="Custom",
            text_color=("#000000"),
        )

        # Campo de correo_usuario con icono
        self.username = MDTextField(
            hint_text="correo Electronico",
            icon_right="email",
            size_hint_x=1,
            mode="rectangle",
        )

        # Campo de contraseña con icono
        self.password = MDTextField(
            hint_text="Contraseña",
            password=True,
            icon_right="lock",
            size_hint_x=1,
            mode="rectangle",
        )

        # Botón de inicio de sesión
        login_button = MDRaisedButton(
            text="Iniciar sesión",
            pos_hint={"center_x": 0.5},
            md_bg_color=("#FE4F2D"),  
            size_hint_x=1,
            font_style="Button"
        )
        login_button.bind(on_release=self.verificar_credenciales)

        # Contenedor de "No estás registrado?" y "Regístrate"
        register_layout = MDGridLayout(cols=2)

        register_text = MDLabel(
            text="[i]No estás registrado? [/i]",
            markup=True,
            font_style="Caption",
            halign="left",
        )

        register_link = MDLabel(
            text="[ref=register][color=#FE4F2D] Regístrate[/color][/ref]",
            markup=True,
            font_size="20sp",
            halign="center",
        )
        register_link.bind(on_ref_press=self.screen_registro)

        register_layout.add_widget(register_text)
        register_layout.add_widget(register_link)
        form_container.add_widget(title)
        form_container.add_widget(self.username)
        form_container.add_widget(self.password)
        form_container.add_widget(login_button)
        form_container.add_widget(register_layout)

        layout.add_widget(form_container)
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.limpiar_campos

    def verificar_credenciales(self, instance):
        usuario = self.username.text.strip()
        contraseña = self.password.text.strip()

        if not usuario or not contraseña:
            self.mostrar_dialogo("¡Error!", "Por favor, rellene todos los campos.")
            return

        resultado = Verificar_datos(usuario, contraseña)  # Prestador
        result = Verificar_datos_usuario(usuario, contraseña)  # Cliente

        from kivy.app import App
        app = App.get_running_app()

        if result:
            app.id_usuario = result["id"]
            self.manager.current = "pantallaUsuario"
            self.limpiar_campos()
        elif resultado:
            app.id_prestador = resultado["id"]
            self.manager.current = "pantallaPServicio"
            self.limpiar_campos()
        else:
            self.mostrar_dialogo("¡Error!", "Credenciales incorrectas.")
            self.limpiar_campos()


    def mostrar_dialogo(self, titulo, mensaje):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=titulo,
            text=mensaje,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def limpiar_campos(self):
        self.username.text=""
        self.password.text=""


    def screen_registro(self, instance, value):
        self.manager.current = "registroscreen"

    