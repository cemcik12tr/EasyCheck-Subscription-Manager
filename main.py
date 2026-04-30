import flet as ft
import json
import os
import datetime
import calendar

# =============================================================================
# BÖLÜM 1: AYARLAR, SABİTLER VE VERİ YAPILARI
# =============================================================================
#---tarih ve zaman ayarları---
TR_ayları=["","Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
zaman=datetime.datetime.now()
suanki_gun = zaman.day
suanki_ay=zaman.month
suanki_yil=zaman.year
degisim_ay=suanki_ay
degisim_yil=suanki_yil


# --- Renk ve Kullanıcı Ayarları ---
KULLANICI_ADI = "Fatih Terim"
RENK_ANA = "#F8F9FA"       # Arka plan
RENK_KOYU = "#102C57"      # Lacivert
RENK_KIRMIZI = "#DC3545"   # İptal/Uyarı
RENK_YESIL = "#28A745"     # Onay
RENK_GRI = "#6C757D"

# --- İkon Sözlüğü ---
IKONLAR = {
    "Su": "water_drop",
    "Elektrik": "bolt",
    "Doğal gaz": "fire_extinguisher",
    "İnternet": "wifi",
    "Mobil": "phone_android",
    "Abonelik": "movie",
    "Netflix" : "MOVIE_FILTER_OUTLINED",
}

# --- Dropdown Seçenekleri ---
Secenekler = {
    "Dijital Abonelikler": {
        "Netflix":{"temel":[150],"standart":[200],"premium":[300]},
        "spotify":{"bireysel":[15],"öğrenci":[20],"duo":[40],"aile":[149.50]},
        "disney+":{"reklamlı":[45],"reklamsız":[95]},
        "hbo max":{"standar":[150],"özel":[1255]},
        "youtube":{"bireysel":[15],"aile":[85],"öğrenci":[95],"youtube music":[15]},
    },
    "fatura" : {
        "Elektrik": ["urfa","gebze","samsun","trabzon","kaçak"],
        "Su":["urfa","gebze","samsun","trabzon","kaçak"],
        "Doğal gaz":["urfa","gebze","samsun","trabzon","kaçak"],
        "İnternet":["urfa","gebze","samsun","trabzon","kaçak"],
        "Mobil":["türkcel","türktelekom","vodafone","bimcell"],
    },
    "diğer" : {"kira":[], "aidat":[], "taksit":[]}
}

# =============================================================================
# BÖLÜM 2: SINIFLAR (CLASSES)
# =============================================================================

class fatura(ft.Container):
    def __init__(self,fiyat,kategori,hizmet,paket,tarih):
        self.fiyat=fiyat
        self.kategori = kategori
        self.hizmet=hizmet
        self.paket=paket
        self.tarih=tarih

# =============================================================================
# BÖLÜM 3: MAIN FONKSİYONU VE UYGULAMA MANTIĞI
# =============================================================================

def main(page: ft.Page):
    
    # --- 3.1: Sayfa Ayarları ---
    page.title = "Easy Check"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = RENK_ANA
    page.padding = 1
    page.window.width, page.window.height = 400, 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- 3.2: Temel Değişkenler ve UI Nesneleri ---
    toplam = ft.Text(f"{0:.2f} TL", color="white", size=30, weight=ft.FontWeight.BOLD)
    
    abonelik_listesi = ft.Column(
        expand=False,
        spacing=10,
    )
    
    fiyat = ft.Text("",color="white",size=14)

    # --- 3.3: Yardımcı Fonksiyonlar (Hesaplama & Kayıt) ---
    
    def analiz_hesapla():
        ozet_veri={}
        for kart in abonelik_listesi.controls:
            if kart.data:
                f:fatura= kart.data
                if f.kategori == "Dijital Abonelikler":
                    if "Dijital Abonelikler" in ozet_veri:
                        ozet_veri["Dijital Abonelikler"]+=f.fiyat
                    else:
                        ozet_veri["Dijital Abonelikler"]=f.fiyat
                else:
                    if f.hizmet in ozet_veri:
                        ozet_veri[f.hizmet]+=f.fiyat
                    else:
                        ozet_veri[f.hizmet]=f.fiyat
        return ozet_veri



    def toplam_guncelle():
        t=sum(x.data.fiyat for x in abonelik_listesi.controls if x.data)
        toplam.value =(f"{t:.2f} TL")
        page.update()

    def verileri_kaydet():
        kaydedilenler = []
        for kart in abonelik_listesi.controls:
            if kart.data:
                f:fatura = kart.data
                if f:
                    kaydedilenler.append({"fiyat":f.fiyat,"kategori":f.kategori,"hizmet":f.hizmet,"paket":f.paket,"tarih":f.tarih     })

        with open("abonelikler.json", "w", encoding="utf-8") as dosya:
            json.dump(kaydedilenler, dosya, ensure_ascii=False, indent=4)

    # --- 3.4: Görsel Oluşturucu (Factory) ---
    
    def ay_degistir(e):
            global degisim_ay,degisim_yil
            if e.control.data==-1:
                degisim_ay -= 1
                if degisim_ay==0:
                    degisim_ay=12
                    degisim_yil-=1
            else:
                degisim_ay+=1
                if degisim_ay==13:
                    degisim_ay=1
                    degisim_yil+=1
            content_area.controls.clear()
            content_area.controls.append(takvim_olustur(degisim_yil,degisim_ay))

            page.update()


    def aylik_takvim(adasdas,gun,yil,ay):
            for abonelik in abonelik_listesi.controls :
                if abonelik.data:
                    o_gun,o_ay,o_yil =map(int ,abonelik.data.tarih.split("."))
                    if o_yil<2000:
                        o_yil+=2000
                    print(f"Listedeki: {o_gun}.{o_ay} - Aranan: {gun}.{ay}")
                    if  o_gun==gun and o_ay==ay and o_yil==yil:
                        adasdas.controls.append(ft.Container(ft.ListTile(
                            title=ft.Text(f"{abonelik.data.hizmet}",weight=ft.FontWeight.BOLD,size=14),
                            subtitle=ft.Text(f"son tarih:{abonelik.data.tarih} ",size=14,weight=ft.FontWeight.BOLD),
                            trailing=ft.Text(f"tutar {abonelik.data.fiyat:.2f} TL",weight=ft.FontWeight.BOLD,size=14)
                            ),bgcolor="white", border_radius=10, margin=2))
    


    def takvim_olustur(yil,ay):

        ilk_gun,ay_gun_sayisi = calendar.monthrange(yil,ay)
        son = 1
        gunler=[]
        o_ay=ft.Column(controls=[])
        for i in range(ilk_gun):
            gunler.append(ft.Container(ft.Text(""),
                bgcolor="grey",
                width=20,height=20,
                border_radius=20,shadow=ft.BoxShadow(blur_radius=5,color="grey"),
                alignment=ft.alignment.center,))
            
        for x in range(1,ay_gun_sayisi+1):
            if x==suanki_gun and ay == suanki_ay:
                gunler.append(ft.Container(ft.Text(f"{x}",color="white"),
                    bgcolor=RENK_KOYU,
                    width=20,height=20,
                    border_radius=20,shadow=ft.BoxShadow(blur_radius=5,color="grey"),
                     alignment=ft.alignment.center,))
                
            else:
                 gunler.append(ft.Container(ft.Text(f"{x}"),
                    bgcolor=RENK_ANA,
                    width=20,height=20,
                    border_radius=20,shadow=ft.BoxShadow(blur_radius=5,color="grey"),
                     alignment=ft.alignment.center,))
        for x in range(32):         
            aylik_takvim(o_ay,x,yil,ay)

        while len(gunler)<42:
            gunler.append(ft.Container(ft.Text(f"{son}"),
                bgcolor="grey",
                width=20,height=20,
                border_radius=20,shadow=ft.BoxShadow(blur_radius=5,color="grey"),
                alignment=ft.alignment.center,))
            son+=1

        baslik = ft.Container(ft.Row([ft.IconButton(ft.Icons.ARROW_LEFT,icon_color="grey",on_click=ay_degistir,data=-1),
            ft.Text(f"{ay}-{yil}"),
            ft.IconButton(ft.Icons.ARROW_RIGHT ,icon_color="grey",on_click=ay_degistir,data=+1),
            ]))
        
        takvim_izgarasi=ft.Container(ft.GridView(controls=gunler,runs_count=7,spacing=8,run_spacing=8,expand=False),
            bgcolor="white",
            padding=15,
            border_radius=15,
            margin=ft.margin.symmetric(horizontal=15),
            shadow=ft.BoxShadow(blur_radius=5,color="grey"),
            height=310,
            width=350
            )

        return ft.Column([baslik,takvim_izgarasi,o_ay])

    def analiz_grafigi_olustur():
        data=analiz_hesapla()
        dilimler=[]
        renkler=[ft.Colors.BLUE, ft.Colors.PURPLE, ft.Colors.RED,ft.Colors.ORANGE,ft.Colors.YELLOW,ft.Colors.GREEN]
        sayac=int(0)
        degerler=[]
        a_toplam=sum(x.data.fiyat for x in abonelik_listesi.controls if x.data)
        for isim,ucret in data.items():
            dilimler.append(
                ft.PieChartSection(
                    value=ucret,
                    title=f"{ucret}",
                    title_style=ft.TextStyle(size=12,weight=ft.FontWeight.BOLD,color="white"),
                    color=renkler[sayac%len(renkler)],
                    radius=60
                )
            )
            if a_toplam>0:
                yuzde=ucret/a_toplam*100
            else:
                yuzde=0
            degerler.append(ft.ListTile(
                leading=ft.Container(width=20,height=20,bgcolor=renkler[sayac%len(renkler)],border_radius=5),
                title=ft.Text(isim),
                trailing=ft.Text(f"{ucret} %{yuzde:.0f}",size=16,weight=ft.FontWeight.BOLD),
                )
            )
            sayac+=1
        
        bitis = ft.Column([
            ft.Container(ft.Text("Harcama Analizi", size=22,weight=ft.FontWeight.BOLD,color=RENK_KOYU,),padding=20),
            ft.PieChart(sections=dilimler,center_space_radius=50,sections_space=2),
            ft.Container(
                content=ft.Column(degerler,scroll=ft.ScrollMode.AUTO,),
                bgcolor="white",
                padding=20,
                margin=ft.margin.symmetric(horizontal=20),
                shadow=ft.BoxShadow(blur_radius=5,color="grey"),
                border_radius=15
            ),
            ]
        )
        return bitis

    def kutucuk_olustur(f):
        def sil_tiklandi(e):
            abonelik_listesi.controls.remove(kart)
            toplam_guncelle()
            verileri_kaydet()
            page.update()

        kart=ft.Container(
            content=ft.ListTile(
                title=ft.Text(f.hizmet, weight=ft.FontWeight.BOLD, color=RENK_KOYU),
                subtitle=ft.Column([ ft.Text(f"Son: {f.tarih}", size=12, color=RENK_GRI)], spacing=2),
                trailing=ft.Row([ft.Text(f"{f.fiyat:.2f} TL", weight=ft.FontWeight.BOLD, size=16, color=RENK_KOYU),
                                 ft.IconButton("delete", icon_color="red",on_click=sil_tiklandi) ], 
                alignment=ft.MainAxisAlignment.END, width=100), # 'alignment' parametresi kullanıldı
            ),
            bgcolor="white", 
            border_radius=12,
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(blur_radius=5, color="grey")
        )
        kart.data=f
        return kart

    # --- 3.5: Veri Yükleme Fonksiyonu ---
    
    def verileri_yükle():
        if not os.path.exists("abonelikler.json"): return
        try:
            with open("abonelikler.json", "r", encoding="utf-8") as dosya:
                veriler = json.load(dosya)
            for veri in veriler:
                nesne  = fatura(veri["fiyat"], veri["kategori"], veri["hizmet"], veri["paket"], veri["tarih"])
                kart=kutucuk_olustur(nesne)
                abonelik_listesi.controls.append(kart)
            toplam_guncelle()
            page.update()
        except: return

    # --- 3.6: Event Handlers (Olay Yönetimi) ---

    def Kategori_degisti(e):
        secilen = kategori_kutusu.value
        digital=(secilen == "Dijital Abonelikler")

        paket_kutusu.visible = digital
        manuel_fiyat_kutusu.visible = not digital

        if secilen:
            alt_secenekler = Secenekler[secilen]
            hizmet_kutusu.options = [ft.dropdown.Option(x) for x in alt_secenekler]
            hizmet_kutusu.disabled = False
            hizmet_kutusu.value = None
            paket_kutusu.value=None
            fiyat.value=""

        page.update()

    def hizmet_degisti(e):
        k, s = kategori_kutusu.value, hizmet_kutusu.value
        if s:
            if k == "Dijital Abonelikler":
                alt = Secenekler[k][s]
                paket_kutusu.options = [ft.dropdown.Option(x) for x in alt]
                paket_kutusu.disabled = False
                paket_kutusu.value = None
                fiyat.value=""
            else:
                manuel_fiyat_kutusu.disabled = False
                manuel_fiyat_kutusu.value = None
                fiyat.value=""
        page.update()

    secilen_tarih_kutusu = ft.Text(f"{suanki_gun}.{suanki_ay}.{suanki_yil}")
    def tarih_ayarla(e):
        if e.control.value:
            tarih_obj=e.control.value
            secilen_tarih_kutusu.value=tarih_obj.strftime('%d.%m.%y')
            secilen_tarih_kutusu.update()
    

    tarih_secici = ft.DatePicker(on_change=tarih_ayarla)
    page.overlay.append(tarih_secici)
    tarih_butonu = ft.ElevatedButton("takvimi aç",icon=ft.Icons.CALENDAR_MONTH,on_click=lambda _:page.open(tarih_secici))
    

    def paket_degisti(e):
            k, h = kategori_kutusu.value, hizmet_kutusu.value
            odenecek.visible=True
            if k and h and k=="Dijital Abonelikler":
                p=paket_kutusu.value
                fiyat.value = str(Secenekler[k][h][p][0])
            else:
                fiyat.value = manuel_fiyat_kutusu.value
            page.update()

    def button_tiklandi(e):
        if not fiyat.value: return
        
        try:
            s_fiyat = float(fiyat.value)
            if s_fiyat >= 0:
                x= fatura(s_fiyat,kategori_kutusu.value,hizmet_kutusu.value,paket_kutusu.value,tarih=secilen_tarih_kutusu.value)

                abonelik_listesi.controls.append(kutucuk_olustur(x))
                hizmet_kutusu.value, fiyat.value, manuel_fiyat_kutusu.value = "", "",""
                verileri_kaydet()
                page.update()
                toplam_guncelle() 
            else:
                page.open(ft.SnackBar(ft.Text("-'li değer girilemez", color="red", weight=ft.FontWeight.BOLD)))
        except:
                page.open(ft.SnackBar(ft.Text("Hatalı değer!", color="red", weight=ft.FontWeight.BOLD)))

    # --- 3.7: UI Bileşenleri (Dialog ve Formlar) ---

    manuel_fiyat_kutusu = ft.TextField(label="miktarı giriniz", visible=False, width=300,disabled=True, on_change=paket_degisti)
    hizmet_kutusu = ft.Dropdown(label="hizmet", width=300, disabled=True, on_change=hizmet_degisti)
    paket_kutusu = ft.Dropdown(label="paket",visible=False, width=300, disabled=True, on_change=paket_degisti)
    kategori_kutusu = ft.Dropdown(
        label="Kategori", width=300, 
        options=[ft.dropdown.Option(a) for a in Secenekler.keys()], on_change=Kategori_degisti
    )
    
    odenecek = ft.Container(
        content=fiyat,
        alignment=ft.alignment.center,
        padding=20,bgcolor=RENK_KOYU,
        margin=ft.margin.symmetric(horizontal=80),
        border_radius=50,
        visible=False
    )

    ekleme_penceresi = ft.AlertDialog(
        title=ft.Text("Yeni Abonelik Ekle"),
        content=ft.Column([kategori_kutusu, hizmet_kutusu,tarih_butonu,secilen_tarih_kutusu, paket_kutusu,manuel_fiyat_kutusu, odenecek], scroll=ft.ScrollMode.AUTO, height=200, tight=True),
        actions=[ft.ElevatedButton("Ekle", icon="add", on_click=button_tiklandi)],
        actions_alignment=ft.MainAxisAlignment.END,
        
    )

    # --- 3.8: Sayfa İskeleti ve Navigasyon ---
    
    content_area = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)
    
    header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("Hoş Geldin,", color=RENK_GRI, size=14),
                    ft.Text(KULLANICI_ADI, color=RENK_KOYU, size=24, weight=ft.FontWeight.BOLD)
                ]),
                ft.Container(
                    content=ft.CircleAvatar(content=ft.Icon("person"), bgcolor="#E9ECEF", color=RENK_KOYU),
                    ink=True, border_radius=50
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=20
        )
    
    total_card = ft.Container(
            content=ft.Column([
                ft.Text("Genel Toplam", color="white", size=14),
                toplam,
                ft.Text("Tüm faturaların toplamıdır.", color="white70", size=12)
            ]),
            bgcolor=RENK_KOYU, padding=20, border_radius=15, 
            margin=ft.margin.symmetric(horizontal=20),
            shadow=ft.BoxShadow(blur_radius=10, color="grey")
        )
    
    ana_sayfa=[
            header,
            total_card,
            ft.Container(ft.Text("Yaklaşan Ödemeler", size=18, weight=ft.FontWeight.BOLD, color=RENK_KOYU), padding=ft.padding.only(left=20, top=20, bottom=10)),
            ft.Container(
                content=abonelik_listesi,
                padding=ft.padding.symmetric(horizontal=20)
            )
        ]

    def sayfa_degisti(e):
        content_area.controls.clear()
        if e.control.selected_index == 0:
            content_area.controls.extend(ana_sayfa)
        elif e.control.selected_index == 1:
            grafik_nesnesi=[analiz_grafigi_olustur()]
            content_area.controls.extend(grafik_nesnesi)
        elif e.control.selected_index == 2:
            global degisim_ay,degisim_yil
            degisim_ay=suanki_ay
            degisim_yil=suanki_yil
            takvim_nesnesi=[takvim_olustur(suanki_yil,suanki_ay)]
            content_area.controls.extend(takvim_nesnesi)
        else:
            content_area.controls.extend([ft.Text("bu sayfa daha yapım aşamasında")])
        page.update()
        
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Ana Ekran"),
            ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS, label="Analiz"),
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH, label="Takvim"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Profil"),
        ],
        on_change=lambda e: sayfa_degisti(e),
        selected_index=0,
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=lambda _: page.open(ekleme_penceresi)
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    # --- 3.9: Başlatma (Initialization) ---
    content_area.controls.extend(ana_sayfa)
    page.add(content_area)
    verileri_yükle()

ft.app(target=main)