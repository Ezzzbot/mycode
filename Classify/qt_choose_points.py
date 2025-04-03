import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ImageViewer(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer with Point Selection")

        # 保存原始图像路径
        self.image_path = image_path

        # 创建主部件和布局
        main_widget = QWidget()
        layout = QVBoxLayout()

        # 创建 QLabel 来显示图像
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.image_label.installEventFilter(self)  # 安装事件过滤器以捕获鼠标事件

        # 创建 QScrollArea 并将 QLabel 放入其中
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.image_label)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # 加载并显示图像
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

        # 保存图像尺寸
        self.image_width = pixmap.width()
        self.image_height = pixmap.height()

    def eventFilter(self, source, event):
        """事件过滤器，用于捕获鼠标点击事件"""
        if event.type() == event.MouseButtonPress and source is self.image_label:
            # 获取鼠标点击位置（相对于 QLabel 的坐标）
            pos = event.pos()
            x = pos.x()
            y = pos.y()

            # 检查是否在图像范围内
            if 0 <= x < self.image_width and 0 <= y < self.image_height:
                print(f"鼠标点击位置坐标: ({x}, {y})")

        return super().eventFilter(source, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 替换为您的图像路径
    image_path = 'Image_20250401163257694.jpg'

    viewer = ImageViewer(image_path)
    viewer.show()
    sys.exit(app.exec_())