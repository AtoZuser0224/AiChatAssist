import time

import openai
from hangul_utils import join_jamos
import pyperclip
import clipboard


def text_macro(input_text):
    # 공백문자를 다른 문자로 변환
    replaced_text = input_text.replace(" ", 'ㅁ')

    # 변환된 문자열 출력
    return replaced_text


openai.api_key = "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"

messages = []
from pynput import keyboard
import pyautogui

lanaguage = input("언어를 설정 : ")
trigger = 0
prom = ""
kor = ""


# 'a' 키를 누를 때 실행되는 콜백 함수
def on_key_press(key):
    global trigger
    global prom
    global kor
    global lanaguage
    try:
        if key.char == '/':
            if trigger == 0:
                print("trigger = ready")
                trigger = 1
            elif trigger == 1:
                print("trigger = start")
                trigger = 2
            elif trigger == 2:
                print("trigger = ready2")
                trigger = 3
            elif trigger == 3:
                print("trigger = start2")
                pyautogui.hotkey('ctrl', 'x')

                kor = clipboard.paste()
                print(kor)

                pyperclip.copy(kor)
                user_content = kor + ("를 " + lanaguage + " 언어로 만들어줘 그대신 사용하는 방법같은건 하나도 말하지마")
                messages.append({"role": "user", "content": f"{user_content}"})

                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

                assistant_content = completion.choices[0].message["content"].strip()

                messages.append({"role": "assistant", "content": f"{assistant_content}"})
                lines = text_macro(assistant_content).splitlines()

                # 리스트에 저장된 각 줄의 문자열 출력
                for line in lines:
                    for i in range(len(line)):
                        if "ㅁ" == line[i]:
                            pyautogui.press('space')
                        else:
                            pyperclip.copy(line[i])
                            pyautogui.hotkey('ctrl', 'v')


                        print(line)
                    pyautogui.press('enter')
                    pyautogui.press('home')

                trigger = 0
                prom = ""

    except AttributeError:
        pass


# 키 이벤트 리스너 등록
with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()
