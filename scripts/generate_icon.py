"""Script to programmatically generate authentic Casio fx-570ES PLUS 2nd Edition application icons."""
import os
import sys
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QGuiApplication,
    QImage,
    QPainter,
    QColor,
    QBrush,
    QPen,
    QFont,
    QPainterPath,
    QLinearGradient,
    QRadialGradient,
)


def generate_icon(size: int = 256) -> QImage:
    image = QImage(size, size, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

    scale = size / 256.0

    # 1. Outer calculator body (matte black rounded rectangle)
    body_rect = QRectF(24 * scale, 12 * scale, 208 * scale, 232 * scale)
    body_path = QPainterPath()
    body_path.addRoundedRect(body_rect, 28 * scale, 28 * scale)

    body_gradient = QLinearGradient(0, 0, 0, 256 * scale)
    body_gradient.setColorAt(0.0, QColor("#2a2d36"))
    body_gradient.setColorAt(0.05, QColor("#1c1d22"))
    body_gradient.setColorAt(0.95, QColor("#141518"))
    body_gradient.setColorAt(1.0, QColor("#0d0e10"))

    painter.fillPath(body_path, body_gradient)
    painter.setPen(QPen(QColor("#3d414d"), 2 * scale))
    painter.drawPath(body_path)

    # 2. Top Branding: CASIO
    font_brand = QFont("Arial", int(10 * scale), QFont.Weight.Bold)
    painter.setFont(font_brand)
    painter.setPen(QColor("#ffffff"))
    painter.drawText(QRectF(36 * scale, 22 * scale, 80 * scale, 16 * scale), Qt.AlignmentFlag.AlignLeft, "CASIO")

    font_model = QFont("Arial", int(7 * scale), QFont.Weight.Bold)
    painter.setFont(font_model)
    painter.setPen(QColor("#ccd2e0"))
    painter.drawText(QRectF(130 * scale, 23 * scale, 90 * scale, 16 * scale), Qt.AlignmentFlag.AlignRight, "fx-570ES")

    # 3. Recessed LCD Screen
    lcd_outer = QRectF(38 * scale, 42 * scale, 180 * scale, 54 * scale)
    painter.setPen(QPen(QColor("#252830"), 1.5 * scale))
    painter.setBrush(QBrush(QColor("#101114")))
    painter.drawRoundedRect(lcd_outer, 8 * scale, 8 * scale)

    lcd_screen = QRectF(42 * scale, 46 * scale, 172 * scale, 46 * scale)
    painter.setPen(QPen(QColor("#9da992"), 1 * scale))
    painter.setBrush(QBrush(QColor("#c2ceb8")))
    painter.drawRoundedRect(lcd_screen, 4 * scale, 4 * scale)

    # LCD content
    font_lcd_indicators = QFont("Consolas", int(6 * scale), QFont.Weight.Bold)
    painter.setFont(font_lcd_indicators)
    painter.setPen(QColor("#182b1f"))
    painter.drawText(QRectF(46 * scale, 48 * scale, 160 * scale, 10 * scale), Qt.AlignmentFlag.AlignLeft, "Math  DEG")

    font_lcd_digits = QFont("Consolas", int(15 * scale), QFont.Weight.Bold)
    painter.setFont(font_lcd_digits)
    painter.drawText(QRectF(46 * scale, 62 * scale, 164 * scale, 26 * scale), Qt.AlignmentFlag.AlignRight, "0.")

    # 4. Circular Replay D-Pad
    dpad_center_x = 128 * scale
    dpad_center_y = 122 * scale
    dpad_radius = 24 * scale

    dpad_grad = QRadialGradient(dpad_center_x, dpad_center_y, dpad_radius)
    dpad_grad.setColorAt(0.0, QColor("#3c3f4a"))
    dpad_grad.setColorAt(0.7, QColor("#262830"))
    dpad_grad.setColorAt(1.0, QColor("#18191e"))

    painter.setPen(QPen(QColor("#4a4e5c"), 1.5 * scale))
    painter.setBrush(dpad_grad)
    painter.drawEllipse(dpad_center_x - dpad_radius, dpad_center_y - (dpad_radius * 0.8), dpad_radius * 2, dpad_radius * 1.6)

    # D-pad arrows
    font_arrows = QFont("Arial", int(7 * scale), QFont.Weight.Bold)
    painter.setFont(font_arrows)
    painter.setPen(QColor("#ffffff"))
    painter.drawText(QRectF(dpad_center_x - 6 * scale, dpad_center_y - 18 * scale, 12 * scale, 10 * scale), Qt.AlignmentFlag.AlignCenter, "▲")
    painter.drawText(QRectF(dpad_center_x - 6 * scale, dpad_center_y + 8 * scale, 12 * scale, 10 * scale), Qt.AlignmentFlag.AlignCenter, "▼")
    painter.drawText(QRectF(dpad_center_x - 20 * scale, dpad_center_y - 5 * scale, 10 * scale, 10 * scale), Qt.AlignmentFlag.AlignCenter, "◀")
    painter.drawText(QRectF(dpad_center_x + 10 * scale, dpad_center_y - 5 * scale, 10 * scale, 10 * scale), Qt.AlignmentFlag.AlignCenter, "▶")

    # 5. Top Function Buttons (small dark oval/rounded keys)
    painter.setBrush(QBrush(QColor("#2f323a")))
    painter.setPen(QPen(QColor("#3d404b"), 1 * scale))
    # Left oval
    painter.drawRoundedRect(QRectF(44 * scale, 110 * scale, 22 * scale, 12 * scale), 6 * scale, 6 * scale)
    painter.drawRoundedRect(QRectF(72 * scale, 110 * scale, 22 * scale, 12 * scale), 6 * scale, 6 * scale)
    # Right oval
    painter.drawRoundedRect(QRectF(162 * scale, 110 * scale, 22 * scale, 12 * scale), 6 * scale, 6 * scale)
    painter.drawRoundedRect(QRectF(190 * scale, 110 * scale, 22 * scale, 12 * scale), 6 * scale, 6 * scale)

    # 6. Function rows (dark small keys)
    for row in range(2):
        for col in range(6):
            x = (42 + col * 29) * scale
            y = (144 + row * 16) * scale
            painter.setBrush(QBrush(QColor("#2e3037")))
            painter.setPen(QPen(QColor("#202126"), 1 * scale))
            painter.drawRoundedRect(QRectF(x, y, 25 * scale, 12 * scale), 3 * scale, 3 * scale)

    # 7. Number Rows & Operators
    # Row 1 of numbers: 7, 8, 9, DEL (Green), AC (Green)
    key_w = 31 * scale
    key_h = 16 * scale
    for col in range(3):
        x = (42 + col * 35) * scale
        y = 180 * scale
        painter.setBrush(QBrush(QColor("#e4e7ee")))
        painter.setPen(QPen(QColor("#b0b5c2"), 1 * scale))
        painter.drawRoundedRect(QRectF(x, y, key_w, key_h), 4 * scale, 4 * scale)

    # DEL & AC (Lime Green)
    for col in range(2):
        x = (147 + col * 35) * scale
        y = 180 * scale
        painter.setBrush(QBrush(QColor("#7dae2e")))
        painter.setPen(QPen(QColor("#547c1a"), 1 * scale))
        painter.drawRoundedRect(QRectF(x, y, key_w, key_h), 4 * scale, 4 * scale)

    # Bottom number rows (4, 5, 6, ×, ÷ / 1, 2, 3, +, - / 0, ., ×10, Ans, =)
    for row in range(2):
        for col in range(5):
            x = (42 + col * 35) * scale
            y = (200 + row * 19) * scale
            if col < 3:
                painter.setBrush(QBrush(QColor("#e4e7ee")))
                painter.setPen(QPen(QColor("#b0b5c2"), 1 * scale))
            else:
                painter.setBrush(QBrush(QColor("#d4d8e2")))
                painter.setPen(QPen(QColor("#9ca2b0"), 1 * scale))
            painter.drawRoundedRect(QRectF(x, y, key_w, key_h), 4 * scale, 4 * scale)

    painter.end()
    return image


def main():
    app = QGuiApplication.instance()
    if app is None:
        app = QGuiApplication(sys.argv)

    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "ui", "assets"))
    os.makedirs(assets_dir, exist_ok=True)

    png_path = os.path.join(assets_dir, "icon.png")
    ico_path = os.path.join(assets_dir, "icon.ico")

    # Generate high-res 256x256 image
    img_256 = generate_icon(256)
    img_256.save(png_path, "PNG")
    print(f"Generated: {png_path}")

    # Generate multi-res ico
    img_256.save(ico_path, "ICO")
    print(f"Generated: {ico_path}")


if __name__ == "__main__":
    main()
