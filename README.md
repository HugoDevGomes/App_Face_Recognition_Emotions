# Face Recognition and Emotion Analysis App

Este projeto é uma aplicação de reconhecimento facial e análise de emoções construída com Kivy e OpenCV. Ela detecta emoções no rosto de usuários em tempo real, permite o login com reconhecimento facial e a adição de novos usuários ao banco de dados.

## Funcionalidades

- **Reconhecimento Facial**: Detecta rostos usando um Cascade Classifier.
- **Análise de Emoções**: Analisa as emoções dos rostos detectados utilizando a biblioteca `FER`.
- **Login com Reconhecimento Facial**: Permite o login de usuários registrados com base no reconhecimento facial.
- **Registro de Novos Usuários**: Adiciona novos usuários ao banco de dados com uma foto capturada pela webcam.
- **Modo Claro/Escuro**: Alterna entre modos claro e escuro para melhor conforto visual.
  
![Face Recognition Demo](https://s12.gifyu.com/images/SfRNu.gif)

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada.
- **Kivy**: Biblioteca para construção de interfaces gráficas.
- **OpenCV**: Biblioteca de visão computacional utilizada para captura e processamento de imagens.
- **FER**: Biblioteca para análise de emoções em imagens de rosto.
- **face_recognition**: Utilizada para verificar correspondência entre rostos registrados e o rosto detectado na imagem.

## Estrutura do Projeto

- `FaceRecognitionApp`: Classe principal que contém toda a lógica do aplicativo.
  - `build()`: Configura e retorna o layout principal do aplicativo.
  - `update(dt)`: Atualiza o frame da webcam, processa a detecção de rostos e emoções.
  - `toggle_mode(instance)`: Alterna entre modos claro e escuro.
  - `change_text_color(color)`: Altera a cor do texto no log.
  - `login(instance)`: Processa o login do usuário utilizando reconhecimento facial.
  - `register_new_user(instance)`: Exibe a janela de registro de novo usuário.
  - `accept_register_new_user(instance)`: Registra um novo usuário.
  - `try_again_register_new_user(instance)`: Fecha a janela de registro.
  - `update_log()`: Atualiza a grid do log com informações de login.
  - `on_stop()`: Libera a captura da câmera ao parar o aplicativo.

## Como Executar

1. Clone o repositório:
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/HugoDevGomes/App_Face_Recognition_Emotions)
    cd seu-repositorio
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3. Execute a aplicação:
    ```bash
    python seu_arquivo.py
    ```

## Requisitos

- Python 3.6+
- Kivy
- OpenCV
- FER
- face_recognition

## Contribuição

Sinta-se à vontade para contribuir com o projeto, seja reportando problemas, solicitando novos recursos ou enviando pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para sugestões, dúvidas ou feedback, entre em contato pelo email: [hugodatawise@hotmail.com](mailto:hugodatawise@hotmail.com)
