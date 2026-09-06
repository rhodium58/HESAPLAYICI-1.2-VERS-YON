from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.utils import get_color_from_hex
import math


class HesaplaApp(App):
    def build(self):
        self.title = "ÇİFCİLER HESAPLAYICI"

        root = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        layout = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(8),
            size_hint_y=None,
        )
        layout.bind(minimum_height=layout.setter("height"))

        title = Label(
            text="[b]ÇİFCİLER HESAPLAYICI[/b]",
            markup=True,
            font_size=dp(24),
            size_hint_y=None,
            height=dp(55),
            halign="center",
            valign="middle",
        )
        title.bind(size=title.setter("text_size"))
        layout.add_widget(title)

        self._add_label(layout, "Uzunluk / Metraj (Metre) [X]:")
        self.input_uzunluk = self._add_input(layout)

        self._add_label(layout, "Genişlik / En (Metre) [Y]:")
        self.input_genislik = self._add_input(layout)

        self._add_label(layout, "Derinlik / Yükseklik [Z] (Beton vb. için):")
        self.input_derinlik = self._add_input(layout, "1")

        self._add_label(layout, "Hesaplanacak Malzeme:")
        self.spinner = Spinner(
            text="1- Hazır Beton (m³)",
            values=(
                "1- Hazır Beton (m³)",
                "2- BİMS 10cm (10x39x18.5)",
                "3- BİMS 15cm (15x39x18.5)",
                "4- BİMS 20cm (20x39x18.5)",
                "5- BİMS 25cm (25x39x18.5)",
                "6- BİMS 30cm (30x39x18.5)",
                "7- Tuğla 8.5cm (8.5x19x19)",
                "8- Tuğla 13.5cm (13.5x19x19)",
                "9- Tuğla 19cm (19x19x19)",
                "10- İzo Tuğla 20cm (20x24x23.5)",
                "11- İzo Tuğla 25cm (25x24x23.5)",
                "12- Yığma Tuğla (20x30x14)",
                "13- 40x40 cm Fayans",
                "14- 60x60 cm Fayans",
                "15- 60x120 cm Fayans",
                "16- Alçıpan Plakası (120x250 cm)",
                "17- 32. Sınıf Parke (8mm)",
                "18- 33. Sınıf Parke (10-12mm)",
                "19- Şilte Metresi (m²)",
            ),
            size_hint_y=None,
            height=dp(55),
            font_size=dp(15),
        )
        layout.add_widget(self.spinner)

        btn_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            spacing=dp(8),
        )

        hesapla_btn = Button(
            text="HESAPLA",
            background_color=get_color_from_hex("#159957"),
            background_normal="",
            font_size=dp(18),
            bold=True,
        )
        hesapla_btn.bind(on_press=self.hesapla)
        btn_layout.add_widget(hesapla_btn)

        temizle_btn = Button(
            text="TEMİZLE",
            background_color=get_color_from_hex("#555555"),
            background_normal="",
            font_size=dp(18),
            bold=True,
        )
        temizle_btn.bind(on_press=self.temizle)
        btn_layout.add_widget(temizle_btn)

        layout.add_widget(btn_layout)

        self.lbl_sonuc = Label(
            text="Ölçüleri girip HESAPLA butonuna basın.",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(150),
            halign="center",
            valign="middle",
        )
        self.lbl_sonuc.bind(size=self.lbl_sonuc.setter("text_size"))
        layout.add_widget(self.lbl_sonuc)

        root.add_widget(layout)
        return root

    @staticmethod
    def _add_label(layout, text):
        label = Label(
            text=text,
            font_size=dp(15),
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))
        layout.add_widget(label)

    @staticmethod
    def _add_input(layout, text=""):
        field = TextInput(
            text=text,
            input_filter="float",
            multiline=False,
            font_size=dp(20),
            size_hint_y=None,
            height=dp(52),
            padding=[dp(10), dp(10), dp(10), dp(10)],
        )
        layout.add_widget(field)
        return field

    def temizle(self, _instance):
        self.input_uzunluk.text = ""
        self.input_genislik.text = ""
        self.input_derinlik.text = "1"
        self.spinner.text = "1- Hazır Beton (m³)"
        self.lbl_sonuc.text = "Ölçüleri girip HESAPLA butonuna basın."

    def hesapla(self, _instance):
        try:
            x_text = self.input_uzunluk.text.strip().replace(",", ".")
            y_text = self.input_genislik.text.strip().replace(",", ".")
            z_text = self.input_derinlik.text.strip().replace(",", ".")

            if not x_text or not y_text:
                raise ValueError

            x = float(x_text)
            y = float(y_text)
            z = float(z_text) if z_text else 1.0

            if x <= 0 or y <= 0 or z <= 0:
                raise ValueError

            alan = x * y
            hacim = alan * z
            secim = self.spinner.text

            if secim.startswith("1-"):
                fireli_hacim = hacim * 1.05
                self.lbl_sonuc.text = (
                    f"Ebatlar: {x:.2f} m × {y:.2f} m × {z:.2f} m\n"
                    f"Net Beton Hacmi: {hacim:.2f} m³\n"
                    f"Önerilen (%5 Fireli): {fireli_hacim:.2f} m³"
                )

            elif "BİMS" in secim:
                net_bims = math.ceil(alan * 12.5)
                fireli_bims = math.ceil(net_bims * 1.07)
                self.lbl_sonuc.text = (
                    f"Duvar Alanı: {alan:.2f} m²\n"
                    f"Net BİMS: {net_bims} Adet\n"
                    f"Önerilen (%7 Fire): {fireli_bims} Adet"
                )

            elif any(k in secim for k in ("Tuğla 8.5cm", "Tuğla 13.5cm", "Tuğla 19cm")):
                net_tugla = math.ceil(alan * 25)
                fireli_tugla = math.ceil(net_tugla * 1.08)
                self.lbl_sonuc.text = (
                    f"Duvar Alanı: {alan:.2f} m²\n"
                    f"Net Tuğla: {net_tugla} Adet\n"
                    f"Önerilen (%8 Fire): {fireli_tugla} Adet"
                )

            elif "İzo Tuğla" in secim:
                net_tugla = math.ceil(alan * 16)
                fireli_tugla = math.ceil(net_tugla * 1.08)
                self.lbl_sonuc.text = (
                    f"Duvar Alanı: {alan:.2f} m²\n"
                    f"Net İzo Tuğla: {net_tugla} Adet\n"
                    f"Önerilen (%8 Fire): {fireli_tugla} Adet"
                )

            elif "Yığma Tuğla" in secim:
                net_tugla = math.ceil(alan * 22)
                fireli_tugla = math.ceil(net_tugla * 1.08)
                self.lbl_sonuc.text = (
                    f"Duvar Alanı: {alan:.2f} m²\n"
                    f"Net Yığma Tuğla: {net_tugla} Adet\n"
                    f"Önerilen (%8 Fire): {fireli_tugla} Adet"
                )

            elif "40x40" in secim:
                net = math.ceil(alan / 0.16)
                fireli = math.ceil((alan * 1.10) / 0.16)
                self.lbl_sonuc.text = (
                    f"Zemin Alanı: {alan:.2f} m²\n"
                    f"Net Fayans: {net} Adet (40×40)\n"
                    f"Önerilen (%10 Fire): {fireli} Adet"
                )

            elif "60x60" in secim:
                net = math.ceil(alan / 0.36)
                fireli = math.ceil((alan * 1.10) / 0.36)
                self.lbl_sonuc.text = (
                    f"Zemin Alanı: {alan:.2f} m²\n"
                    f"Net Fayans: {net} Adet (60×60)\n"
                    f"Önerilen (%10 Fire): {fireli} Adet"
                )

            elif "60x120" in secim:
                net = math.ceil(alan / 0.72)
                fireli = math.ceil((alan * 1.10) / 0.72)
                self.lbl_sonuc.text = (
                    f"Zemin Alanı: {alan:.2f} m²\n"
                    f"Net Fayans: {net} Adet (60×120)\n"
                    f"Önerilen (%10 Fire): {fireli} Adet"
                )

            elif "Alçıpan" in secim:
                net = math.ceil(alan / 3.00)
                fireli = math.ceil((alan * 1.05) / 3.00)
                self.lbl_sonuc.text = (
                    f"Kaplama Alanı: {alan:.2f} m²\n"
                    f"Net Alçıpan: {net} Plaka\n"
                    f"Önerilen (%5 Fire): {fireli} Plaka"
                )

            elif "32. Sınıf" in secim:
                paket = math.ceil((alan * 1.10) / 1.83)
                self.lbl_sonuc.text = (
                    f"Alan: {alan:.2f} m²\n"
                    f"Gereken: {paket} Paket (32. Sınıf Parke)\n"
                    f"Toplam Metraj: {paket * 1.83:.2f} m²"
                )

            elif "33. Sınıf" in secim:
                paket = math.ceil((alan * 1.10) / 1.50)
                self.lbl_sonuc.text = (
                    f"Alan: {alan:.2f} m²\n"
                    f"Gereken: {paket} Paket (33. Sınıf Parke)\n"
                    f"Toplam Metraj: {paket * 1.50:.2f} m²"
                )

            elif "Şilte" in secim:
                silte_m2 = alan * 1.05
                rulo = math.ceil(silte_m2 / 15.0)
                self.lbl_sonuc.text = (
                    f"Net Zemin: {alan:.2f} m²\n"
                    f"Gereken Şilte (%5 Fire): {silte_m2:.2f} m²\n"
                    f"Rulo Sayısı (15 m²'lik): {rulo} Rulo"
                )

        except (ValueError, TypeError):
            self.lbl_sonuc.text = "Lütfen X, Y ve Z için geçerli ve 0'dan büyük sayılar giriniz!"


if __name__ == "__main__":
    HesaplaApp().run()
