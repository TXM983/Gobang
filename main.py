import time
import pyautogui
import threading
import keyboard

# 设置点击间隔时间（单位：秒）
CLICK_INTERVAL = 1

# 设置点击持续时间（单位：秒）
CLICK_DURATION = 1

# 将 PyAutoGUI 的 FAILSAFE 特性设置为 False，以防止意外退出
pyautogui.FAILSAFE = False


def click_mouse():
    """模拟鼠标左键单击"""
    pyautogui.mouseDown(button='left')
    time.sleep(CLICK_DURATION)
    pyautogui.mouseUp(button='left')


def start_clicking():
    """开启连点器"""
    global is_clicking_enabled

    print("连点器已开启")
    is_clicking_enabled = True
    while is_clicking_enabled:
        click_mouse()
        time.sleep(CLICK_INTERVAL)


def stop_clicking():
    """关闭连点器"""
    global is_clicking_enabled

    print("连点器已关闭")
    is_clicking_enabled = False


# 初始化连点器状态
is_clicking_enabled = False

# 创建线程
start_thread = threading.Thread(target=start_clicking)
stop_thread = threading.Thread(target=stop_clicking)


# 监听小键盘按键事件
def on_key_pressed(event):
    global start_thread, stop_thread

    if event.name == '1':
        if not start_thread.is_alive():
            start_thread = threading.Thread(target=start_clicking)
            start_thread.start()
    elif event.name == '2':
        if not stop_thread.is_alive():
            stop_thread = threading.Thread(target=stop_clicking)
            stop_thread.start()


# 注册键盘事件监听器
keyboard.on_press(on_key_pressed)

while True:
    pass
