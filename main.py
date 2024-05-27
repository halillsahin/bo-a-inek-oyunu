from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle,Ellipse
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import random
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

class CustomEllipseButton(Button):
    def __init__(self, **kwargs):
        super(CustomEllipseButton, self).__init__(**kwargs)
        self.default_color = (0, 0, 1, 1)  # Mavi renk
        self.disabled_color = (1, 1, 1, 0)  # Şeffaf
        self.background_color = (0, 0, 0, 0)
        self.is_transparent = False  # Butonun şeffaf olup olmadığını takip etmek için bir değişken
        with self.canvas.before:
            Color(*self.default_color)
            self.shape = Ellipse(size=self.size, pos=self.pos)
            self.bind(size=self.update_shape, pos=self.update_shape)
        
    def update_shape(self, *args):
        self.shape.size = self.size
        self.shape.pos = self.pos

    def change_color(self, transparent=False):
        self.is_transparent = transparent  # Butonun şeffaf olup olmadığını güncelle
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.disabled_color if transparent else self.default_color)
            self.shape = Ellipse(size=self.size, pos=self.pos)
    

class Stopwatch(Label):
    def __init__(self, **kwargs):
        super(Stopwatch, self).__init__(**kwargs)
        self.elapsed_time = 0
        self.text = "00:00:00"
        self.event = Clock.schedule_interval(self.update_time, 1)
        with self.canvas.before:
            Color(1, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_time(self, dt):
        self.elapsed_time += 1
        minutes, seconds = divmod(self.elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        self.text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def stop(self):
        Clock.unschedule(self.event)


class Denemesayisi_rengi(Label):
    def __init__(self, **kwargs):
        super(Denemesayisi_rengi, self).__init__(**kwargs)
        
        self.text="DENEME SAYISI:0 "
        self.color = [0, 0, 0, 1]
        with self.canvas.before:
            Color(0, 1, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class TextInputCustom(TextInput):
    def __init__(self, **kwargs):
        super(TextInputCustom, self).__init__(**kwargs)
        self.filter_characters = "0123456789"
        self.multiline=False
        

    def insert_text(self, substring, from_undo=False):
        if all(char in self.filter_characters for char in substring):
            super(TextInputCustom, self).insert_text(substring, from_undo=from_undo)

  


class MainApp(App):
    gizlisayi = None

    @staticmethod
    def olustur_gizlisayi():
        if MainApp.gizlisayi is None:
            numaralar = list(range(10))
            random.shuffle(numaralar)
            MainApp.gizlisayi = "".join(map(str, numaralar[:4]))
        return MainApp.gizlisayi

    def build(self):
        layout = BoxLayout(orientation='vertical')
        # Bölümler
        top_section = GridLayout(cols=3, size_hint_y=0.30)
        middle_section = BoxLayout(size_hint_y=0.55)
        bottom_section = GridLayout(rows=1, cols=10, size_hint_y=0.15)

        # İlk bölüm envanterleri
        self.stopwatch = Stopwatch()
        self.denemesayisi = Denemesayisi_rengi()
        temizle_butonu = Button(text="TEMİZLE")
        temizle_butonu.bind(on_press=self.temizle_but)
        self.denenensayı=0
        self.textinput = TextInputCustom(hint_text='4 Haneli Bir Sayı Giriniz ', font_size=45,disabled=True)
        self.textinput.bind(text=self.elemansayisi)  # TextInput değişikliklerini dinlemek için bağlama
        self.textinput.bind(text=self.buton_rengi)
        self.textinput.bind(on_text_validate=self.kontrol_but)
        self.kontrol_butonu=Button(text="KONTROL ET")
        self.kontrol_butonu.disabled=True
        self.kontrol_butonu.bind(on_press=self.kontrol_but)     
            
        
        # İlk bölüm elemanları ekleme
        top_section.add_widget(self.stopwatch)
        top_section.add_widget(self.denemesayisi)
        top_section.add_widget(temizle_butonu)
        top_section.add_widget(Label(text="LÜTFEN TAHMİNİNİZİ GİRİNİZ: ", color=[0, 0, 0, 1],font_size=23))
        top_section.add_widget(self.textinput)
        top_section.add_widget(self.kontrol_butonu)
        
        # Orta bölüm
        self.sonuc_ekrani = Label(text="",font_size=30,color=[0.8,0.4,0.4,1])
        middle_section.add_widget(self.sonuc_ekrani)

        # Butonların oluşturulması ve fonksiyonların eklenmesi
        self.buton0 = CustomEllipseButton(text="0")
        self.buton0.bind(on_press=self.buton00)
        self.buton1 = CustomEllipseButton(text="1")
        self.buton1.bind(on_press=self.buton11)
        self.buton2 = CustomEllipseButton(text="2")
        self.buton2.bind(on_press=self.buton22)
        self.buton3 = CustomEllipseButton(text="3")
        self.buton3.bind(on_press=self.buton33)
        self.buton4 = CustomEllipseButton(text="4")
        self.buton4.bind(on_press=self.buton44)
        self.buton5 = CustomEllipseButton(text="5")
        self.buton5.bind(on_press=self.buton55)
        self.buton6 = CustomEllipseButton(text="6")
        self.buton6.bind(on_press=self.buton66)
        self.buton7 = CustomEllipseButton(text="7")
        self.buton7.bind(on_press=self.buton77)
        self.buton8 = CustomEllipseButton(text="8")
        self.buton8.bind(on_press=self.buton88)
        self.buton9 = CustomEllipseButton(text="9")
        self.buton9.bind(on_press=self.buton99)

        # Butonların eklenmesi
        bottom_section.add_widget(self.buton0)
        bottom_section.add_widget(self.buton1)
        bottom_section.add_widget(self.buton2)
        bottom_section.add_widget(self.buton3)
        bottom_section.add_widget(self.buton4)
        bottom_section.add_widget(self.buton5)
        bottom_section.add_widget(self.buton6)
        bottom_section.add_widget(self.buton7)
        bottom_section.add_widget(self.buton8)
        bottom_section.add_widget(self.buton9)

        # Düzene bölümler eklenmesi
        layout.add_widget(top_section)
        layout.add_widget(middle_section)
        layout.add_widget(bottom_section)

        return layout

    # Butonların fonksiyonlarının oluşturulması
    def temizle_but(self, instance):
        self.textinput.text = ""

    def buton00(self, instance):
            if "0" in self.textinput.text :
               self.textinput.text+= ""
            else:
               self.textinput.text+="0"
               
               
           

    def buton11(self, instance):
            if "1"in self.textinput.text :
               self.textinput.text+= ""
            else:
               self.textinput.text+="1"

    def buton22(self, instance):
            if "2"in self.textinput.text :
               self.textinput.text+= ""
            else:
               self.textinput.text+="2"

    def buton33(self, instance):
            if "3"in self.textinput.text :
               self.textinput.text+= ""
            else:
               self.textinput.text+="3"

    def buton44(self, instance):
            if "4"in self.textinput.text :
               self.textinput.text+= ""
            else:
               self.textinput.text+="4"

    def buton55(self, instance):
            if "5"in self.textinput.text :
               self.textinput.text+= ""
            else:
               self.textinput.text+="5"

    def buton66(self, instance):
        if "6"in self.textinput.text :
               self.textinput.text+= ""
        else:
               self.textinput.text+="6"

    def buton77(self, instance):
            if "7" in self.textinput.text :
               self.textinput.text+= ""
            else:
               self.textinput.text+="7"

    def buton88(self, instance):
            if "8"in self.textinput.text :
                self.textinput.text+= ""
            else:
               self.textinput.text+="8"

    def buton99(self, instance):
           if "9"in self.textinput.text :
               self.textinput.text+= ""
           else:
               self.textinput.text+="9"

    def buton_rengi(self,instance,value):
        butonlarlist=[self.buton0,self.buton1,self.buton2,self.buton3,self.buton4,self.buton5,self.buton6,self.buton7,self.buton8,self.buton9]
        for i in butonlarlist:
            if i.text in self.textinput.text:
                i.change_color(True)
            else:
                i.change_color(False)
                

    def elemansayisi(self, instance,value):
        if len(self.textinput.text) == 4:
            self.kontrol_butonu.disabled = False
        else:
            self.kontrol_butonu.disabled = True
    
    def kontrol_but(self, instance):
        tahmin = self.textinput.text
        self.denenensayı+=1
        self.denemesayisi.text=f"DENEME SAYISI: {self.denenensayı}"
        boğa = 0
        inek = 0
        gizlisayi = MainApp.olustur_gizlisayi()


        for i in range(4):
            if gizlisayi[i] == tahmin[i]:
                boğa += 1

        for i in range(4):
            if tahmin[i] in gizlisayi and tahmin[i] != gizlisayi[i]:
                inek += 1

        if boğa == 4:
            self.sonuc_ekrani.text = "Tebrikler"
            self.stopwatch.stop()
            self.show_popup()
            self.ses_efekti()
        else:
            self.sonuc_ekrani.text += f" \n {self.textinput.text} ,  {boğa}  boğa,  {inek}  inek"
        self.textinput.text=""
    def show_popup(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(text=f"Tebrikler! {self.stopwatch.text} sürede ve {self.denenensayı} denemede bildiniz.")
        tekrar_oyna=Button(text="Tekrar Oyna")
        close_button = Button(text="Kapat")
        layout.add_widget(label)
        layout.add_widget(tekrar_oyna)
        layout.add_widget(close_button)

        popup = Popup(title='Kazandınız!',
                      content=layout,
                      size_hint=(None, None), size=(500, 300),
                      auto_dismiss=True)
        
        tekrar_oyna.bind(on_press=popup.dismiss)
        tekrar_oyna.bind(on_press=self.replay_game)
        close_button.bind(on_press=popup.dismiss)
        
        # Animasyon ekleme
        animation = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)
        animation.repeat = True  # Animasyonu sürekli tekrarla
        animation.start(label)  # Animasyonu label üzerinde başlat

        popup.open()
    def replay_game(self, instance):
        self.textinput.text = ""
        self.denenensayı = 0
        self.denemesayisi.text = f"DENEME SAYISI:{self.denenensayı}"
        self.sonuc_ekrani.text = ""
        self.stopwatch.stop()
        self.stopwatch.event = Clock.schedule_interval(self.stopwatch.update_time, 1)  # Süreyi tekrar başlat
        self.stopwatch.elapsed_time = 0
        MainApp.gizlisayi=None  # Yeni gizli sayı oluştur
    def ses_efekti(self):
        self.sound=SoundLoader.load(r"C:\Users\halil\OneDrive\Masaüstü\python boğa inek\ineksesi.MP3")
        self.sound.play()
if __name__ == '__main__':
    Window.clearcolor=0,1,0.9,1
    MainApp().run()
