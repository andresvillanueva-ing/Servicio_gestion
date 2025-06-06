"""Pantalla de informacion de servicios"""

import os

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivy_garden.mapview import MapView, MapMarker
from kivy.app import App

from plyer import filechooser
from cryptography.fernet import Fernet

from Database.Data_servicios import modificar_servicio

# Cargar o generar clave de cifrado
if not os.path.exists("clave.key"):
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(Fernet.generate_key())

# Cargar la clave de cifrado
with open("clave.key", "rb") as clave_archivo:
    clave = clave_archivo.read()

fernet = Fernet(clave)


class modificar_servicio_screen(MDScreen):
    """Clase Principal de la pantalla para modificar los datos del Servicio"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "modificar_servicio"
        self.servicio_actual = None
        self.layout = MDBoxLayout(orientation="vertical", spacing=10)
        self.add_widget(self.layout)
        self.ruta_imagen = ""
        self.map_marker = None

    def on_pre_enter(self):
        self.layout.clear_widgets()
        if self.servicio_actual:
            self.construir_ui(self.servicio_actual)

    def construir_ui(self, servicio):
        """Metodo que recibe el servicio y construye la interfaz de usuario"""

        self.layout.clear_widgets()
        self.servicio_actual = servicio
        self.ruta_imagen = servicio.get("imagen", "")

        top_bar = MDTopAppBar(
            title="Modificar de Servicio",
            left_action_items=[["arrow-left", lambda x: self.volver_atras()]],
            elevation=5,
            size_hint_y=None,
            height="56dp",
            md_bg_color="#015551",
        )
        self.layout.add_widget(top_bar)

        scroll_view = ScrollView()
        content_layout = MDBoxLayout(
            orientation="vertical", padding=10, spacing=10, size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter("height"))

        self.razon_social = MDTextField(
            text=servicio.get("razon_social"),
            hint_text="Nombre del servicio",
            mode="rectangle",
            icon_right="home-city",
        )
        self.nit = MDTextField(
            text=servicio.get("nit"),
            hint_text="NIT",
            input_filter="int",
            mode="rectangle",
            icon_right="numeric",
        )
        self.Administrador = MDTextField(
            text=servicio.get("administrador"),
            hint_text="Nombre del administrador",
            mode="rectangle",
            icon_right="account-cog",
        )
        self.Descripcion = MDTextField(
            text=servicio.get("descripcion"),
            hint_text="Descripción del servicio",
            mode="rectangle",
            icon_right="sort-alphabetical-descending",
        )
        self.horario = MDTextField(
            text=servicio.get("horario"),
            hint_text="Horario de atención. ej: 00:00 a 00:00",
            mode="rectangle",
            icon_right="alarm-check",
        )
        self.Puestos = MDTextField(
            text=servicio.get("puestos"),
            hint_text="Puestos disponibles",
            mode="rectangle",
            icon_right="arrow-all",
        )
        self.ubicacion = MDTextField(
            text=servicio.get("ubicacion"),
            hint_text="Dirección. Ej: Calle 10 #12-34",
            mode="rectangle",
            icon_right="map-marker-outline",
        )

        self.boton_imagen = MDIconButton(
            icon="image",
            icon_size="32sp",
            pos_hint={"center_x": 0.5},
            md_bg_color="#F17259",
            on_release=self.seleccionar_imagen,
        )
        self.boton_imagen.tooltip_text = "Seleccionar imagen"

        if self.ruta_imagen:
            content_layout.add_widget(MDLabel(text="Imagen actual:", halign="center"))
            content_layout.add_widget(
                Image(source=self.ruta_imagen, size_hint_y=None, height=200)
            )

        content_layout.add_widget(self.boton_imagen)

        # Campos de texto
        content_layout.add_widget(self.razon_social)
        content_layout.add_widget(self.nit)
        content_layout.add_widget(self.Administrador)
        content_layout.add_widget(self.Descripcion)
        content_layout.add_widget(self.horario)
        content_layout.add_widget(self.Puestos)
        content_layout.add_widget(self.ubicacion)

        # Mapa interactivo
        self.map_view = MapView(
            zoom=15, lat=9.2419, lon=-74.4262, size_hint_y=None, height="300dp"
        )
        self.map_view.bind(on_touch_down=self.on_map_touch)

        content_layout.add_widget(self.map_view)

        ubicacion_str = servicio.get("ubicacion")
        if ubicacion_str:
            try:
                lat_str, lon_str = ubicacion_str.split(",")
                lat, lon = float(lat_str), float(lon_str)
                self.map_marker = MapMarker(lat=lat, lon=lon)
                self.map_view.center_on(lat, lon)
                self.map_view.add_marker(self.map_marker)
            except Exception as e:
                print("Error al interpretar la ubicación:", e)

        self.registro_button = MDRaisedButton(
            text="Guardar Cambios",
            pos_hint={"center_x": 0.5},
            md_bg_color="#FE4F2D",
            on_release=self.registrar,
        )
        content_layout.add_widget(self.registro_button)

        scroll_view.add_widget(content_layout)
        self.layout.add_widget(scroll_view)

    def registrar(self, instance):
        """Metodo para registrar los datos del servicio modificados"""

        if not all(
            [
                self.razon_social.text.strip(),
                self.nit.text.strip(),
                self.Administrador.text.strip(),
                self.Descripcion.text.strip(),
                self.horario.text.strip(),
                self.Puestos.text.strip(),
                self.ubicacion.text.strip(),
            ]
        ):
            print("⚠️ Todos los campos son obligatorios.")
            return

        if not self.ruta_imagen:
            print("⚠️ No se ha seleccionado una imagen.")
            return

        try:
            razon_social_cifrado = fernet.encrypt(self.razon_social.text.encode())
            nit_cifrado = fernet.encrypt(self.nit.text.encode())
            administrador_cifrado = fernet.encrypt(self.Administrador.text.encode())
            descripcion_cifrado = fernet.encrypt(self.Descripcion.text.encode())
            horario_cifrado = fernet.encrypt(self.horario.text.encode())
            puestos_cifrado = fernet.encrypt(self.Puestos.text.encode())
            ubicacion_cifrada = fernet.encrypt(self.ubicacion.text.encode())

            modificar_servicio(
                razon_social=razon_social_cifrado,
                nit=nit_cifrado,
                administrador=administrador_cifrado,
                id_prestador=App.get_running_app().id_prestador,
                descripcion=descripcion_cifrado,
                horario=horario_cifrado,
                puestos=puestos_cifrado,
                ubicacion=ubicacion_cifrada,
                imagen=self.ruta_imagen,
            )

            from kivymd.uix.snackbar import Snackbar

            Snackbar(MDLabel(text="Servicio modificado con éxito.")).open()

            self.manager.current = "pantallaPServicio"

        except Exception as e:
            import traceback

            traceback.print_exc()

    def seleccionar_imagen(self, instance):
        """Metodo para seleccionar una imagen"""

        filechooser.open_file(
            title="Seleccionar imagen",
            filters=[("Archivos de imagen", "*.png", "*.jpg", "*.jpeg")],
            on_selection=self.imagen_seleccionada,
        )

    def imagen_seleccionada(self, seleccion):
        """Metodo para informar sobre la imagen seleccionada"""

        if seleccion:
            ruta = seleccion[0]

            class ImagenDialogLayout(BoxLayout):
                def __init__(self, ruta_img, **kwargs):
                    super().__init__(orientation="vertical", **kwargs)
                    self.add_widget(Image(source=ruta_img, size_hint=(1, 1)))

            content = ImagenDialogLayout(ruta)

            self.dialog_imagen = MDDialog(
                title="¿Esta es la imagen que deseas usar?",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        on_release=lambda x: self.dialog_imagen.dismiss(),
                    ),
                    MDFlatButton(
                        text="Aceptar", on_release=lambda x: self.confirmar_imagen(ruta)
                    ),
                ],
            )
            self.dialog_imagen.open()

    def confirmar_imagen(self, ruta):
        """Metodo para confirmar la seleccion de imagen"""

        self.ruta_imagen = ruta
        self.dialog_imagen.dismiss()

    def on_map_touch(self, mapview, touch):
        """Metodo para manejar el toque en el mapa"""

        if not self.map_view.collide_point(*touch.pos):
            return

        lat, lon = self.map_view.get_latlon_at(touch.x, touch.y)
        self.ubicacion.text = f"{lat:.6f},{lon:.6f}"

        if self.map_marker:
            self.map_view.remove_marker(self.map_marker)

        self.map_marker = MapMarker(lat=lat, lon=lon)
        self.map_view.add_marker(self.map_marker)

    def volver_atras(self):
        self.manager.current = "pantallaPServicio"
