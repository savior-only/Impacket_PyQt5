import sys
from PyQt5 import QtWidgets
import os
import subprocess

class ImpacketGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Impacket GUI by SXdysq")

        # 创建选项卡控件
        self.tab_control = QtWidgets.QTabWidget(self)

        # 创建Wmiexec选项卡
        self.wmiexec_tab = QtWidgets.QWidget()
        self.tab_control.addTab(self.wmiexec_tab, "Wmiexec")

        # 创建atexec选项卡
        self.atexec_tab = QtWidgets.QWidget()
        self.tab_control.addTab(self.atexec_tab, "Atexec")

        # 创建Psexec选项卡
        self.psexec_tab = QtWidgets.QWidget()
        self.tab_control.addTab(self.psexec_tab, "Psexec")

        # 创建SMBexec选项卡
        self.smbexec_tab = QtWidgets.QWidget()
        self.tab_control.addTab(self.smbexec_tab, "SMBexec")

        # 创建DCOMexec选项卡
        self.dcomexec_tab = QtWidgets.QWidget()
        self.tab_control.addTab(self.dcomexec_tab, "DCOMexec")

        # 创建配置选项卡
        self.config_tab = QtWidgets.QWidget()
        self.tab_control.addTab(self.config_tab, "配置")

        self.setCentralWidget(self.tab_control)

        # 创建布局
        self.create_layout(self.wmiexec_tab)
        self.create_layout(self.atexec_tab)
        self.create_layout(self.psexec_tab)
        self.create_layout(self.smbexec_tab)
        self.create_layout(self.dcomexec_tab)
        self.create_config_layout()

    def create_layout(self, tab_widget):
        layout = QtWidgets.QGridLayout(tab_widget)

        ip_label = QtWidgets.QLabel("IP地址:")
        layout.addWidget(ip_label, 0, 0)
        ip_entry = QtWidgets.QLineEdit()
        layout.addWidget(ip_entry, 0, 1)

        username_label = QtWidgets.QLabel("用户名:")
        layout.addWidget(username_label, 0, 2)
        username_entry = QtWidgets.QLineEdit()
        layout.addWidget(username_entry, 0, 3)

        password_label = QtWidgets.QLabel("pass/hash:")
        layout.addWidget(password_label, 0, 4)
        password_entry = QtWidgets.QLineEdit()
        layout.addWidget(password_entry, 0, 5)

        command_label = QtWidgets.QLabel("命令:")
        layout.addWidget(command_label, 1, 0)
        command_entry = QtWidgets.QLineEdit()
        layout.addWidget(command_entry, 1, 1)

        AuthType_label = QtWidgets.QLabel("认证类型:")
        layout.addWidget(AuthType_label, 1, 2)
        AuthType_combobox = QtWidgets.QComboBox()
        AuthType_combobox.addItems(["pass", "hash"])
        layout.addWidget(AuthType_combobox, 1, 3)

        encoding_label = QtWidgets.QLabel("编码:")
        layout.addWidget(encoding_label, 1, 4)
        encoding_combobox = QtWidgets.QComboBox()
        encoding_combobox.addItems(["gbk", "utf-8"])
        layout.addWidget(encoding_combobox, 1, 5)

        send_button = QtWidgets.QPushButton("ATTACK")
        layout.addWidget(send_button, 2, 0, 1, 6)

        output_text = QtWidgets.QTextEdit()
        layout.addWidget(output_text, 3, 0, 1, 6)

        # 绑定按钮的点击事件到run_command方法
        send_button.clicked.connect(self.run_command)

    def create_config_layout(self):
        layout = QtWidgets.QGridLayout(self.config_tab)
        
        env_label = QtWidgets.QLabel("Python解释器路径:")
        layout.addWidget(env_label, 0, 0)
        env_entry = QtWidgets.QLineEdit("python3")
        layout.addWidget(env_entry, 0 ,1)
        # 将环境变量输入框保存为实例变量
        self.env_entry = env_entry

    def run_command(self):
        current_tab = self.tab_control.currentIndex()

        # 获取当前选项卡的布局和控件
        layout = self.tab_control.widget(current_tab).layout()
        ip_entry = layout.itemAtPosition(0, 1).widget()
        username_entry = layout.itemAtPosition(0, 3).widget()
        password_entry = layout.itemAtPosition(0, 5).widget()
        command_entry = layout.itemAtPosition(1, 1).widget()
        AuthType_combobox = layout.itemAtPosition(1, 3).widget()
        encoding_combobox = layout.itemAtPosition(1, 5).widget()
        output_text = layout.itemAtPosition(3, 0).widget()

        # 获取环境变量输入框的值
        python_path = self.env_entry.text()
        # # 获取当前脚本的目录路径
        # current_dir = os.path.dirname(__file__)
        # print(current_dir)

        ip = ip_entry.text()
        username = username_entry.text()
        password = password_entry.text()
        command = command_entry.text()
        encoding = encoding_combobox.currentText()
        auth_type = AuthType_combobox.currentText()

        if auth_type == "pass":
            auth = f"{username}:{password}"
        else:
            auth = username

        if current_tab == 0:  # Wmiexec选项卡
            script_path = os.path.join("impacket-0.11.0/examples", "wmiexec.py")
            if auth_type == "pass":
                command = f"{python_path} {script_path} {auth}@{ip} '{command}' -codec {encoding}"
            else:
                command = f"{python_path} {script_path} {auth}@{ip} '{command}' -hashes :{password} -codec {encoding}"
        if current_tab == 1:  # Atexec选项卡
            script_path = os.path.join("impacket-0.11.0/examples", "atexec.py")
            if auth_type == "pass":
                command = f"{python_path} {script_path} {auth}@{ip} '{command}' -codec {encoding}"
            else:
                command = f"{python_path} {script_path} {auth}@{ip} '{command}' -hashes :{password} -codec {encoding}"
        elif current_tab == 2:  # Psexec选项卡
            script_path = os.path.join("impacket-0.11.0/examples", "psexec.py")
            if auth_type == "pass":
                command = f"{python_path} {script_path} {auth}@{ip} '{command}' -codec {encoding}"
            else:
                command = f"{python_path} {script_path} {auth}@{ip} '{command}' -hashes :{password} -codec {encoding}"
        elif current_tab == 3:  # SMBexec选项卡
            script_path = os.path.join("impacket-0.11.0/examples", "smbexec.py")
            if auth_type == "pass":
                command = f"{python_path} {script_path} {auth}@{ip} '{command}' -codec {encoding}"
            else:
                command = f"{python_path} {script_path} {auth}@{ip} '{command}' -hashes :{password} -codec {encoding}"
        elif current_tab == 4:  # DCOMexec选项卡
            script_path = os.path.join("impacket-0.11.0/examples", "dcomexec.py")
            if auth_type == "pass":
                command = f"{python_path} {script_path} -object MMC20 {auth}@{ip} '{command}' -codec {encoding}"
            else:
                command = f"{python_path} {script_path} -object MMC20 {auth}@{ip} '{command}' -hashes :{password} -codec {encoding}"

        try:
            output = subprocess.check_output(command, shell=True)
            output_text.clear()
            output_text.append(output.decode())
        except subprocess.CalledProcessError as e:
            error_message = f"Command execution failed with return code {e.returncode}:\n{e.output.decode()}"
            QtWidgets.QMessageBox.critical(self, "Error", error_message)


app = QtWidgets.QApplication(sys.argv)
window = ImpacketGUI()
window.show()
sys.exit(app.exec_())
