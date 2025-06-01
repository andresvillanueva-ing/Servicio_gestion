from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivy.app import App
from plyer import filechooser
from cryptography.fernet import Fernet
import os

from kivy_garden.mapview import MapView, MapMarker
from kivy.clock import Clock

from Database.Data_sercivios import agregar_servicio

# Cargar o generar clave de cifrado
if not os.path.exists("clave.key"):
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(Fernet.generate_key())

# Cargar la clave de cifrado
with open("clave.key", "rb") as clave_archivo:
    clave = clave_archivo.read()

fernet = Fernet(clave)

class registrar_servicio_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "registrarservicios"
        self.ruta_imagen = ""
        self.map_marker = None

        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')

        # Top AppBar
        top_bar = MDTopAppBar(
            title="Registro de Servicio",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
            md_bg_color="#015551"
        )
        main_layout.add_widget(top_bar)

        # ScrollView para el contenido
        scroll_view = ScrollView()
        content_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        self.razon_social = MDTextField(hint_text="Razón social", mode="rectangle", icon_right="home-city")
        self.nit = MDTextField(hint_text="NIT", input_filter="int", mode="rectangle", icon_right="numeric")
        self.Administrador = MDTextField(hint_text="Nombre del administrador", mode="rectangle", icon_right="account-cog")
        self.Descripcion = MDTextField(hint_text="Descripción del servicio", mode="rectangle", icon_right="sort-alphabetical-descending")
        self.horario = MDTextField(hint_text="Horario de atención. ej: 00:00 a 00:00", mode="rectangle", icon_right="alarm-check")
        self.Puestos = MDTextField(hint_text="Puestos disponibles", mode="rectangle", icon_right="arrow-all")

        self.ubicacion = MDTextField(
            hint_text="Coordenadas (lat, lon)",
            helper_text="Ubicación seleccionada en el mapa",
            helper_text_mode="on_focus",
            mode="rectangle",
            icon_right="map-marker",
            readonly=True
        )
        self.map_view = MapView(zoom=15, lat=4.710989, lon=-74.072090, size_hint_y=None, height="300dp")
        self.map_view.bind(on_touch_down=self.colocar_marcador)

        self.boton_imagen = MDIconButton(
            icon="image",
            icon_size="32sp",
            pos_hint={"center_x": 0.5},
            md_bg_color="#F17259",
            on_release=self.seleccionar_imagen,
        )

        self.tipo_servicios_button = MDFlatButton(
            text="Tipo de servicio",
            pos_hint={"center_x": 0.5},
            md_bg_color="#F17259"
        )

        menu_items = [
            {"text": "Hotel", "on_release": lambda x="Hotel": self.set_tipo_servicio(x)},
            {"text": "Parqueadero", "on_release": lambda x="Parqueadero": self.set_tipo_servicio(x)},
            {"text": "Restaurante", "on_release": lambda x="Restaurante": self.set_tipo_servicio(x)}
        ]

        self.tipo_servicio_menu = MDDropdownMenu(
            caller=self.tipo_servicios_button,
            items=menu_items,
            width_mult=4
        )
        self.tipo_servicios_button.bind(on_release=lambda *args: self.tipo_servicio_menu.open())
 
        self.registro_button = MDRaisedButton(
            text="Registrar",
            pos_hint={"center_x": 0.5},
            md_bg_color="#FE4F2D",
            on_release=self.registrar
        )

        # Agregar widgets al layout
        content_layout.add_widget(self.razon_social)
        content_layout.add_widget(self.nit)
        content_layout.add_widget(MDLabel(text="Seleccionar Tipo de servicio", halign="center"))
        content_layout.add_widget(self.tipo_servicios_button)
        content_layout.add_widget(self.Administrador)
        content_layout.add_widget(self.Descripcion)
        content_layout.add_widget(self.horario)
        content_layout.add_widget(self.Puestos)
        content_layout.add_widget(MDLabel(text="Selecciona la ubicación en el mapa:", halign="center"))
        content_layout.add_widget(self.map_view)
        content_layout.add_widget(self.ubicacion)
        content_layout.add_widget(self.boton_imagen)
        content_layout.add_widget(self.registro_button)

        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def colocar_marcador(self, instance, touch):
        if not self.map_view.collide_point(*touch.pos):
            return

        lat, lon = self.map_view.get_latlon_at(touch.x, touch.y)
        self.ubicacion.text = f"{lat:.67}, {lon:.6f}"

        if self.map_marker:
            self.map_view.remove_widget(self.map_marker)

        self.map_marker = MapMarker(lat=lat, lon=lon)
        self.map_view.add_widget(self.map_marker)


    def set_tipo_servicio(self, tipo):
        self.tipo_servicios_button.text = tipo
        self.tipo_servicio_menu.dismiss()

    def seleccionar_imagen(self, instance):
        filechooser.open_file(
            title="Seleccionar imagen",
            filters=[("Archivos de imagen", "*.png", "*.jpg", "*.jpeg")],
            on_selection=self.imagen_seleccionada
        )

    def imagen_seleccionada(self, seleccion):
        if seleccion:
            ruta = seleccion[0]

            class ImagenDialogLayout(BoxLayout):
                def __init__(self, ruta_img, **kwargs):
                    super().__init__(orientation='vertical', **kwargs)
                    self.add_widget(Image(source=ruta_img, size_hint=(1, 1)))

            content = ImagenDialogLayout(ruta)

            self.dialog_imagen = MDDialog(
                title="¿Esta es la imagen que deseas usar?",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="Cancelar", on_release=lambda x: self.dialog_imagen.dismiss()),
                    MDFlatButton(text="Aceptar", on_release=lambda x: self.confirmar_imagen(ruta)),
                ],
            )
            self.dialog_imagen.open()

    def confirmar_imagen(self, ruta):
        self.ruta_imagen = ruta
        self.dialog_imagen.dismiss()

    def registrar(self, instance):
        if not all([
            self.razon_social.text.strip(),
            self.nit.text.strip(),
            self.Administrador.text.strip(),
            self.Descripcion.text.strip(),
            self.horario.text.strip(),
            self.Puestos.text.strip(),
            self.ubicacion.text.strip(),
            self.tipo_servicios_button.text != "Tipo de servicio"
        ]):
            print("⚠️ Todos los campos son obligatorios.")
            return

        if not self.ruta_imagen:
            print("⚠️ No se ha seleccionado una imagen.")
            return

        try:
            razon_social_cifrado = fernet.encrypt(self.razon_social.text.encode())
            nit_cifrado = fernet.encrypt(self.nit.text.encode())
            tipo_servicio_cifrado = self.tipo_servicios_button.text
            administrador_cifrado = fernet.encrypt(self.Administrador.text.encode())
            descripcion_cifrado = fernet.encrypt(self.Descripcion.text.encode())
            horario_cifrado = fernet.encrypt(self.horario.text.encode())
            puestos_cifrado = fernet.encrypt(self.Puestos.text.encode())
            ubicacion_cifrada = fernet.encrypt(self.ubicacion.text.encode())

            agregar_servicio(
                razon_social=razon_social_cifrado,
                nit=nit_cifrado,
                tipo_servicio=tipo_servicio_cifrado,
                administrador=administrador_cifrado,
                id_prestador=App.get_running_app().id_prestador,
                descripcion=descripcion_cifrado,
                horario=horario_cifrado,
                puestos=puestos_cifrado,
                ubicacion=ubicacion_cifrada,
                imagen=self.ruta_imagen
            )

            from kivymd.uix.snackbar import Snackbar
            Snackbar(
                MDLabel(
                    text="Servicio modificado con éxito."
                )).open()

            # Limpiar campos
            self.razon_social.text = ""
            self.nit.text = ""
            self.Administrador.text = ""
            self.Descripcion.text = ""
            self.horario.text = ""
            self.Puestos.text = ""
            self.tipo_servicios_button.text = "Tipo de servicio"
            self.ruta_imagen = ""
            self.ubicacion.text = ""
            if self.map_marker:
                self.map_view.remove_widget(self.map_marker)
                self.map_marker = None

            self.manager.current = "pantallaPServicio"

        except Exception as e:
            import traceback
            traceback.print_exc()

    def volver_atras(self):
        self.manager.current = "pantallaPServicio"
