from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from Database.Data_P_Servicio import Verificar_datos
from Database.Data_usuario import Verificar_datos_usuario
from kivymd.uix.dialog import MDDialog

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
            text="[b][i]Iniciar sesión[/i][/b]",
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
            text="Iniciar sesión",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.4, 0, 1, 1),  # Color morado
            size_hint_x=1,
        )
        login_button.bind(on_release=self.verificar_credenciales)

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

    def verificar_credenciales(self, instance):
        usuario = self.username.text.strip()
        contraseña = self.password.text.strip()

        if not usuario or not contraseña:
            self.mostrar_dialogo("¡Error!", "Por favor, rellene todos los campos.")
            return

        resultado = Verificar_datos(usuario, contraseña)
        result = Verificar_datos_usuario(usuario, contraseña)

        if result:
            self.mostrar_dialogo("¡Bienvenido!", "Inicio de sesión exitoso.")
            self.manager.current = "pantallaUsuario"
        elif resultado:
            self.mostrar_dialogo("¡Bienvenido!", "Inicio de sesión exitoso.")
            self.manager.current = "pamtallaPServicio"
        else:
            self.mostrar_dialogo("¡Error!", "Credenciales incorrectas.")


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

    def screen_registro(self, instance, value):
        self.manager.current = "registroscreen"