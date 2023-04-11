import openai
from hangul_utils import join_jamos
import pyperclip

cons = {'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ', 'T': 'ㅆ',
        'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ'}
# 모음-중성
vowels = {'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ', 'h': 'ㅗ', 'hk': 'ㅘ',
          'ho': 'ㅙ', 'hl': 'ㅚ',
          'y': 'ㅛ', 'n': 'ㅜ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'b': 'ㅠ', 'm': 'ㅡ', 'ml': 'ㅢ', 'l': 'ㅣ'}

# 자음-종성
cons_double = {'rt': 'ㄳ', 'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ', 'fx': 'ㄾ', 'fv': 'ㄿ',
               'fg': 'ㅀ', 'qt': 'ㅄ'}


def engkor(text):
    result = ''  # 영 > 한 변환 결과

    # 1. 해당 글자가 자음인지 모음인지 확인
    vc = ''
    for t in text:
        if t in cons:
            vc += 'c'
        elif t in vowels:
            vc += 'v'
        else:
            vc += '!'

    # cvv → fVV / cv → fv / cc → dd
    vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')

    # 2. 자음 / 모음 / 두글자 자음 에서 검색
    i = 0
    while i < len(text):
        v = vc[i]
        t = text[i]

        j = 1
        # 한글일 경우
        try:
            if v == 'f' or v == 'c':  # 초성(f) & 자음(c) = 자음
                result += cons[t]

            elif v == 'V':  # 더블 모음
                result += vowels[text[i:i + 2]]
                j += 1

            elif v == 'v':  # 모음
                result += vowels[t]

            elif v == 'd':  # 더블 자음
                result += cons_double[text[i:i + 2]]
                j += 1
            else:
                result += t

        # 한글이 아닐 경우
        except:
            if v in cons:
                result += cons[t]
            elif v in vowels:
                result += vowels[t]
            else:
                result += t

        i += j

    return join_jamos(result)


openai.api_key = "Your Api key"

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
                pyautogui.press('enter')
                pyperclip.copy(kor)
                user_content = kor + ("를 "+lanaguage+" 언어로")
                messages.append({"role": "user", "content": f"{user_content}"})

                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

                assistant_content = completion.choices[0].message["content"].strip()

                messages.append({"role": "assistant", "content": f"{assistant_content}"})
                pyperclip.copy(assistant_content)
                pyautogui.hotkey('ctrl', 'v')
                trigger = 0
                prom = ""
        elif trigger == 2:
            # 키 값을 한글로 변환

            prom = prom + key.char
            kor = engkor(prom)
            print(kor)

    except AttributeError:
        pass


# 키 이벤트 리스너 등록
with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()
