from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import detector
from PyQt5.QtGui import QIcon
import time
class MyMainGUI(QDialog):

    question_cnt = 0

    def __init__(self, parent=None):
        super().__init__(parent)

        self.detect_on=QPixmap('public/detect_on.png')
        self.detect_off=QPixmap('public/detect_off.png')
        # 이모티콘
        self.neutral=QPixmap('public/neutral.png').scaledToWidth(200)
        self.question=QPixmap('public/question.png').scaledToWidth(200)
        self.doubt = QPixmap('public/doubt.png').scaledToWidth(200)
        self.tired=QPixmap('public/sleep.png').scaledToWidth(200)
        self.left=QPixmap('public/left.png').scaledToWidth(200)
        self.yes=QPixmap('public/yes.png').scaledToWidth(200)
        self.no=QPixmap('public/no.png').scaledToWidth(200)

        # 얼굴인식 여부
        self.detectDot = QLabel()
        self.detectDot.resize(10,10)
        self.detectDot.setPixmap(self.detect_off)
        self.detectText = QLabel('인식안됨', self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.detectDot)
        hbox.addWidget(self.detectText)

        # 사용자 이모티콘
        self.userEmoticon = QLabel()
        self.userEmoticon.setPixmap(self.neutral)

        # 질문 버튼
        self.questionBtn = QPushButton(self)
        self.questionBtn.setIcon(QIcon('public/question.png'))

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.userEmoticon)
        vbox.addWidget(self.questionBtn)
        self.setLayout(vbox)
        self.setGeometry(100, 50, 200, 300)

class Test:
    def __init__(self):
        name = ""


class MyMain(MyMainGUI):
    add_sec_signal = pyqtSignal()
    send_instance_singal = pyqtSignal("PyQt_PyObject")

    def __init__(self, parent=None):
        super().__init__(parent)

        self.questionBtn.clicked.connect(self.btn_clicked)

        # video 스레드
        self.th = Worker(parent=self)
        self.th.detect_changed.connect(self.detect_update)  # custom signal from worker thread to main thread
        self.th.state_changed.connect(self.state_update)  # custom signal from worker thread to main thread
        self.th.start()
        self.th.working = True
        
        self.show()

    # 질문 버튼
    def btn_clicked(self):
        self.question_cnt = 30
        self.userEmoticon.setPixmap(self.question)

    @pyqtSlot(str)
    def detect_update(self, msg):
        # 검출 안됨
        if msg == "0":
            self.detectDot.setPixmap(self.detect_off)
            self.detectText.setText("인식 안됨")
        elif msg == "1":
            self.detectDot.setPixmap(self.detect_on)
            self.detectText.setText("인식 중")

    @pyqtSlot(str)
    def state_update(self, msg):
        self.question_cnt -= 1
        if self.question_cnt > 0:
            return

        if msg == "1":
            self.userEmoticon.setPixmap(self.neutral)
        elif msg == "2":
            self.userEmoticon.setPixmap(self.doubt)
        elif msg == "3":
            self.userEmoticon.setPixmap(self.tired)
        elif msg == "4":
            self.userEmoticon.setPixmap(self.left)
        elif msg == "5":
            self.userEmoticon.setPixmap(self.yes)
        elif msg == "6":
            self.userEmoticon.setPixmap(self.no)



class Worker(QThread):
    detect_changed = pyqtSignal(str)
    state_changed = pyqtSignal(str)

    def __init__(self, detect = 0,state=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True
        self.detect = detect
        self.state = state

        # self.main.add_sec_signal.connect(self.add_sec)   # 이것도 작동함. # custom signal from main thread to worker thread

    def __del__(self):
        print(".... end thread.....")
        self.wait()

    def run(self):
        md = detector.MyDetector()
        md.video(self.detect, self.detect_changed, self.state, self.state_changed)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()