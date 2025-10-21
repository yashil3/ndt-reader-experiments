import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivy.properties import BooleanProperty
import serial
import pandas as pd
import threading
import time


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []


class NDTThicknessApp(App):
    def build(self):
        self.data = []           # Store thickness readings
        self.serial_port = None
        self.running = False
        self.last_value = None
        self.timer = None

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # UI Elements
        self.thickness_label = Label(text='Thickness: -- mm', font_size=24)

        self.port_input = TextInput(hint_text='Enter Serial Port (e.g., COM3 or /dev/ttyUSB0)', multiline=False)
        self.connect_button = Button(text='Connect', size_hint_y=None, height=50)
        self.connect_button.bind(on_press=self.connect_serial)

        self.record_button = Button(text='Record Reading', size_hint_y=None, height=50)
        self.record_button.bind(on_press=self.record_reading)

        self.export_button = Button(text='Export to CSV', size_hint_y=None, height=50)
        self.export_button.bind(on_press=self.export_to_csv)

        self.rv = RV()

        layout.add_widget(self.port_input)
        layout.add_widget(self.connect_button)
        layout.add_widget(self.thickness_label)
        layout.add_widget(self.record_button)
        layout.add_widget(self.export_button)
        layout.add_widget(self.rv)

        return layout

    def connect_serial(self, instance):
        port = self.port_input.text.strip()
        if not port:
            self.thickness_label.text = 'Enter a valid serial port.'
            return

        try:
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            self.running = True
            self.read_thread = threading.Thread(target=self.read_serial)
            self.read_thread.start()
            self.connect_button.text = 'Connected'
            self.connect_button.disabled = True
            self.thickness_label.text = 'Connected. Waiting for data...'
        except Exception as e:
            self.thickness_label.text = f'Error: {str(e)}'

    def read_serial(self):
        """
        Continuously read thickness data from the serial port.
        Adjust parsing logic as per your NDT device’s output format.
        """
        while self.running:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                if line:
                    # Example formats: "THK=3.52", "3.52", or "T: 3.52mm"
                    value = self.parse_thickness(line)
                    if value is not None:
                        Clock.schedule_once(lambda dt: self.update_thickness(value))
                time.sleep(0.1)
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.thickness_label, 'text', f'Error: {e}'))
                break

    def parse_thickness(self, raw_line):
        """Extract numeric thickness value from the device output."""
        import re
        match = re.search(r'([0-9]*\.?[0-9]+)', raw_line)
        if match:
            return float(match.group(1))
        return None

    def update_thickness(self, value):
        self.thickness_label.text = f'Thickness: {value:.3f} mm'
        self.last_value = value

    def record_reading(self, instance):
        if self.last_value is not None:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self.data.append({'Timestamp': timestamp, 'Thickness (mm)': self.last_value})
            self.update_rv()
        else:
            self.thickness_label.text = 'No reading to record.'

    def update_rv(self):
        self.rv.data = [{'text': f"{row['Timestamp']} - {row['Thickness (mm)']} mm"} for row in self.data]

    def export_to_csv(self, instance):
        if not self.data:
            self.thickness_label.text = 'No data to export.'
            return
        try:
            df = pd.DataFrame(self.data)
            df.to_csv('thickness_readings.csv', mode='a', index=False, header=False)
            self.data.clear()
            self.update_rv()
            self.thickness_label.text = 'Data exported to thickness_readings.csv'
        except Exception as e:
            self.thickness_label.text = f'Export failed: {str(e)}'

    def on_stop(self):
        self.running = False
        if self.serial_port:
            self.serial_port.close()


if __name__ == '__main__':
    NDTThicknessApp().run()
