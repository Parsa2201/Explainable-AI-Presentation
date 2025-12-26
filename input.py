from pynput.mouse import Listener as MouseListener, Button
from pynput.keyboard import Controller as KeyboardController, Key

keyboard = KeyboardController()


def on_click(x, y, button, pressed):
    if button == Button.right and pressed:
        keyboard.press(Key.left)  # Simulate left arrow key press
        keyboard.release(Key.left)
    elif button == Button.left and pressed:
        keyboard.press(Key.right)  # Simulate right arrow key press
        keyboard.release(Key.right)

# Start mouse listener
with MouseListener(on_click=on_click) as listener:
    listener.join()