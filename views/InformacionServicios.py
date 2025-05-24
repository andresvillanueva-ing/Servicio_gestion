from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton
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
        self.layout = MDBoxLayout(orientation="vertical", spacing=10, padding=(0,0,0,10))
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
            size_hint=(1, None),
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
            spacing=20,
            size_hint=(1, None),
            height=dp(60),
            padding=(dp(20), 0),
        )

        reservar_btn = MDRaisedButton(
            on_release=self.confirmar_reserva,
            size_hint=(1, None),
            width=dp(200),
            height=dp(48),
            md_bg_color="#FFFFFF00",
        )
        reservar_content = MDBoxLayout(orientation="vertical", spacing=5)
        reservar_content.add_widget(
            MDIcon(icon="calendar-cursor", size_hint=(None, None), size=(dp(24), dp(24)), halign="center")
        )
        reservar_content.add_widget(MDLabel(halign="center"))
        reservar_btn.add_widget(reservar_content)
        botones.add_widget(reservar_btn)

        botones.add_widget(Widget())

        ir_btn = MDRaisedButton(
            on_release=self.abrir_mapa,
            size_hint=(1, None),
            width=dp(120),
            height=dp(48),
            md_bg_color="#FFFFFF00",
        )
        ir_content = MDBoxLayout(orientation="vertical", spacing=5, )
        ir_content.add_widget(
            MDIcon(icon="bus-marker", size_hint=(1, None), size=(dp(24), dp(40)), halign="center")
        )
        ir_content.add_widget(MDLabel( halign="center"))
        ir_btn.add_widget(ir_content)
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
            padding=dp(15),
            size_hint=(1, None),
            height=dp(120),
            elevation=3,
            radius=[15],
        )
        info_box = MDBoxLayout(orientation="vertical")
        descripcion = servicio.get("descripcion", "").strip()
        if descripcion:
            info_box.add_widget(
                MDLabel(
                    text=descripcion,
                    halign="center",
                    theme_text_color="Secondary",
                    font_style="Body1",
                )
            )
        info_card.add_widget(info_box)
        self.layout.add_widget(info_card)

        # --- Informacion del servicio ---

        informacion_box = MDCard(
            orientation="vertical",
            padding=dp(10),
            size_hint=(1, None),
            elevation=2,
            radius=[15],
        )
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
        informacion_box.add_widget(administrador_box)
        informacion_box.add_widget(ubicacion_box)
        informacion_box.add_widget(horario_box)
        self.layout.add_widget(informacion_box)

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
