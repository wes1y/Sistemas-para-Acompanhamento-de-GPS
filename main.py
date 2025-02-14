import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox, QComboBox, QAction)
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtWidgets import QStackedWidget, QMainWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GTT/RN v1')
        self.resize(1024, 600)  # Define um tamanho inicial, mas permite redimensionamento
        self.setup_ui()

    def setup_ui(self):
        # Criação da barra de menu
        menubar = self.menuBar()

        # Adicionando menus
        file_menu = menubar.addMenu('Gerenciamento')
        edit_menu = menubar.addMenu('Editar')

        # Adicionando ações ao menu Gerenciamento
        new_action = QAction('Novo', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.novo_arquivo)
        file_menu.addAction(new_action)

        open_action = QAction('Abrir', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.abrir_arquivo)
        file_menu.addAction(open_action)

        # Adicionando ações ao menu Editar
        copy_action = QAction('Copiar', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copiar_texto)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Colar', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.colar_texto)
        edit_menu.addAction(paste_action)

        layout = QVBoxLayout()
        lbl_welcome = QLabel('teste')
        lbl_welcome.setFont(QFont('Arial', 16, QFont.Bold))
        lbl_welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_welcome)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def novo_arquivo(self):
        QMessageBox.information(self, 'Novo Arquivo', 'Ação Novo Arquivo selecionada.')

    def abrir_arquivo(self):
        QMessageBox.information(self, 'Abrir Arquivo', 'Ação Abrir Arquivo selecionada.')

    def copiar_texto(self):
        QMessageBox.information(self, 'Copiar', 'Ação Copiar selecionada.')

    def colar_texto(self):
        QMessageBox.information(self, 'Colar', 'Ação Colar selecionada.')

class ForgotPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Recuperar Senha')
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        lbl_titulo = QLabel('Recuperar Senha')
        lbl_titulo.setFont(QFont('Arial', 16, QFont.Bold))
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        lbl_email = QLabel('Email:')
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText('Digite seu email')
        layout.addWidget(lbl_email)
        layout.addWidget(self.txt_email)

        btn_recuperar = QPushButton('Recuperar Senha')
        btn_recuperar.clicked.connect(self.recuperar_senha)
        layout.addWidget(btn_recuperar)

        self.setLayout(layout)

    def recuperar_senha(self):
        email = self.txt_email.text()
        QMessageBox.information(self, 'Recuperar Senha', f'Instruções de recuperação de senha enviadas para {email}')

class WaitingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Realizando conexão...')
        self.setFixedSize(420, 220)  # Tamanho fixo da janela
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        lbl_message = QLabel('Realizando conexão com banco de dados...')
        lbl_message.setFont(QFont('Arial', 10))  # Diminuir o tamanho da fonte
        lbl_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_message)

        self.setLayout(layout)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(420, 660)  # Tamanho fixo da janela
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove os botões padrão do Windows
        self.tentativas_restantes = 3
        self.tempo_bloqueio = 30  # Tempo inicial de bloqueio em segundos
        self.bloqueios_consecutivos = 0  # Contador de bloqueios consecutivos
        self.settings = QSettings('MinhaEmpresa', 'MeuApp')
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        # Título
        lbl_titulo = QLabel('GTT/RN - Gestão de Transportes e Tráfego')
        lbl_titulo.setFont(QFont('Arial', 16, QFont.Bold))
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        # Campo de usuário
        lbl_usuario = QLabel('Usuário:')
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText('Digite seu usuário')
        layout.addWidget(lbl_usuario)
        layout.addWidget(self.txt_usuario)

        # Campo de senha
        lbl_senha = QLabel('Senha:')
        self.txt_senha = QLineEdit()
        self.txt_senha.setPlaceholderText('Digite sua senha')
        self.txt_senha.setEchoMode(QLineEdit.Password)
        layout.addWidget(lbl_senha)
        layout.addWidget(self.txt_senha)

        # Checkbox lembrar usuário
        self.chk_lembrar_usuario = QCheckBox('Lembrar Usuário')
        layout.addWidget(self.chk_lembrar_usuario)

        # Checkbox lembrar senha
        self.chk_lembrar_senha = QCheckBox('Lembrar Senha')
        layout.addWidget(self.chk_lembrar_senha)

        # ComboBox selecionar empresa
        lbl_empresa = QLabel('Selecione a Empresa:')
        self.cmb_empresa = QComboBox()
        self.cmb_empresa.addItems(['Departamento de Transportes', 'Transportes Guanabara', 'Transflor (ViaSul)', 'Trans.NACIONAL', 'Santa Maria', 'Transportes NSC', 'Caravela Potiguar Transportes'])
        layout.addWidget(lbl_empresa)
        layout.addWidget(self.cmb_empresa)

        # Botão de login
        self.btn_login = QPushButton('Entrar')
        self.btn_login.clicked.connect(self.verificar_login)
        self.btn_login.setFixedHeight(52)  # Altura de um botão e meio
        layout.addWidget(self.btn_login)

        # Layout para botões de fechar e esqueceu senha
        lower_btn_layout = QHBoxLayout()

        # Botão de fechar
        self.btn_fechar = QPushButton('Fechar')
        self.btn_fechar.clicked.connect(self.fechar_sistema)
        self.btn_fechar.setFixedHeight(40)  # Metade da altura do botão de login
        lower_btn_layout.addWidget(self.btn_fechar)

        # Botão de esqueceu sua senha
        self.btn_esqueceu_senha = QPushButton('Esqueceu sua senha?')
        self.btn_esqueceu_senha.setStyleSheet('background: none; border: none; color: blue; text-decoration: underline;')
        self.btn_esqueceu_senha.clicked.connect(self.abrir_tela_recuperar_senha)
        self.btn_esqueceu_senha.setFixedHeight(40)  # Metade da altura do botão de login
        lower_btn_layout.addWidget(self.btn_esqueceu_senha)

        layout.addLayout(lower_btn_layout)

        # Label para contador de bloqueio
        self.lbl_contador = QLabel()
        self.lbl_contador.setAlignment(Qt.AlignCenter)
        self.lbl_contador.setStyleSheet('color: red; font-weight: bold;')
        self.lbl_contador.hide()  # Esconde o contador inicialmente
        layout.addWidget(self.lbl_contador)

        # Ícone de carregamento
        self.loading_label = QLabel(self)
        self.loading_movie = QMovie("loading.gif")  # Substitua pelo caminho do seu GIF
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.hide()  # Esconde o ícone inicialmente
        layout.addWidget(self.loading_label)

        self.setLayout(layout)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
            }
            QLabel {
                color: #333333;
                font-size: 12px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0069D9;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
        """)

    def verificar_login(self):
        usuario = self.txt_usuario.text()
        senha = self.txt_senha.text()

        if not usuario or not senha:
            QMessageBox.warning(self, 'Erro', 'Os campos Usuário e Senha são obrigatórios!')
            return

        if usuario == "admin" and senha == "admin":
            self.bloqueios_consecutivos = 0  # Resetar bloqueios consecutivos após login bem-sucedido
            self.salvar_dados()
            self.mostrar_tela_espera()
        else:
            self.tentativas_restantes -= 1
            
            if self.tentativas_restantes <= 0:  # Bloquear após 3 tentativas
                self.bloquear_sistema()
            else:
                QMessageBox.warning(self, 'Erro', 
                    f'Usuário ou senha inválidas! Tentativas restantes: {self.tentativas_restantes}')

    def mostrar_tela_espera(self):
        self.waiting_window = WaitingWindow()
        self.waiting_window.show()
        self.close()

        QTimer.singleShot(2000, self.transicao_para_main_app)  # Espera 2 segundos antes de transitar para a MainApp

    def transicao_para_main_app(self):
        self.waiting_window.close()
        self.main_app = MainApp()
        self.main_app.show()

    def bloquear_sistema(self):
        # Desabilitar campos e botão
        self.txt_usuario.setEnabled(False)
        self.txt_senha.setEnabled(False)
        self.btn_login.setEnabled(False)

        # Aumentar tempo de bloqueio progressivamente
        self.bloqueios_consecutivos += 1
        self.tempo_bloqueio = 30 * (2 ** (self.bloqueios_consecutivos - 1))  # 30, 60, 120, 240, ...

        # Mostrar contador e ícone de carregamento
        self.lbl_contador.show()
        self.loading_label.show()
        self.loading_movie.start()

        # Iniciar temporizador
        self.tempo_restante = self.tempo_bloqueio
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_contador)
        self.timer.start(1000)  # Atualizar a cada 1 segundo

        # Atualizar contador imediatamente
        self.atualizar_contador()

    def atualizar_contador(self):
        if self.tempo_restante > 0:
            self.lbl_contador.setText(f"Tente novamente em {self.tempo_restante} segundos...")
            self.tempo_restante -= 1
        else:
            # Reativar sistema
            self.timer.stop()
            self.txt_usuario.setEnabled(True)
            self.txt_senha.setEnabled(True)
            self.btn_login.setEnabled(True)
            self.lbl_contador.hide()
            self.loading_label.hide()
            self.loading_movie.stop()
            self.tentativas_restantes = 3  # Resetar tentativas

    def salvar_dados(self):
        if self.chk_lembrar_usuario.isChecked():
            self.settings.setValue('usuario', self.txt_usuario.text())
        else:
            self.settings.remove('usuario')

        if self.chk_lembrar_senha.isChecked():
            self.settings.setValue('senha', self.txt_senha.text())
        else:
            self.settings.remove('senha')

    def carregar_dados(self):
        usuario = self.settings.value('usuario', '')
        senha = self.settings.value('senha', '')

        self.txt_usuario.setText(usuario)
        self.txt_senha.setText(senha)

        self.chk_lembrar_usuario.setChecked(bool(usuario))
        self.chk_lembrar_senha.setChecked(bool(senha))

    def abrir_tela_recuperar_senha(self):
        self.forgot_password_window = ForgotPasswordWindow()
        self.forgot_password_window.show()

    def fechar_sistema(self):
        QApplication.instance().quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = LoginWindow()
    janela.show()
    sys.exit(app.exec_())
