from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from views.LoginScreen import login_screen
from views.RegistroPServicioScreen import registro_p_servicio_screen
from views.RegistroUsuarioScreen import registro_usuario_screen
from views.RegistroScreen import Registro_Screen
from views.PantallaPServicio import Pantalla_P_Servicio
from views.RegistrarServicio import registrar_servicio_screen
from views.PantallaUsuario import PantallaUsuario
from kivy.app import App

class ServicioGestion(MDApp):
    def build(self):

        manager = MDScreenManager()
        manager.add_widget(login_screen(name="loginscreen"))
        manager.add_widget(Registro_Screen(name="registroscreen"))
        manager.add_widget(registro_usuario_screen(name="registrousuarioscreen"))
        manager.add_widget(registro_p_servicio_screen(name="registropservicioscreen"))
        manager.add_widget(Pantalla_P_Servicio(name="pantallaPServicio"))
        manager.add_widget(registrar_servicio_screen(name="registrarservicios"))
        manager.add_widget(PantallaUsuario(name="pantalla_usuario"))
        return manager
    
if __name__ == "__main__":
    ServicioGestion().run()