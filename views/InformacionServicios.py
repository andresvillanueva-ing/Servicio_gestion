from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.widget import Widget

class informacion_servicios_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "informacionservicios"
        self.layout = MDBoxLayout(orientation='vertical', spacing=0, padding=0)
        self.add_widget(self.layout)
        self.dialog = None
        self.datos_servicio = None

    def mostrar_info(self, servicio):
        self.layout.clear_widgets()
        self.datos_servicio = servicio

        # Encabezado con imagen como fondo
        encabezado = MDCard(
            orientation="vertical",
            padding=0,
            spacing=0,
            size_hint=(1, None),
            height=dp(260),
            elevation=2,
            radius=[20, 20, 0, 0],  
        )

        if servicio.get("imagen"):
            imagen = Image(
                source=servicio["imagen"],
                size_hint=(1, 1),
                allow_stretch=True,
                keep_ratio=False
            )
        else:
            imagen = MDLabel(
                text="[b]Foto no disponible[/b]",
                markup=True,
                halign="center",
                valign="middle",
                size_hint=(1, 1)
            )

        encabezado.add_widget(imagen)
        self.layout.add_widget(encabezado)

        # Botones
        botones = MDBoxLayout(orientation="horizontal", spacing=10)
        botones_card = MDCard(
            padding=dp(10),
            size_hint=(1, None),
            height=dp(70),
            elevation=0,
            radius=[0, 0, 20, 20],
        )

        reservar_btn = MDRaisedButton(
            on_release=self.confirmar_reserva,
            size_hint=(None, None),
            width=dp(140),
            height=dp(48),
        )
        reservar_content = MDBoxLayout(orientation="horizontal", spacing=5)
        reservar_content.add_widget(MDIcon(icon="calendar-check", size_hint=(None, None), size=(dp(24), dp(24))))
        reservar_content.add_widget(MDLabel(halign="center"))
        reservar_btn.add_widget(reservar_content)
        botones.add_widget(reservar_btn)

        botones.add_widget(Widget())

        ir_btn = MDRaisedButton(
            on_release=self.abrir_mapa,
            size_hint=(None, None),
            width=dp(120),
            height=dp(48),
        )
        ir_content = MDBoxLayout(orientation="horizontal", spacing=5)
        ir_content.add_widget(MDIcon(icon="map-marker", size_hint=(None, None), size=(dp(24), dp(24))))
        ir_content.add_widget(MDLabel(halign="center"))
        ir_btn.add_widget(ir_content)
        botones.add_widget(ir_btn)

        botones_card.add_widget(botones)
        self.layout.add_widget(botones_card)

        # Título de sección
        self.layout.add_widget(MDLabel(
            text="[b]Información del servicio[/b]",
            markup=True,
            font_style="Subtitle1",
            halign="center",
            padding=(10, 0)
        ))

        # Descripción y precio
        info_box = MDBoxLayout(
            orientation="vertical",
            spacing=5,
            padding=dp(10),
            size_hint=(1, None),
            height=dp(100)
        )

        descripcion = servicio.get('descripcion', '').strip()
        if descripcion:
            info_box.add_widget(MDLabel(
                text=descripcion,
                halign="left",
                theme_text_color="Secondary"
            ))

        precio = servicio.get("precio", "$")
        info_box.add_widget(MDLabel(
            text=f"Precio: {precio}",
            halign="left",
            theme_text_color="Primary"
        ))

        self.layout.add_widget(info_box)

        # Ubicación
        self.layout.add_widget(MDLabel(
            text="[b]Ubicación[/b]",
            markup=True,
            font_style="Subtitle1",
            halign="left",
            padding=(10, 0)
        ))

        ubicacion = servicio.get("ubicacion", "Ubicación no disponible")
        ubicacion_box = MDBoxLayout(
            orientation="horizontal",
            padding=dp(10),
            size_hint=(1, None),
            height=dp(50)
        )
        ubicacion_box.add_widget(MDIcon(icon="map-marker", size_hint=(None, None), size=(dp(24), dp(24))))
        ubicacion_box.add_widget(MDLabel(text=ubicacion, halign="left"))
        self.layout.add_widget(ubicacion_box)

        # Horario
        self.layout.add_widget(MDLabel(
            text="[b]Horario de atención[/b]",
            markup=True,
            font_style="Subtitle1",
            halign="left",
            padding=(10, 0)
        ))

        horario = servicio.get("horario", "Abierto de 7:00 a 22:00")
        horario_box = MDBoxLayout(
            orientation="horizontal",
            padding=dp(10),
            size_hint=(1, None),
            height=dp(50)
        )
        horario_box.add_widget(MDIcon(
            icon="clock-time-four-outline",
            size_hint=(None, None),
            size=(dp(24), dp(24))
        ))
        horario_box.add_widget(MDLabel(text=horario, halign="left"))
        self.layout.add_widget(horario_box)

    def confirmar_reserva(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                title="¿Confirmar reserva?",
                text="¿Deseas realizar la reserva de este servicio?",
                buttons=[
                    MDRaisedButton(text="Cancelar", on_release=self.cancelar_dialogo),
                    MDRaisedButton(text="Confirmar", on_release=self.realizar_reserva)
                ]
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



