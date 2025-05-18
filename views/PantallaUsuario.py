from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.metrics import dp
from Database.Data_sercivios import obtener_servicios_por_tipo
from kivymd.uix.toolbar import MDTopAppBar


class Pantalla_Usuario(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pantallaUsuario"

        