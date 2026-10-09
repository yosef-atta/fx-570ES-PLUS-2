from src.ui.main_window import MainWindow

def test_window_launch(application):
    window = MainWindow()
    window.show()
    application.processEvents()
    assert window.isVisible()
    assert window.windowTitle() == "Scientific Calculator"
    assert window.minimumWidth() >= 470
    assert window.minimumHeight() >= 690
    window.close()
    application.processEvents()
    assert not window.isVisible()

def test_startup_state_clean(application):
    window = MainWindow()
    state = window.controller.state
    # Ensure startup executes zero mathematical operations
    assert state.expression == ""
    assert state.result == ""
    assert state.mode == "COMP"
    assert state.power_on is True
    assert len(state.deferred_actions) == 0
    window.close()

