import pygame
import sys
import ctypes
from ctypes import wintypes

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200
RIDEV_INPUTSINK = 0x00000100
key_width = 60
key_height = 60
spacing = 10
long_key = key_width * 3 + spacing * 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption('Keyboard Overlay')

hwnd = pygame.display.get_wm_info()["window"]
SWP_NOACTIVATE = 0x0010
HWND_TOPMOST = -1

user32 = ctypes.WinDLL('user32', use_last_error=True)
SetWindowPos = user32.SetWindowPos
SetWindowPos.restype = wintypes.BOOL
SetWindowPos.argtypes = [
    wintypes.HWND,  # hWnd
    wintypes.HWND,  # hWndInsertAfter
    ctypes.c_int,   # X
    ctypes.c_int,   # Y
    ctypes.c_int,   # cx
    ctypes.c_int,   # cy
    ctypes.c_uint,  # uFlags
]

SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SWP_NOACTIVATE)

font = pygame.font.SysFont(None, 48)

# Key positions based on typical keyboard layout
keys = {
    'W': (spacing * 4 + key_width, spacing),
    'A': (spacing * 3, key_height + spacing * 2),
    'S': (spacing * 4 + key_width, key_height + spacing * 2),
    'D': (spacing * 5 + key_width * 2, key_height + spacing * 2),
    'E': (spacing * 5 + key_width * 2, spacing),
    'R': (spacing * 6 + key_width * 3, spacing),
    'SH': (spacing, key_height * 2 + spacing * 3),
    'SB': (spacing * 2 + key_width, key_height * 2 + spacing * 3)
}

key_states = {key: False for key in keys}

def draw_key(screen, key, position, pressed, width=key_width):
    x, y = position
    color = (100, 100, 255) if pressed else (170, 170, 170)
    pygame.draw.rect(screen, color, (x, y, width, key_height))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, key_height), 2)
    text = font.render(key, True, (0, 0, 0))
    text_rect = text.get_rect(center=(x + width // 2, y + key_height // 2))
    screen.blit(text, text_rect)

def main():
    register_raw_input()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.upper() in key_states:
                    key_states[event.unicode.upper()] = True
                elif event.key == pygame.K_SPACE:
                    key_states['SB'] = True
                elif event.key == pygame.K_LSHIFT:
                    key_states['SH'] = True
            elif event.type == pygame.KEYUP:
                if event.unicode.upper() in key_states:
                    key_states[event.unicode.upper()] = False
                elif event.key == pygame.K_SPACE:
                    key_states['SB'] = False
                elif event.key == pygame.K_LSHIFT:
                    key_states['SH'] = False

        screen.fill((255, 255, 255))

        for key, position in keys.items():
            if key == 'SB':
                draw_key(screen, key, position, key_states[key], width=long_key)
            else:
                draw_key(screen, key, position, key_states[key])

        pygame.display.flip()

def register_raw_input():
    class RAWINPUTDEVICE(ctypes.Structure):
        _fields_ = [("usUsagePage", ctypes.c_ushort),
                    ("usUsage", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong),
                    ("hwndTarget", ctypes.c_void_p)]

    RegisterRawInputDevices = ctypes.windll.user32.RegisterRawInputDevices
    RegisterRawInputDevices.argtypes = [ctypes.POINTER(RAWINPUTDEVICE), ctypes.c_uint, ctypes.c_uint]

    rid = RAWINPUTDEVICE()
    rid.usUsagePage = 0x01
    rid.usUsage = 0x06
    rid.dwFlags = RIDEV_INPUTSINK
    rid.hwndTarget = ctypes.windll.user32.GetActiveWindow()

    if not RegisterRawInputDevices(ctypes.byref(rid), 1, ctypes.sizeof(rid)):
        raise ctypes.WinError()

if __name__ == '__main__':
    main()
