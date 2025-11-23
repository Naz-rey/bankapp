from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
import os, sys, re

Window.size = (350, 650)

DATA_FILE = "users.txt"
LAST_FILE = "last_user.txt"



def parse_balance(balance_str):
    """
    balance_str: мүмкін болатын форматтар: "3500тг", "3500 tg", "3500tg", "3500"
    қайтару: int саны (немесе 0)
    """
    if not balance_str:
        return 0
    
    m = re.search(r'(\d+)', balance_str)
    if m:
        return int(m.group(1))
    try:
        return int(balance_str)
    except:
        return 0

def load_users():
    users = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(":", maxsplit=3)
             
                if len(parts) == 1:
                   
                    continue
                if len(parts) == 2:
                    name = parts[0].strip()
                    balance = parse_balance(parts[1].strip())
                    pin = ""
                    bought_list = []
                elif len(parts) == 3:
                    name = parts[0].strip()
                    balance = parse_balance(parts[1].strip())
                    pin = parts[2].strip()
                    bought_list = []
                else:  # len = 4
                    name = parts[0].strip()
                    balance = parse_balance(parts[1].strip())
                    pin = parts[2].strip()
                    bought_field = parts[3].strip()
                    bought_list = [b for b in (bought_field.split(",") if bought_field else []) if b]

                users[name] = {
                    "balance": balance,
                    "pin": pin,
                    "bought": bought_list
                }
    return users

def save_users(users):
    
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        for name, data in users.items():
            bought = ",".join(data.get("bought", []))
            f.write(f"{name}:{data.get('balance',0)}тг:{data.get('pin','')}:{bought}\n")

def save_last_user(username):
    with open(LAST_FILE,"w",encoding="utf-8") as f:
        f.write(username or "")

def load_last_user():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE,"r",encoding="utf-8") as f:
            return f.read().strip()
    return None



def round_btn(text, func):
    btn = Button(
        text=text,
        font_size=24,
        background_color=(1,1,1,1),
        color=(0,0.4,0,1),
        background_normal=""
    )
    btn.border = (30,30,30,30)
    btn.bind(on_press=func)
    return btn

class StartScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation="vertical", spacing=20, padding=40)
        with layout.canvas.before:
            Color(1,1,1,1)
            self.bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        layout.bind(pos=self.update_bg, size=self.update_bg)

        login_btn = round_btn("Кіру", lambda inst: setattr(self.manager, 'current', 'login'))
        reg_btn = round_btn("Тіркелу", lambda inst: setattr(self.manager, 'current', 'register'))

        layout.add_widget(login_btn)
        layout.add_widget(reg_btn)
        self.add_widget(layout)

    def update_bg(self, *a):
        self.bg.size = self.size
        self.bg.pos = self.pos

class RegisterScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation="vertical", spacing=15, padding=20)
        with layout.canvas.before:
            Color(1,1,1,1)
            self.bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        layout.bind(size=self.update_bg,pos=self.update_bg)

        layout.add_widget(Label(text="Пайдаланушы аты", font_size=22))
        self.username = TextInput(multiline=False, font_size=22)
        layout.add_widget(self.username)

        layout.add_widget(Label(text="PIN", font_size=22))
        self.pin = TextInput(multiline=False, password=True, font_size=22)
        layout.add_widget(self.pin)

        btn = round_btn("Тіркелу", self.register_user)
        layout.add_widget(btn)

        self.add_widget(layout)

    def update_bg(self, *a):
        self.bg.size=self.size
        self.bg.pos=self.pos

    def register_user(self, instance):
        username = self.username.text.strip()
        pin = self.pin.text.strip()
        users = load_users()

        if not username or not pin:
            Popup(title="Қате", content=Label(text="Бос орын болмауы керек"),
                  size_hint=(0.7,0.4)).open()
            return

        if username in users:
            Popup(title="Қате", content=Label(text="Пайдаланушы бұрыннан бар"),
                  size_hint=(0.7,0.4)).open()
            return

        users[username] = {"balance":0, "pin":pin, "bought":[]}
        save_users(users)

        Popup(title="Сәтті", content=Label(text="Тіркелді!"), size_hint=(0.7,0.4)).open()
        self.manager.current = "login"

class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation="vertical", spacing=15, padding=20)
        with layout.canvas.before:
            Color(1,1,1,1)
            self.bg = RoundedRectangle(size=self.size,pos=self.pos,radius=[20])
        layout.bind(size=self.update_bg,pos=self.update_bg)

        layout.add_widget(Label(text="Пайдаланушы аты", font_size=22))
        self.username = TextInput(multiline=False, font_size=22)
        layout.add_widget(self.username)

        layout.add_widget(Label(text="PIN", font_size=22))
        self.pin = TextInput(multiline=False, font_size=22, password=True)
        layout.add_widget(self.pin)

        btn = round_btn("Кіру", self.login)
        layout.add_widget(btn)

        self.add_widget(layout)

    def update_bg(self,*a):
        self.bg.size=self.size
        self.bg.pos=self.pos

    def login(self, instance):
        uname = self.username.text.strip()
        pin = self.pin.text.strip()
        users = load_users()

        if uname in users and users[uname]["pin"] == pin:
            save_last_user(uname)
            self.manager.get_screen("main").set_user(uname)
            self.manager.current = "main"
        else:
            Popup(title="Қате", content=Label(text="Қате деректер"), size_hint=(0.7,0.4)).open()

