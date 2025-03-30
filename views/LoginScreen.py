from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.gridlayout import MDGridLayout

class login_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "loginscreen"

        
        layout = RelativeLayout()

        form_container = MDBoxLayout(
            orientation="vertical",
            padding=[40, 40, 40, 40],
            spacing=20,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, 0.6),
        )

        # Título
        title = MDLabel(
            text="[b][i]Log in[/i][/b]",
            markup=True,
            font_style="H4",
            halign="center",
            theme_text_color="Custom",
            text_color=(27,27,27,27),
        )

        # Campo de correo con icono
        self.username = MDTextField(
            hint_text="Email",
            icon_right="email",
            size_hint_x=1,
            mode="rectangle",
        )

        # Campo de contraseña con icono
        self.password = MDTextField(
            hint_text="Password",
            password=True,
            icon_right="lock",
            size_hint_x=1,
            mode="rectangle",
        )

        # Botón de inicio de sesión
        login_button = MDRaisedButton(
            text="Log in",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.4, 0, 1, 1),  # Color morado
            size_hint_x=1,
        )
        login_button.bind(on_release=self.verify_credentials)

        # Contenedor de "No estás registrado?" y "Regístrate"
        register_layout = MDGridLayout(cols=2, padding=[10, 0, 10, 0])

        register_text = MDLabel(
            text="[i]No estás registrado?[/i]",
            markup=True,
            font_style="Caption",
            theme_text_color="Hint",
            halign="right",
        )

        register_link = MDLabel(
            text="[ref=register][color=#0000FF]Regístrate[/color][/ref]",
            markup=True,
            font_style="Caption",
            halign="left",
        )
        register_link.bind(on_ref_press = self.screen_registro)

        register_layout.add_widget(register_text)
        register_layout.add_widget(register_link)
        form_container.add_widget(title)
        form_container.add_widget(self.username)
        form_container.add_widget(self.password)
        form_container.add_widget(login_button)
        form_container.add_widget(register_layout)

        layout.add_widget(form_container)
        self.add_widget(layout)

    def verify_credentials(self, instance):
        usuario = self.username.text
        contraseña = self.password.text

        if usuario == "admin" and contraseña == "1234":
            self.username.helper_text = "Acceso concedido"
            self.username.helper_text_mode = "on_focus"
        else:
            self.username.helper_text = "Credenciales incorrectas"
            self.username.helper_text_mode = "on_error"
            
    def screen_registro(self, instance, value):
        self.manager.current = "registroscreen"