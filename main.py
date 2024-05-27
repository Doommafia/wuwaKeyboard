import tkinter as tk
import keyboard

#CONSTANTS
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 250
key_width = 60
key_height = 60
spacing = 10
long_key = key_width * 3 + spacing * 2

# KEY_LAYOUT
keys = {
    'W': (spacing * 4 + key_width, spacing),
    'A': (spacing * 3, key_height + spacing * 2),
    'S': (spacing * 4 + key_width, key_height + spacing * 2),
    'D': (spacing * 5 + key_width * 2, key_height + spacing * 2),
    'Q': (spacing * 3 , spacing),
    'E': (spacing * 5 + key_width * 2, spacing),
    'R': (spacing * 6 + key_width * 3, spacing),
    'SHIFT': (spacing * 3 , key_height * 2 + spacing * 3),
    'SPACE': (spacing * 4 + key_width, key_height * 2 + spacing * 3),
}

key_states = {key: False for key in keys}

root = tk.Tk()
root.title('Keyboard Overlay')
root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')
root.overrideredirect(True)  # NO BORDER/TITLE
root.wm_attributes("-topmost", 1)  # ONTOP

canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

def draw_key(key, position, pressed, width=key_width):
    x, y = position
    color = 'blue' if pressed else 'grey'
    canvas.create_rectangle(x, y, x + width, y + key_height, fill=color, outline='black')
    text = key
    canvas.create_text(x + width // 2, y + key_height // 2, text=text, font=('Helvetica', '20'))

def update_keys():
    canvas.delete('all')  
    for key, position in keys.items():
        draw_key(key, position, key_states[key], width=long_key if key in ['SPACE'] else key_width)

def on_key_event(e):
    key = e.name.upper()
    if key == '0':  
        root.destroy() 
    if key in key_states:
        key_states[key] = e.event_type == keyboard.KEY_DOWN
        update_keys()

keyboard.hook(on_key_event)

root.mainloop()
