from src.ui.main_window import MainWindow

def test_window_launch(application):
    window = MainWindow()
    window.show()
    application.processEvents()
    assert window.isVisible()
    assert window.windowTitle() == "Scientific Calculator"
    window.close()
