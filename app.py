import os
import json
import fitz  # PyMuPDF for PDF handling
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle

import ollama  # Assuming you have an AI model handler

class ChatBubble(Label):
    def __init__(self, message, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.text = message
        self.size_hint_y = None
        self.bind(width=lambda *x: self.setter('text_size')(self, (self.width, None)))
        self.bind(texture_size=self.setter('size'))
        self.padding = [15, 10]

        background_color = get_color_from_hex('#ddc6f8') if is_user else get_color_from_hex('#E5E5EA')
        text_color = get_color_from_hex('#000000') if is_user else get_color_from_hex('#333333')

        self.background_color = background_color
        self.color = text_color

        with self.canvas.before:
            Color(*background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[18])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ChatApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#FFFFFF')
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.chat_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.scroll_view.add_widget(self.chat_layout)

        self.input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        self.message_input = TextInput(hint_text='Type a message...', multiline=False, size_hint_x=0.8)
        self.send_button = Button(text='Send Message', size_hint_x=0.2, on_press=self.send_message)

        self.input_layout.add_widget(self.message_input)
        self.input_layout.add_widget(self.send_button)

        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.input_layout)

        self.load_and_send_files()  # Automatically load and send files on app start

        return self.layout

    def load_and_send_files(self):
        folder_path = r'C:\Users\Osmany\OneDrive\Desktop\hub\Offline-Chat\Folder'
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith('.pdf'):
                try:
                    text = self.extract_text_from_pdf(file_path)
                    # Example: Assuming text is JSON data format
                    data = json.loads(text)

                    # Send data to AI (replace with your AI interaction logic)
                    response = ollama.chat(model='dolphin-llama3', messages=data)

                    # Process AI response
                    ai_message = response['message']['content']
                    self.add_message(ai_message, is_user=False)

                except Exception as e:
                    self.add_message(f'Error loading or sending file {filename}: {str(e)}', is_user=False)

        self.scroll_to_bottom()

    def extract_text_from_pdf(self, file_path):
        text = ''
        with fitz.open(file_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()

        return text

    def send_message(self, instance):
        user_message = self.message_input.text.strip()
        if user_message:
            self.add_message(user_message, is_user=True)
            self.message_input.text = ''

            try:
                # Example: Send user message to AI
                response = ollama.chat(model='dolphin-llama3', messages=[{'role': 'user', 'content': user_message}])
                ai_message = response['message']['content']
                self.add_message(ai_message, is_user=False)

            except Exception as e:
                self.add_message(f'Error: {str(e)}', is_user=False)

        self.scroll_to_bottom()

    def add_message(self, message, is_user=True):
        bubble = ChatBubble(message, is_user=is_user)
        self.chat_layout.add_widget(bubble)

    def scroll_to_bottom(self):
        self.scroll_view.scroll_y = 0

if __name__ == '__main__':
    ChatApp().run()
