from pynput import keyboard
from pynput.keyboard import Controller ,Key
from tkinter import *
import pystray
from PIL import Image
from pystray import MenuItem as item
import sys
import os
import subprocess
from tkinter import messagebox
import ctypes

processes = subprocess.Popen('tasklist', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]

dev_mode = False


if processes.decode().count(os.path.basename(sys.executable)) > 2  and not dev_mode:
    messagebox.showerror('App already running!', f'{os.path.basename(sys.executable)} already running')
    sys.exit(0)

def resource_path(relative_path):

    try:

        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_languages():
    with open(resource_path('language_dict' ), 'r') as f:
        return ({x[-1].strip() : x[0] for x in [r.split('		') for r in f.read().split('\n')]})


def get_keyboard_language():
    languages = get_languages()

    user32 = ctypes.WinDLL('user32', use_last_error=True)

    handle = user32.GetForegroundWindow()

    threadid = user32.GetWindowThreadProcessId(handle, 0)

    layout_id = user32.GetKeyboardLayout(threadid)

    language_id = layout_id & (2 ** 16 - 1)

    language_id_hex = hex(language_id)

    if language_id_hex in languages.keys():
        return languages[language_id_hex]
    else:
        return str(language_id_hex)

kbl = get_keyboard_language()


kbd = Controller()
shift_pressed = False
def switch_language():
    kbd.press(Key.alt_l)
    kbd.press(Key.shift)
    kbd.release(Key.alt_l)
    kbd.release(Key.shift)
if 'English' not in kbl and 'German' not in kbl:
    switch_language()
    if not dev_mode:
        subprocess.Popen(sys.executable)
        sys.exit()
    else:
        subprocess.Popen([sys.executable , __file__])
        sys.exit()




def on_activate_a():
    if not shift_pressed:
        kbd.type('ä')

def on_activate_A():
    kbd.type('Ä')

def on_activate_o():
    if not shift_pressed:
        kbd.type('ö')

def on_activate_O():
    kbd.type('Ö')

def on_activate_u():
    if not shift_pressed:
        kbd.type('ü')

def on_activate_U():
    kbd.type('Ü')


def on_activate_S():
    kbd.type('ẞ')


def on_press(key):
    global shift_pressed
    if key == keyboard.Key.shift_l:

        shift_pressed = True

def on_release(key):
    global shift_pressed
    if key == keyboard.Key.shift_l:

        shift_pressed = False





hotkeys = {

        '<ctrl>+<alt>+a': on_activate_a,
        '<ctrl>+<alt>+<shift>+a': on_activate_A,
        '<ctrl>+<alt>+u': on_activate_u,
        '<ctrl>+<alt>+<shift>+u': on_activate_U,
        '<ctrl>+<alt>+o': on_activate_o,
        '<ctrl>+<alt>+<shift>+o': on_activate_O,
        '<ctrl>+<alt>+s': on_activate_S,

}

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
h = keyboard.GlobalHotKeys(hotkeys)


inst = '''
Easy German Letters keyboard Shortcuts:

   ctrl+alt+a ---> ä
   ctrl+alt+shift+a ---> Ä

   ctrl+alt+u ---> ü
   ctrl+alt+shift+u ---> Ü

   ctrl+alt+o ---> ö
   ctrl+alt+shift+o ---> Ö

   ctrl+alt+s ---> ẞ
   ctrl+alt+shift+s ---> ẞ

You can close the window and the application will continue running in the background.
You can exit the app completely by closing the window and clicking 'Quit' on the tray icon menu.
enjoy!

'''

win = Tk()
win.title("Instructions")
win.iconbitmap(resource_path('favicon.ico'))
l = Label(win, text=inst).pack()


def quit_window(icon, item):
    h.stop()
    listener.stop()
    icon.stop()
    win.destroy()


def show_instructions(icon, item):
    icon.stop()
    win.after(0, win.deiconify)


def hide_window():
    image = Image.open(resource_path('favicon.ico'))
    win.withdraw()
    menu = (item('Quit', quit_window), item('Instructions', show_instructions))
    icon = pystray.Icon("name", image, "Easy german keyboard", menu)
    icon.run()


win.protocol('WM_DELETE_WINDOW', hide_window)


if __name__ == "__main__":
    h.start()
    listener.start()
    win.mainloop()
    listener.join()
    h.join()