class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_user = None

        self.layout = BoxLayout(orientation="vertical", spacing=5, padding=5)
        with self.layout.canvas.before:
            Color(1,1,1,1)
            self.bg = RoundedRectangle(size=self.size,pos=self.pos,radius=[15])
        self.layout.bind(size=self.update_bg,pos=self.update_bg)

        self.top_layout = BoxLayout(size_hint=(1,0.35), padding=20)
        with self.top_layout.canvas.before:
            Color(0,0.7,0,1)
            self.rect = RoundedRectangle(size=self.top_layout.size,pos=self.top_layout.pos,radius=[20])
        self.top_layout.bind(size=self.update_top_rect,pos=self.update_top_rect)

        self.balance_label = Label(text="", font_size=60, color=(1,1,1,1), bold=True)
        self.top_layout.add_widget(self.balance_label)
        self.layout.add_widget(self.top_layout)

        btns = [
            ("Аудару", self.transfer_popup),
            ("NFC", self.nfc_popup),
            ("Дүкен", self.shop_popup),
            ("Хабарламалар", self.show_bought),
            ("Шығу (App)", self.exit_app),
            ("Аккаунттан шығу", self.logout)
        ]
        for name, func in btns:
            self.layout.add_widget(round_btn(name, func))

        self.add_widget(self.layout)

    def update_bg(self,*a):
        self.bg.size=self.layout.size
        self.bg.pos=self.layout.pos

    def update_top_rect(self,*a):
        self.rect.size=self.top_layout.size
        self.rect.pos=self.top_layout.pos

    def set_user(self, uname):
        self.current_user = uname
        self.update_display()

    def update_display(self):
        users = load_users()
        bal = users.get(self.current_user, {}).get("balance", 0)
        self.balance_label.text = f"{bal} тг"

    def transfer_popup(self, instance):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        layout.add_widget(Label(text="Кімге:", font_size=22))
        user_input = TextInput(multiline=False, font_size=22)
        layout.add_widget(user_input)

        layout.add_widget(Label(text="Сома:", font_size=22))
        amount_input = TextInput(multiline=False, font_size=22, input_filter="int")
        layout.add_widget(amount_input)

        btn_send = round_btn("Жіберу", lambda inst: None)
        layout.add_widget(btn_send)

        popup = Popup(title="Аудару", content=layout, size_hint=(0.8,0.7))

        def do_send(inst):
            to = user_input.text.strip()
            amt = amount_input.text.strip()
            users = load_users()
            if to not in users:
                popup.content.add_widget(Label(text="Пайдаланушы жоқ", color=(1,0,0,1)))
                return
            if not amt.isdigit():
                popup.content.add_widget(Label(text="Сома дұрыс емес", color=(1,0,0,1)))
                return
            amt_i = int(amt)
            if users[self.current_user]["balance"] < amt_i:
                popup.content.add_widget(Label(text="Баланс жетпейді", color=(1,0,0,1)))
                return
            users[self.current_user]["balance"] -= amt_i
            users[to]["balance"] += amt_i
            save_users(users)
            self.update_display()
            popup.dismiss()

        btn_send.unbind(on_press=None)
        btn_send.bind(on_press=do_send)
        popup.open()

    def nfc_popup(self, instance):
        Popup(title="NFC", content=Label(text="Төлем терминалға жақындат"), size_hint=(0.7,0.4)).open()

    def shop_popup(self, instance):
        goods = {
            "Телефон": 3000,
            "Ноутбук": 10000,
            "Құлаққап": 1500,
            "Сағат": 2500
        }

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        popup = Popup(title="Дүкен", content=layout, size_hint=(0.9,0.9))

        for item, price in goods.items():
            def make_buy(i):
                return lambda inst: self.buy(i, popup)
            layout.add_widget(round_btn(f"{item} - {price} тг", make_buy(item)))

        close = round_btn("Жабу", lambda inst: popup.dismiss())
        layout.add_widget(close)
        popup.open()

    def buy(self, item, popup=None):
        users = load_users()
        price_map = {"Телефон":3000,"Ноутбук":10000,"Құлаққап":1500,"Сағат":2500}
        price = price_map.get(item, 0)

        if users[self.current_user]["balance"] < price:
            Popup(title="Қате", content=Label(text="Баланс жетпейді"), size_hint=(0.7,0.4)).open()
            return

        users[self.current_user]["balance"] -= price
        users[self.current_user].setdefault("bought", []).append(item)
        save_users(users)
        self.update_display()

        if popup:
            popup.dismiss()
        Popup(title="Сәтті", content=Label(text=f"{item} жолда келеді"), size_hint=(0.7,0.4)).open()

    def show_bought(self, instance):
        users = load_users()
        lst = users.get(self.current_user, {}).get("bought", [])
        text = "\n".join(lst) if lst else "Сатып алынған тауар жоқ"
        Popup(title="Сатып алынғандар", content=Label(text=text), size_hint=(0.8,0.7)).open()

    def exit_app(self, instance):
        App.get_running_app().stop()
        sys.exit()

    def logout(self, instance):
        save_last_user("")
        self.manager.current = "login"

class BankApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MainScreen(name="main"))

        last = load_last_user()
        if last:
            sm.get_screen("login").username.text = last
            sm.current = "login"
        else:
            sm.current = "start"
        return sm

if __name__ == "__main__":
    BankApp().run()



