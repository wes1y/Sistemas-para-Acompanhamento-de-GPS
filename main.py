import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox, QComboBox, 
                            QAction, QProgressBar, QMainWindow, QTableWidget, QTableWidgetItem, 
                            QDialog, QFormLayout, QDialogButtonBox)
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
            ('Sincronizando dados...', 'Banco: SQLite | Tabelas: 12'),
            ('Carregando módulos do sistema...', 'Alterações de módulos...'),
            ('Verificando atualizações...', 'Versão atual: 1.0'),
            ('Sistema atualizado!', 'Versão: 1.0'),
        ]
        
        self.etapa_atual = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_conexao)
        self.timer.start(900)

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

class VehicleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Cadastrar Novo Veículo')
        self.setFixedSize(400, 300)
        
        layout = QFormLayout()
        
        self.txt_placa = QLineEdit()
        self.txt_placa.setPlaceholderText('Ex: ABC1D23')
        layout.addRow('Placa:', self.txt_placa)
        
        self.txt_modelo = QLineEdit()
        self.txt_modelo.setPlaceholderText('Ex: Ford Ranger 2023')
        layout.addRow('Modelo:', self.txt_modelo)
        
        self.cb_tipo = QComboBox()
        self.cb_tipo.addItems(['Ônibus'])
        layout.addRow('Tipo:', self.cb_tipo)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GTT/RN v1')
        self.resize(1024, 600)
        self.veiculos = []
        self.setup_ui()
        self.setup_status_db()
        self.add_example_vehicles()

    def setup_status_db(self):
        status_bar = self.statusBar()
        status_bar.addPermanentWidget(QLabel(f" Banco de dados: SQLite  "))
        status_bar.addPermanentWidget(QLabel(f" Servidor: w19.gtt.rn.gov.br  "))
        status_bar.addPermanentWidget(QLabel(f" Última sincronização: {QDateTime.currentDateTime().toString('hh:mm:ss')} "))
        status_bar.addPermanentWidget(QLabel(f" Usuário:  wesly "))
        status_bar.addPermanentWidget(QLabel(f" Permissões:  Supervisor "))

    def setup_ui(self):
        menubar = self.menuBar()
        
        # Menu Gerenciamento
        file_menu = menubar.addMenu('Gerenciamento')
        new_action = QAction('Novo', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.novo_arquivo)
        file_menu.addAction(new_action)

        # Menu Cadastros
        cadastro_menu = menubar.addMenu('Cadastros')
        veiculo_action = QAction('Veículos', self)
        veiculo_action.triggered.connect(self.show_vehicle_registration)
        cadastro_menu.addAction(veiculo_action)

        # Layout principal
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Tabela de veículos
        self.table_veiculos = QTableWidget()
        self.table_veiculos.setColumnCount(5)
        self.table_veiculos.setHorizontalHeaderLabels(['ID', 'Placa', 'Modelo', 'Tipo', 'Status'])
        self.table_veiculos.setColumnWidth(0, 50)
        self.table_veiculos.setColumnWidth(1, 100)
        self.table_veiculos.setColumnWidth(4, 100)
        
        # Botão de novo veículo
        btn_novo = QPushButton('Novo Veículo')
        btn_novo.setStyleSheet('background-color: #4CAF50; color: white;')
        btn_novo.clicked.connect(self.show_vehicle_registration)

        layout.addWidget(QLabel('Frota de Veículos Cadastrados:', self))
        layout.addWidget(self.table_veiculos)
        layout.addWidget(btn_novo)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def novo_arquivo(self):
        QMessageBox.information(self, 'Novo Arquivo', 'Ação Novo Arquivo selecionada.')

    def add_example_vehicles(self):
        self.veiculos = [
            {'id': 1, 'placa': 'RNB4A21', 'modelo': 'Volvo FH 540', 'tipo': 'Caminhão', 'status': 'Ativo'},
            {'id': 2, 'placa': 'RNM5C89', 'modelo': 'Mercedes-Benz OF-1721', 'tipo': 'Ônibus', 'status': 'Em Manutenção'},
            {'id': 3, 'placa': 'RNE3F45', 'modelo': 'Honda CG 160 Titan', 'tipo': 'Moto', 'status': 'Ativo'}
        ]
        self.update_table()

    def update_table(self):
        self.table_veiculos.setRowCount(len(self.veiculos))
        for row, veiculo in enumerate(self.veiculos):
            self.table_veiculos.setItem(row, 0, QTableWidgetItem(str(veiculo['id'])))
            self.table_veiculos.setItem(row, 1, QTableWidgetItem(veiculo['placa']))
            self.table_veiculos.setItem(row, 2, QTableWidgetItem(veiculo['modelo']))
            self.table_veiculos.setItem(row, 3, QTableWidgetItem(veiculo['tipo']))
            self.table_veiculos.setItem(row, 4, QTableWidgetItem(veiculo['status']))

    def show_vehicle_registration(self):
        dialog = VehicleDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            novo_veiculo = {
                'id': len(self.veiculos) + 1,
                'placa': dialog.txt_placa.text(),
                'modelo': dialog.txt_modelo.text(),
                'tipo': dialog.cb_tipo.currentText(),
                'status': 'Ativo'
            }
            self.veiculos.append(novo_veiculo)
            self.update_table()
            QMessageBox.information(self, 'Sucesso', 'Veículo cadastrado com sucesso!')

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

class AtualizacaoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Atualizações em andamento')
        self.setFixedSize(300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        lbl_mensagem = QLabel('Aguarde enquanto o sistema é atualizado!')
        lbl_mensagem.setStyleSheet('font-size: 10px; color: #333333;')
        lbl_mensagem.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_mensagem)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def iniciar_progresso(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_progresso)
        self.timer.start(15)

    def atualizar_progresso(self):
        valor_atual = self.progress_bar.value()
        if valor_atual < 100:
            self.progress_bar.setValue(valor_atual + 1)
        else:
            self.timer.stop()
            QApplication.instance().quit()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(420, 520)
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

        self.btn_login = QPushButton('Entrar')
        self.btn_login.clicked.connect(self.verificar_login)
        self.btn_login.setFixedHeight(52)
        self.btn_login.setStyleSheet('background-color: #28a745; color: white; border-radius: 0px;')  # Verde sem bordas arredondadas
        layout.addWidget(self.btn_login)

        lower_btn_layout = QHBoxLayout()
        self.btn_fechar = QPushButton('Fechar')
        self.btn_fechar.clicked.connect(self.fechar_sistema)
        self.btn_fechar.setFixedHeight(40)
        self.btn_fechar.setStyleSheet('background-color: #dc3545; color: white; border-radius: 0px;')  # Vermelho sem bordas arredondadas
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
                border: none; padding: 8px; font-size: 14px;
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
        self.hide()

    def transicao_para_main_app(self):
        if hasattr(self, 'waiting_window'):
            self.waiting_window.close()
            
        self.main_app = MainApp()
        self.main_app.show()
        self.close()

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
        reply = QMessageBox.question(self, 'Confirmação', 'Você realmente deseja fechar o sistema?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.mostrar_tela_atualizacao()

    def mostrar_tela_atualizacao(self):
        self.atualizacao_window = AtualizacaoWindow()
        self.atualizacao_window.show()
        self.atualizacao_window.iniciar_progresso()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = LoginWindow()
    janela.show()
    sys.exit(app.exec_())