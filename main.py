from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
from kivy.clock import Clock
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from views.LoginScreen import login_screen
from views.RegistroPServicioScreen import registro_p_servicio_screen
from views.RegistroUsuarioScreen import registro_usuario_screen
from views.RegistroScreen import Registro_Screen
from views.PantallaPServicio import Pantalla_P_Servicio
from views.RegistrarServicio import registrar_servicio_screen
from views.PantallaUsuario import Pantalla_Usuario
from views.InformacionServicios import informacion_servicios_screen
from views.ReservasScreen import reservas_screen
from views.informacion_reservas import Informacion_Reserva_Screen
from views.informacion_reserva_prestador import Informacion_Reserva_prestador_Screen
from views.ModificarInformacionServicio import modificar_servicio_screen
from views.PerfilUsuario import PerfilUsuario
from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
Builder.load_file('views/SplashScreen.kv')

class SplashScreen(Screen):
    pass

class ServicioGestion(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal" 
        self.theme_cls.theme_style = "Light"   # Define si el tema es claro u oscuro
        self.theme_cls.accent_palette = "Orange" 
        
        self.manager = MDScreenManager()
    
        self.manager.add_widget(SplashScreen(name="splashscreen"))
        self.manager.current = "splashscreen"

        Clock.schedule_once(self.cargar_datos, 10)

        self.manager.add_widget(login_screen(name="loginscreen"))
        self.manager.add_widget(Registro_Screen(name="registroscreen"))
        self.manager.add_widget(registro_usuario_screen(name="registrousuarioscreen"))
        self.manager.add_widget(registro_p_servicio_screen(name="registropservicioscreen"))
        self.manager.add_widget(Pantalla_P_Servicio(name="pantallaPServicio"))
        self.manager.add_widget(registrar_servicio_screen(name="registrarservicios"))
        self.manager.add_widget(Pantalla_Usuario(name="pantallaUsuario"))
        self.manager.add_widget(informacion_servicios_screen(name="informacionservicios"))
        self.manager.add_widget(reservas_screen(name="reservasscreen"))
        self.manager.add_widget(Informacion_Reserva_Screen(name="informacionreserva"))
        self.manager.add_widget(Informacion_Reserva_prestador_Screen(name="informacionreservaprestador"))
        self.manager.add_widget(modificar_servicio_screen(name="modificar_servicio"))
        self.manager.add_widget(PerfilUsuario(name="perfil_usuario"))


        return self.manager
    
    def cargar_datos(self, dt):
        self.manager.current = 'loginscreen'

if __name__ == "__main__":
    ServicioGestion().run()