from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.widget import Widget


class informacion_servicios_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "informacionservicios"
        self.layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        self.add_widget(self.layout)
        self.dialog = None
        self.datos_servicio = None
        self.servicio_actual = None

    def on_pre_enter(self):
        self.layout.clear_widgets()
        if self.servicio_actual:
            self.construir_ui(self.servicio_actual)

    def construir_ui(self, servicio):
        self.layout.clear_widgets()
        self.datos_servicio = servicio

        # --- Encabezado con imagen y título superpuesto ---
        encabezado = MDCard(
            size_hint=(1, 1),
            height=dp(260),
            radius=[0, 0, 20, 20],
            elevation=6,
            padding=0,
            orientation="vertical",
            md_bg_color="#015551",
        )

        if servicio.get("imagen"):
            imagen = Image(
                source=servicio["imagen"],
                size_hint=(1, 1),
                allow_stretch=True,
                keep_ratio=False,
            )
        else:
            imagen = MDLabel(
                text="[b]Foto no disponible[/b]",
                markup=True,
                halign="center",
                valign="middle",
                size_hint=(1, 1),
                theme_text_color="Secondary",
            )

        encabezado.add_widget(imagen)

        # Título superpuesto sobre la imagen
        titulo_label = MDLabel(
            text=f"[b]{servicio.get('razon_social', 'Servicio') }[/b]",
            markup=True,
            font_style="H5",
            size_hint=(1, None),
            height=dp(40),
            pos_hint={"center_x": 0.5},
            theme_text_color="Primary",
            halign="center",
            valign="middle",
        )
        encabezado.add_widget(titulo_label)

        self.layout.add_widget(encabezado)

        # ScrollView para el contenido
        
        scroll_view = ScrollView()
        content_layout = MDBoxLayout(
            orientation="vertical", padding=10, spacing=10, size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter("height"))

        # --- Botones ---
        botones = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5} 
        )

        reservar_btn = MDRectangleFlatIconButton(
            text="Reservar",
            icon="calendar-plus",
            on_release=self.confirmar_reserva,
            size_hint=(1, None),
        )
        ir_btn = MDRectangleFlatIconButton(
            text="ir a mapa",
            icon="bus-marker",
            on_release=self.confirmar_reserva,
            size_hint=(1, None),
        )
        botones.add_widget(reservar_btn)
        botones.add_widget(ir_btn)

        self.layout.add_widget(botones)

        # --- Sección Información ---
        self.layout.add_widget(
            MDLabel(
                text="[b]Información del servicio[/b]",
                markup=True,
                font_style="H6",
                halign="center",
                size_hint_y=None,
                height=dp(30),
                padding=(0, dp(10)),
            )
        )
        info_card = MDCard(
            orientation="vertical",
            padding=dp(10),
            size_hint=(1, None),
            height=dp(300),
            elevation=2,
            radius=[15],
        )
        
        descripcion = servicio.get("descripcion")
        descripcion_box = MDBoxLayout(orientation="horizontal", spacing=10)
        descripcion_box.add_widget(
            MDLabel(
                text=descripcion, halign="center"
            )
        )
        # --- Informacion del servicio ---
        administrador_box = MDBoxLayout(orientation="horizontal", spacing=10)
        administrador_box.add_widget(
            MDIcon(icon="account-cog", size_hint=(None, None), size=(dp(24), dp(24)))
        )
        administrador_box.add_widget(
            MDLabel(
                text=servicio.get("administrador", "Sin administrador"), halign="left"
            )
        )
        ubicacion_box = MDBoxLayout(orientation="horizontal", spacing=10)
        ubicacion_box.add_widget(
            MDIcon(icon="map-marker", size_hint=(None, None), size=(dp(24), dp(24)))
        )
        ubicacion_box.add_widget(
            MDLabel(text=servicio.get("ubicacion", "No disponible"), halign="left")
        )
        horario_box = MDBoxLayout(orientation="horizontal", spacing=10)
        horario_box.add_widget(
            MDIcon(
                icon="clock-time-four-outline",
                size_hint=(None, None),
                size=(dp(24), dp(24)),
            )
        )
        horario_box.add_widget(
            MDLabel(
                text=servicio.get("horario", "Abierto de 7:00 a 22:00"), halign="left"
            )
        )
        info_card.add_widget(MDLabel(text="Descripcion del servicio", halign="center", font_style="H6"))
        info_card.add_widget(descripcion_box)
        info_card.add_widget(MDLabel(text="Informacion de servicio", halign="center", font_style="H6"))
        info_card.add_widget(administrador_box)
        info_card.add_widget(ubicacion_box)
        info_card.add_widget(horario_box)
        content_layout.add_widget(info_card)
        scroll_view.add_widget(content_layout)
        self.layout.add_widget(scroll_view)

    def confirmar_reserva(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                title="¿Confirmar reserva?",
                text="¿Deseas realizar la reserva de este servicio?",
                buttons=[
                    MDRaisedButton(text="Cancelar", on_release=self.cancelar_dialogo),
                    MDRaisedButton(text="Confirmar", on_release=self.realizar_reserva),
                ],
            )
        self.dialog.open()

    def cancelar_dialogo(self, *args):
        self.dialog.dismiss()

    def realizar_reserva(self, *args):
        self.dialog.dismiss()
        from kivymd.app import MDApp

        app = MDApp.get_running_app()
        pantalla_reservas = app.root.get_screen("reservasscreen")
        pantalla_reservas.recibir_servicio(self.datos_servicio)
        app.root.current = "reservasscreen"

    def abrir_mapa(self, *args):
        print("Abrir mapa con ubicación:", self.datos_servicio.get("ubicacion"))
