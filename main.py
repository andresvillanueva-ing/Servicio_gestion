from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from views.LoginScreen import login_screen
from views.RegistroPServicioScreen import registro_p_servicio_screen
from views.RegistroUsuarioScreen import registro_usuario_screen
from views.RegistroScreen import Registro_Screen
from Database.Data_P_Servicio import agregar_prestador_servicio

class ServicioGestion(MDApp):
    def build(self):
        manager = MDScreenManager()
        manager.add_widget(login_screen(name="loginscreen"))
        manager.add_widget(Registro_Screen(name="registroscreen"))
        manager.add_widget(registro_usuario_screen(name="registrousuarioscreen"))
        manager.add_widget(registro_p_servicio_screen(name="registropservicioscreen"))
        agregar_prestador_servicio("andres@gmail.com", "andres villanueva", 123456 , "parqueadero la inquebrantable", 32198770141, "1234567")
        return manager
    

if __name__ == "__main__":
    ServicioGestion().run()
