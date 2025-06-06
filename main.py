"""Este módulo contiene la clase principal de la aplicación."""

from kivy.config import Config
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from views.login_screen import login_screen
from views.registro_p_servicio_screen import registro_p_servicio_screen
from views.registro_usuario_screen import registro_usuario_screen
from views.registro_screen import Registro_Screen
from views.pantalla_p_servicio import Pantalla_P_Servicio
from views.registrar_servicio import registrar_servicio_screen
from views.pantalla_usuario import Pantalla_Usuario
from views.informacion_servicios import informacion_servicios_screen
from views.reservas_screen import reservas_screen
from views.informacion_reservas import Informacion_Reserva_Screen
from views.informacion_reserva_prestador import Informacion_Reserva_prestador_Screen
from views.modificar_informacion_servicio import modificar_servicio_screen
from views.perfil_usuario import PerfilUsuario
from views.perfil_prestador import Perfilprestador
from views.modificar_usuario import ModificarUsuario
from views.modificar_prestadores import Modificarprestador
from views.mapa import Mapa_Screen


Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")

Builder.load_file("views/SplashScreen.kv")

class SplashScreen(Screen):
    """Pantalla de presentación (Splash Screen)."""


class ServicioGestion(MDApp):
    """Clase principal de la aplicación que extiende MDApp."""

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.accent_palette = "Orange"

        self.manager = MDScreenManager()
        self.manager.add_widget(SplashScreen(name="splashscreen"))
        self.manager.current = "splashscreen"

        Clock.schedule_once(self.cargar_datos, 10)

        self.manager.add_widget(login_screen(name="loginscreen"))
        self.manager.add_widget(Registro_Screen(name="registroscreen"))
        self.manager.add_widget(registro_usuario_screen(name="registrousuarioscreen"))
        self.manager.add_widget(
            registro_p_servicio_screen(name="registropservicioscreen")
        )
        self.manager.add_widget(Pantalla_P_Servicio(name="pantallaPServicio"))
        self.manager.add_widget(registrar_servicio_screen(name="registrarservicios"))
        self.manager.add_widget(Pantalla_Usuario(name="pantallaUsuario"))
        self.manager.add_widget(
            informacion_servicios_screen(name="informacionservicios")
        )
        self.manager.add_widget(reservas_screen(name="reservasscreen"))
        self.manager.add_widget(Informacion_Reserva_Screen(name="informacionreserva"))
        self.manager.add_widget(
            Informacion_Reserva_prestador_Screen(name="informacionreservaprestador")
        )
        self.manager.add_widget(modificar_servicio_screen(name="modificar_servicio"))
        self.manager.add_widget(PerfilUsuario(name="perfil_usuario"))
        self.manager.add_widget(Perfilprestador(name="perfil_prestador"))
        self.manager.add_widget(ModificarUsuario(name="modificar_usuario"))
        self.manager.add_widget(Modificarprestador(name="modificar_prestador"))
        self.manager.add_widget(Mapa_Screen(name="mapascreen"))

        return self.manager

    def cargar_datos(self, dt):
        """Carga las pantallas de la aplicación después del SplashScreen."""

        self.manager.current = "loginscreen"


if __name__ == "__main__":
    ServicioGestion().run()
