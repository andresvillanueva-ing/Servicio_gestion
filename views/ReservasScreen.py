# views/ReservasScreen.py

from kivymd.uix.screen import MDScreen
from Database.Data_Reservas import agregar_reserva # Asegúrate de que esta importación sea correcta
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.dialog import MDDialog # Importar MDDialog para mensajes al usuario


class reservas_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "reservasscreen"
        self.datos_servicio = None # Inicializa esta propiedad para almacenar el servicio
        self.selected_date = None # Para almacenar la fecha seleccionada

        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        scroll = ScrollView()
        content = MDBoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        self.nombre_usuario = MDTextField(hint_text="Nombre completo")
        self.telefono = MDTextField(hint_text="Teléfono")
        self.correo = MDTextField(hint_text="Correo electrónico")

        self.boton_fecha = MDRaisedButton(
            text="Seleccionar fecha",
            pos_hint={"center_x": 0.5},
            on_release=self.show_date_picker
        )
        self.label_fecha_seleccionada = MDLabel(
            text="Fecha no seleccionada",
            halign="center",
            theme_text_color="Secondary"
        )


        self.boton_reservar = MDRaisedButton(
            text="Reservar",
            pos_hint={"center_x": 0.5},
            on_release=self.reservar
        )

        content.add_widget(MDLabel(text="Datos de la reserva", halign="center"))
        content.add_widget(self.nombre_usuario)
        content.add_widget(self.telefono)
        content.add_widget(self.correo)
        content.add_widget(self.boton_fecha)
        content.add_widget(self.label_fecha_seleccionada) # Mostrar la fecha seleccionada
        content.add_widget(self.boton_reservar)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def show_date_picker(self, *args):
        date_dialog = MDDatePicker(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.selected_date = value
        self.label_fecha_seleccionada.text = f"Fecha seleccionada: {value.strftime('%d/%m/%Y')}"


    def reservar(self, instance):
        # ¡AQUÍ ESTÁ LA CORRECCIÓN! Accede a la propiedad self.datos_servicio
        servicio = self.datos_servicio

        if servicio and isinstance(servicio, dict):
            # Recopilar los datos del usuario
            nombre = self.nombre_usuario.text
            telefono = self.telefono.text
            correo = self.correo.text
            fecha_reserva = self.selected_date

            # Validar que todos los campos necesarios estén llenos
            if not all([nombre, telefono, correo, fecha_reserva, servicio]):
                self.show_message_dialog("Error", "Por favor, complete todos los campos y seleccione una fecha.")
                return

            # Aquí podrías llamar a tu función para agregar la reserva a la base de datos
            try:
                id_servicio = servicio.get("id", "ID_NO_DISPONIBLE") # Asegúrate de que tus servicios tengan un 'id'
                razon_social = servicio.get("razon_social", "N/A")

                # Ejemplo de cómo podrías llamar a agregar_reserva
                # agregar_reserva(id_servicio, razon_social, nombre, telefono, correo, fecha_reserva.strftime('%Y-%m-%d'))
                self.show_message_dialog("Reserva Exitosa", f"Has reservado en {razon_social} para el {fecha_reserva.strftime('%d/%m/%Y')}.")

                # Limpiar campos después de la reserva
                self.nombre_usuario.text = ""
                self.telefono.text = ""
                self.correo.text = ""
                self.selected_date = None
                self.label_fecha_seleccionada.text = "Fecha no seleccionada"

                # Opcional: Volver a la pantalla de servicios o a una pantalla de confirmación
                app = MDApp.get_running_app()
                app.root.current = "pantallaUsuario" # O a donde quieras ir después de reservar

            except Exception as e:
                self.show_message_dialog("Error de Reserva", f"Ocurrió un error al intentar reservar: {e}")

        else:
            self.show_message_dialog("Error", "No se ha seleccionado un servicio para reservar.")


    def recibir_servicio(self, datos_servicio):
        self.datos_servicio = datos_servicio
        # Opcional: Actualizar algún label en la pantalla de reservas con el nombre del servicio
        # self.ids.nombre_servicio_label.text = f"Reservar en: {datos_servicio.get('razon_social', 'N/A')}"


    def show_message_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()