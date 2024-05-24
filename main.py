import os
import datetime
import subprocess
import cv2
import numpy as np
import self as self
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from fer import FER

class FaceRecognitionApp(App):
    def build(self):
        # Diretório para armazenar imagens dos usuários
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        # Caminho para o arquivo de log
        self.log_path = './log.txt'

        # Inicializa o modo escuro como False
        self.dark_mode = False

        # Cria o layout principal
        self.main_layout = BoxLayout(orientation='vertical')

        # Barra superior para o botão de alternância do modo escuro
        self.top_bar = BoxLayout(size_hint_y=None, height=50)
        self.toggle_button = ToggleButton(text='Dark Mode', on_press=self.toggle_mode)
        self.top_bar.add_widget(self.toggle_button)
        self.main_layout.add_widget(self.top_bar)

        # Parte do meio com câmera e layout do log
        self.middle_layout = BoxLayout(orientation='horizontal', size_hint_y=2)

        # Layout da câmera
        self.camera_layout = BoxLayout(orientation='vertical')
        self.camera_output = Image()
        self.camera_layout.add_widget(self.camera_output)

        self.middle_layout.add_widget(self.camera_layout)

        # Layout do log
        self.log_layout = GridLayout(cols=2, size_hint=(0.5, 0.6))
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        self.middle_layout.add_widget(self.log_layout)
        self.main_layout.add_widget(self.middle_layout)

        # Parte inferior com botões de login e registro
        self.bottom_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        self.login_button = Button(text='Login', on_press=self.login, size_hint_y=None, height=50)
        self.bottom_layout.add_widget(self.login_button)

        self.register_button = Button(text='Register New User', on_press=self.register_new_user, size_hint_y=None, height=50)
        self.bottom_layout.add_widget(self.register_button)
        self.main_layout.add_widget(self.bottom_layout)

        # Configura a captura de vídeo da câmera
        self.capture = cv2.VideoCapture(0)

        # Inicializa o detector de emoções
        self.emotion_detector = FER(mtcnn=True)
        self.emotion_label = Label(text="", size_hint_y=None, height=30)

        self.camera_layout.add_widget(self.emotion_label)

        # Configura a atualização do frame da webcam
        Clock.schedule_interval(self.update, 1.0/30.0)
        self.update_log()  # Atualiza a grid do log na inicialização
        return self.main_layout

    def update(self, dt):
        # Função chamada periodicamente para atualizar o frame da webcam
        ret, frame = self.capture.read()
        if ret:
            self.processed_frame = frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detecta emoções no frame da câmera
            emotion_results = self.emotion_detector.detect_emotions(rgb_frame)

            # Atualiza a label com a emoção detectada
            if emotion_results:
                top_emotion = max(emotion_results[0]['emotions'], key=emotion_results[0]['emotions'].get)
                self.emotion_label.text = f'Emotion: {top_emotion} - {emotion_results[0]["emotions"][top_emotion]:.2f}'
            else:
                self.emotion_label.text = 'No emotion detected'

            # Detecta faces no frame da câmera usando cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            # Desenha retângulos ao redor das faces detectadas
            for (x, y, w, h) in faces:
                cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Converte o frame para uma textura Kivy e exibe na interface
            buf = cv2.flip(rgb_frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.camera_output.texture = texture

    def toggle_mode(self, instance):
        # Função para alternar entre modos claro e escuro
        if self.dark_mode:
            Window.clearcolor = (1, 1, 1, 1)  # Modo claro
            self.dark_mode = False
            self.change_text_color('black')
        else:
            Window.clearcolor = (0, 0, 0, 1)  # Modo escuro
            self.dark_mode = True
            self.change_text_color('white')

    def change_text_color(self, color):
        # Função para alterar a cor do texto nas labels do log
        for widget in self.log_layout.children:
            if isinstance(widget, Label):
                widget.color = (0, 0, 0, 1) if color == 'black' else (1, 1, 1, 1)

    def login(self, instance):
        # Função para processar o login com reconhecimento facial
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.processed_frame)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]

        if name in ['unknown_person', 'no_persons_found']:
            popup = Popup(title='Ops...', content=Label(text='Unknown user. Please register new user or try again.'), size_hint=(None, None), size=(400, 400))
            popup.open()
        else:
            popup = Popup(title='Welcome back!', content=Label(text=f'Welcome, {name}'), size_hint=(None, None), size=(400, 400))
            popup.open()
            with open(self.log_path, 'a') as f:
                f.write(f'{name},{datetime.datetime.now()}\n')
            os.remove(unknown_img_path)
            self.update_log()  # Atualiza a grid do log após o login

    def register_new_user(self, instance):
        # Função para exibir a janela de registro de novo usuário
        self.new_user_popup = Popup(title='Register New User', size_hint=(None, None), size=(600, 400))

        self.new_user_layout = BoxLayout(orientation='vertical')
        self.new_user_text = TextInput(hint_text='Please, input username:', multiline=False)
        self.new_user_layout.add_widget(self.new_user_text)

        self.accept_button = Button(text='Accept', on_press=self.accept_register_new_user)
        self.new_user_layout.add_widget(self.accept_button)

        self.try_again_button = Button(text='Try Again', on_press=self.try_again_register_new_user)
        self.new_user_layout.add_widget(self.try_again_button)

        self.new_user_popup.content = self.new_user_layout
        self.new_user_popup.open()

    def accept_register_new_user(self, instance):
        # Função para registrar um novo usuário
        name = self.new_user_text.text
        cv2.imwrite(os.path.join(self.db_dir, f'{name}.jpg'), self.processed_frame)
        popup = Popup(title='Success', content=Label(text='User was registered successfully!'), size_hint=(None, None), size=(400, 400))
        popup.open()
        self.new_user_popup.dismiss()

    def try_again_register_new_user(self, instance):
        # Função para fechar a janela de registro
        self.new_user_popup.dismiss()

    def update_log(self):
        # Função para atualizar a grid do log com informações de login
        self.log_layout.clear_widgets()
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as log_file:
                for line in log_file:
                    name, timestamp = line.strip().split(',')
                    name_label = Label(text=name, size_hint_y=None, height=30)
                    timestamp_label = Label(text=timestamp, size_hint_y=None, height=30)
                    if self.dark_mode:
                        name_label.color = (1, 1, 1, 1)
                        timestamp_label.color = (1, 1, 1, 1)
                    else:
                        name_label.color = (0, 0, 0, 1)
                        timestamp_label.color = (0, 0, 0, 1)
                    self.log_layout.add_widget(name_label)
                    self.log_layout.add_widget(timestamp_label)

    def on_stop(self):
        # Libera a captura da câmera ao parar o aplicativo
        self.capture.release()

if __name__ == '__main__':
    FaceRecognitionApp().run()
