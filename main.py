import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox, QComboBox, 
                            QAction, QProgressBar, QMainWindow)
from PyQt5.QtGui import QFont, QMovie, QPixmap
from PyQt5.QtCore import Qt, QTimer, QSettings, QDateTime, pyqtSignal

class EnhancedWaitingWindow(QWidget):
    connection_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Conectando ao Sistema GTT/RN')
        self.setFixedSize(500, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setup_ui()
        self.simular_conexao()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        # Logo do sistema
        lbl_logo = QLabel()
        lbl_logo.setPixmap(QPixmap("logo-grau.png").scaled(100, 100, Qt.KeepAspectRatio))
        lbl_logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_logo)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #007BFF;
                border-radius: 10px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #007BFF;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Etapas de conexão
        self.lbl_etapa = QLabel('Iniciando processo de conexão...')
        self.lbl_etapa.setAlignment(Qt.AlignCenter)
        self.lbl_etapa.setStyleSheet('font-size: 14px; color: #333333;')
        layout.addWidget(self.lbl_etapa)

        # Detalhes técnicos
        self.lbl_detalhes = QLabel()
        self.lbl_detalhes.setAlignment(Qt.AlignCenter)
        self.lbl_detalhes.setStyleSheet('font-size: 12px; color: #666666;')
        layout.addWidget(self.lbl_detalhes)

        self.setLayout(layout)

    def simular_conexao(self):
        self.etapas = [
            ('Validando credenciais...', 'Perfil: Supervisor'),
            ('Conectando ao servidor principal...', 'Servidor: w19.rn.gov.br:5432'),
            ('Estabelecendo conexão segura...', 'Protocolo: TLS 1.3 | Cifra: AES-256'),
            ('Sincronizando dados iniciais...', 'Banco: SQLite | Tabelas: 12'),
            ('Carregando módulos do sistema...', 'Módulos: Frota, Rotas, GPS, Relatórios'),
            ('Verificando atualizações...', 'Versão atual: 1.0 | Última versão: 1.0'),
            ('Inicializando interface...', 'Carregamento completo')
        ]
        
        self.etapa_atual = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_conexao)
        self.timer.start(700)

    def atualizar_conexao(self):
        if self.etapa_atual < len(self.etapas):
            etapa, detalhes = self.etapas[self.etapa_atual]
            progresso = int((self.etapa_atual + 1) * (100 / len(self.etapas)))
            
            self.lbl_etapa.setText(etapa)
            self.lbl_detalhes.setText(detalhes)
            self.progress_bar.setValue(progresso)
            
            self.etapa_atual += 1
        else:
            self.timer.stop()
            self.connection_finished.emit()
            self.close()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GTT/RN v1')
        self.resize(1024, 600)
        self.setup_ui()
        self.setup_status_db()

    def setup_status_db(self):
        status_bar = self.statusBar()
        
        # Informações do banco de dados
        status_bar.addPermanentWidget(QLabel(f" Banco de dados: SQLite  "))
        status_bar.addPermanentWidget(QLabel(f" Servidor: w19.gtt.rn.gov.br  "))
        status_bar.addPermanentWidget(QLabel(f" Última sincronização: {QDateTime.currentDateTime().toString('hh:mm:ss')} "))
        status_bar.addPermanentWidget(QLabel(f" Usuário:  "))  # Espaço extra
        status_bar.addPermanentWidget(QLabel(f" Permissões:  "))
        
        # Ícone de status
        self.lbl_status_db = QLabel()
        self.lbl_status_db.setPixmap(QPixmap("connected_icon.png").scaled(20, 20))
        status_bar.addPermanentWidget(self.lbl_status_db)

    def setup_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Gerenciamento')
        edit_menu = menubar.addMenu('Editar')

        new_action = QAction('Novo', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.novo_arquivo)
        file_menu.addAction(new_action)

        open_action = QAction('Abrir', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.abrir_arquivo)
        file_menu.addAction(open_action)

        copy_action = QAction('Copiar', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copiar_texto)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Colar', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.colar_texto)
        edit_menu.addAction(paste_action)

        layout = QVBoxLayout()
        lbl_welcome = QLabel('Sistema GTT/RN')
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
        QMessageBox.information(self, 'Recuperar Senha', f'Instruções enviadas para {email}')

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(420, 660)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.tentativas_restantes = 3
        self.tempo_bloqueio = 30
        self.bloqueios_consecutivos = 0
        self.settings = QSettings('MinhaEmpresa', 'MeuApp')
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        lbl_titulo = QLabel('GTT/RN - Gestão de Transportes e Tráfego')
        lbl_titulo.setFont(QFont('Arial', 16, QFont.Bold))
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        lbl_usuario = QLabel('Usuário:')
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText('Digite seu usuário')
        layout.addWidget(lbl_usuario)
        layout.addWidget(self.txt_usuario)

        lbl_senha = QLabel('Senha:')
        self.txt_senha = QLineEdit()
        self.txt_senha.setPlaceholderText('Digite sua senha')
        self.txt_senha.setEchoMode(QLineEdit.Password)
        layout.addWidget(lbl_senha)
        layout.addWidget(self.txt_senha)

        self.chk_lembrar_usuario = QCheckBox('Lembrar Usuário')
        layout.addWidget(self.chk_lembrar_usuario)

        self.chk_lembrar_senha = QCheckBox('Lembrar Senha')
        layout.addWidget(self.chk_lembrar_senha)

        lbl_empresa = QLabel('Selecione a Empresa:')
        self.cmb_empresa = QComboBox()
        self.cmb_empresa.addItems(['Departamento de Transportes', 'Transportes Guanabara', 
                                  'Transflor (ViaSul)', 'Trans.NACIONAL', 'Santa Maria', 
                                  'Transportes NSC', 'Caravela Potiguar Transportes'])
        layout.addWidget(lbl_empresa)
        layout.addWidget(self.cmb_empresa)

        self.btn_login = QPushButton('Entrar')
        self.btn_login.clicked.connect(self.verificar_login)
        self.btn_login.setFixedHeight(52)
        layout.addWidget(self.btn_login)

        lower_btn_layout = QHBoxLayout()
        self.btn_fechar = QPushButton('Fechar')
        self.btn_fechar.clicked.connect(self.fechar_sistema)
        self.btn_fechar.setFixedHeight(40)
        lower_btn_layout.addWidget(self.btn_fechar)

        self.btn_esqueceu_senha = QPushButton('Esqueceu sua senha?')
        self.btn_esqueceu_senha.setStyleSheet('background: none; border: none; color: blue; text-decoration: underline;')
        self.btn_esqueceu_senha.clicked.connect(self.abrir_tela_recuperar_senha)
        self.btn_esqueceu_senha.setFixedHeight(40)
        lower_btn_layout.addWidget(self.btn_esqueceu_senha)

        layout.addLayout(lower_btn_layout)

        self.lbl_contador = QLabel()
        self.lbl_contador.setAlignment(Qt.AlignCenter)
        self.lbl_contador.setStyleSheet('color: red; font-weight: bold;')
        self.lbl_contador.hide()
        layout.addWidget(self.lbl_contador)

        self.loading_label = QLabel(self)
        self.loading_movie = QMovie("loading.gif")
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)

        self.setLayout(layout)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F5F5F5; }
            QLabel { color: #333333; font-size: 12px; }
            QLineEdit {
                padding: 8px; border: 1px solid #CCCCCC;
                border-radius: 4px; font-size: 14px;
            }
            QPushButton {
                background-color: #007BFF; color: white;
                border: none; border-radius: 4px;
                padding: 8px; font-size: 14px;
            }
            QPushButton:hover { background-color: #0069D9; }
            QPushButton:disabled { background-color: #CCCCCC; }
        """)

    def verificar_login(self):
        usuario = self.txt_usuario.text()
        senha = self.txt_senha.text()

        if not usuario or not senha:
            QMessageBox.warning(self, 'Erro', 'Campos obrigatórios!')
            return

        if usuario == "wesly" and senha == "admin":
            self.bloqueios_consecutivos = 0
            self.salvar_dados()
            self.mostrar_tela_espera()
        else:
            self.tentativas_restantes -= 1
            if self.tentativas_restantes <= 0:
                self.bloquear_sistema()
            else:
                QMessageBox.warning(self, 'Erro', f'Tentativas restantes: {self.tentativas_restantes}')

    def mostrar_tela_espera(self):
        if hasattr(self, 'waiting_window'):
            self.waiting_window.close()
            
        self.waiting_window = EnhancedWaitingWindow()
        self.waiting_window.connection_finished.connect(self.transicao_para_main_app)
        self.waiting_window.show()
        self.close()

    def transicao_para_main_app(self):
        if hasattr(self, 'waiting_window'):
            self.waiting_window.close()
            
        self.main_app = MainApp()
        self.main_app.show()

    def bloquear_sistema(self):
        self.txt_usuario.setEnabled(False)
        self.txt_senha.setEnabled(False)
        self.btn_login.setEnabled(False)
        self.bloqueios_consecutivos += 1
        self.tempo_bloqueio = 30 * (2 ** (self.bloqueios_consecutivos - 1))

        self.lbl_contador.show()
        self.loading_label.show()
        self.loading_movie.start()

        self.tempo_restante = self.tempo_bloqueio
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_contador)
        self.timer.start(1000)
        self.atualizar_contador()

    def atualizar_contador(self):
        if self.tempo_restante > 0:
            self.lbl_contador.setText(f"Tente novamente em {self.tempo_restante}s...")
            self.tempo_restante -= 1
        else:
            self.timer.stop()
            self.txt_usuario.setEnabled(True)
            self.txt_senha.setEnabled(True)
            self.btn_login.setEnabled(True)
            self.lbl_contador.hide()
            self.loading_label.hide()
            self.loading_movie.stop()
            self.tentativas_restantes = 3

    def salvar_dados(self):
        self.settings.setValue('usuario', self.txt_usuario.text() if self.chk_lembrar_usuario.isChecked() else '')
        self.settings.setValue('senha', self.txt_senha.text() if self.chk_lembrar_senha.isChecked() else '')

    def carregar_dados(self):
        self.txt_usuario.setText(self.settings.value('usuario', ''))
        self.txt_senha.setText(self.settings.value('senha', ''))
        self.chk_lembrar_usuario.setChecked(bool(self.settings.value('usuario')))
        self.chk_lembrar_senha.setChecked(bool(self.settings.value('senha')))

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