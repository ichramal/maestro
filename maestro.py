import telebot
import base64
import requests
import os
from io import BytesIO
from telebot import types
import json
from telebot import TeleBot, types
import urllib.parse
import random
import io
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import math 
import tempfile

# Bot Tokeninizi buraya girin
BOT_TOKEN = "7601889695:AAFtV-nUPioYApM2NPtioGhHVvMo_3VCess"
bot = telebot.TeleBot(BOT_TOKEN)




@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username if message.from_user.username else "kullanıcı"
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    channel_ids = [-1002326374972, -1002359512475]  # Kanal ID'lerini gerçek ID'lerle değiştirin
    current_hour = datetime.now().hour

    def is_user_member_all(user_id, channel_ids):
        for channel_id in channel_ids:
            if not is_user_member(user_id, channel_id):
                return False
        return True

    if not is_user_member_all(user_id, channel_ids):
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Kanal1", url="https://t.me/MaestroChecker")
        button2 = types.InlineKeyboardButton("Kanal2", url="https://t.me/iichramal")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, "⚠️ Lütfen Aşağıda Verilen Kanallara Katılıp Tekrardan Başlatınız.", reply_markup=markup)
        return

    if 5 <= current_hour < 12:
        greeting = "🌅 Günaydın"
    elif 12 <= current_hour < 15:
        greeting = "🌞 İyi öğlenler"
    elif 15 <= current_hour < 17:
        greeting = "☀️ İyi günler"
    elif 17 <= current_hour < 21:
        greeting = "🌆 İyi akşamlar"
    else:
        greeting = "🌙 İyi geceler"

    response = (
        f"{greeting}! @{username}\n\n"
        "💎 Sizi aramızda görmek bizi gerçekten mutlu ediyor! Bu platformda sorgularınızı yapabileceğiniz için "
        "heyecanlıyız ve size yardımcı olmaktan memnuniyet duyacağız.\n\n"
        "💡 Sorgularınız sınırsız ve ücretsiz! Herhangi bir sorun olduğunda, ekibimize veya topluluğumuza her zaman "
        "danışabilirsiniz.\n\n"
        "🏆 İlgili katılımcılarımıza hitap etmekten onur duyuyoruz.\n\n"
        "⚠ Dikkat! Zaman zaman sistem üzerinde bakım yapmamız gerekebilir. Bu yüzden bazı sorgular geçici olarak çalışmayabilir. Eğer bir sorgu yanıt vermiyorsa, lütfen daha sonra tekrar deneyin veya bize bildirin. Anlayışınız için teşekkür ederiz!"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("❄️ Sorgular", callback_data="commands"))
    markup.add(types.InlineKeyboardButton("🛠 Araçlar", callback_data="tools"))
    markup.add(types.InlineKeyboardButton("👑 Admin", callback_data="admin"))
    bot.send_message(message.chat.id, response, reply_markup=markup)
    
# ─── ANA MENÜ ───────────────────────────────────────────────
@bot.callback_query_handler(func=lambda call: call.data == "tools")
def show_tools(call):
    markup = types.InlineKeyboardMarkup(row_width=6)
    markup.row(
        types.InlineKeyboardButton("🌟 Resim", callback_data="resim"),
        types.InlineKeyboardButton("✉️  Email", callback_data="email"),
        types.InlineKeyboardButton("📝 Yaz", callback_data="yaz")
    )
    markup.add(
        types.InlineKeyboardButton("💲 Döviz", callback_data="doviz"),
        
    )
    
    

    markup.add(
        types.InlineKeyboardButton("💣 Sms Bomb", callback_data="sms"),
        types.InlineKeyboardButton("🌊 DDoS", callback_data="ddos")
    )


    markup.add(
        types.InlineKeyboardButton("🚪Port", callback_data="port")
    )

    markup.add(
        types.InlineKeyboardButton('💳 cc checker', callback_data='cc'),
        types.InlineKeyboardButton('🔲 qr', callback_data='qr'),
        types.InlineKeyboardButton('🏧 Bin', callback_data='bin'),
    )

    

    markup.add(
        types.InlineKeyboardButton('🎉 DC Sunucu', callback_data='dcsunucu'),
        types.InlineKeyboardButton('🎁 DC Gen', callback_data='dcgen'),

    )



    markup.add(

        types.InlineKeyboardButton('💬 Telegram', callback_data='telegram'),
        types.InlineKeyboardButton('🎮 DC Sorgu', callback_data='dcsorgu'),
        types.InlineKeyboardButton('🌐 Ip', callback_data='ip')
    )
    

    

    markup.add(
        types.InlineKeyboardButton('🔄 Ping', callback_data='ping')

    )



    markup.add(
        types.InlineKeyboardButton('📷 Live Shot', callback_data='liveshot'),
        types.InlineKeyboardButton('🌎 DNS', callback_data='dns'),
        types.InlineKeyboardButton('📃 SSL', callback_data='ssl')
    )

    markup.add(
        types.InlineKeyboardButton('📊 Log', callback_data='log'),
    )


    # Geri ve Diğer butonlarını ekliyoruz
    markup.add(
        types.InlineKeyboardButton("↩️ Geri", callback_data="back_to_main")
    )
    
    bot.edit_message_text(
        "ㅤㅤㅤ𝐌 𝐀 𝐄 𝐒 𝐓 𝐑 𝐎",  # Menü metni
        chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        reply_markup=markup
    )



@bot.callback_query_handler(func=lambda call: call.data in ["resim", "yaz", "doviz", "sms", "ddos", "email", "bin", "cc", "dcsorgu", "dcsunucu", "telegram", "ip"
                                                            , "qr", "port", "liveshot", "ssl", "log", "dns", "ping", "dcgen"])
def handle_tools_query(call):
    # Varsayılan text
    new_text = "Seçtiğiniz seçenek bulunamadı."

    if call.data == "resim":
        new_text = "/resim (yazı) yazarak resim aratın."
    elif call.data == "yaz":
        new_text = "/yaz (yazı) yazarak kağıda yazı yaz."
    elif call.data == "sms":
        new_text = "/sms (num) yazarak sms bomb kullan"
    elif call.data == "DDoS":
        new_text = "/ddos (Site) yazarak DDoS kullan"
    elif call.data == "doviz":
        new_text = "/doviz (kur) yazarak anlık değere bak."
    elif call.data == 'email':
        new_text = "/email (Email adresi) yazarak e-posta bilgilerini sorgulayabilirsiniz."
    elif call.data == 'cc':
        new_text = "/check (kart numarası) yazarak checkle."
    elif call.data == 'telegram':
        new_text = "/telegram (Kullanıcı adı) yazarak Telegram kullanıcı bilgilerini alabilirsiniz."
    elif call.data == 'ip':
        new_text = "/ip (IP adresi) yazarak IP adresinden bilgi alabilirsiniz."
    elif call.data == 'dcsunucu':
        new_text = "/dcsunucu (invite) yazarak sunucudan bilgi alabilirsiniz."
    elif call.data == 'dcsorgu':
        new_text = "/dcsorgu (id) yazarak kullanıcıdan bilgi alabilirsiniz."
    elif call.data == 'bin':
        new_text = "/bin (bin) yazarak binden bilgi alabilirsiniz."
    elif call.data == 'port':
        new_text = "/port (url) yazarak portları alabilirsiniz."
    elif call.data == 'liveshot':
        new_text = "/liveshot (url) yazarak liveshot alabilirsiniz."
    elif call.data == 'ssl':
        new_text = "/ssl (url) yazarak ssl tls sertifika alabilirsiniz."
    elif call.data == 'log':
        new_text = "/log (url) yazarak loglar alabilirsiniz. günde sadece 3 kez hakkınız"
    elif call.data == 'dns':
        new_text = "/dns (url) yazarak dns bilgilerini alabilirsiniz"
    elif call.data == 'ping':
        new_text = "/ping (url) yazarak ms testi alabilirsiniz"
    elif call.data == 'qr':
        new_text = "/qr (text) yazarak qr kod alabilirsiniz"
    elif call.data == 'dcgen':
        new_text = "/dcgen yazarak nitro gen kullana bilirsiniz,günlük 3 kez ücretsiz"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("↩️ Geri", callback_data="tools"))

    # Mesajı güncelle
    bot.edit_message_text(
        new_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )





@bot.callback_query_handler(func=lambda call: call.data == "admin")
def show_admin(call):
    admin_text = "👑 Admin: @ichramall"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("↩️ Geri", callback_data="back_to_main"))
    bot.edit_message_text(
        admin_text, 
        chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        reply_markup=markup
    )













# ─── KOMUTLAR MENÜSÜ ───────────────────────────────────────────────
@bot.callback_query_handler(func=lambda call: call.data == "commands")
def show_commands(call):
    markup = types.InlineKeyboardMarkup()
    
    # Üst kısım: 2 buton
    markup.add(
        types.InlineKeyboardButton('🇹🇷 Ad soyad', callback_data='sorgu'),
        types.InlineKeyboardButton('⚡ TC Pro', callback_data='tc')
    )

    # 3 butonluk satır
    markup.add(
        types.InlineKeyboardButton('🏠 Adres', callback_data='adres'),
        types.InlineKeyboardButton('🔎 Tum Sokak', callback_data='sokaktum'),
        types.InlineKeyboardButton('📱 Tcgsm', callback_data='tcgsm')
    )


    

    # 3 butonluk satır
    markup.add(
        types.InlineKeyboardButton('👪 Anne Baba', callback_data='annebaba'),
        types.InlineKeyboardButton('🏡 Hane', callback_data='hane')
    )




 # 3 butonluk satır
    markup.add(
        types.InlineKeyboardButton('🏘 Apartman', callback_data='apartman')
    )




    # 3 butonluk satır
    markup.add(
        types.InlineKeyboardButton('📲 Gsm tc', callback_data='gsmtc'),
        types.InlineKeyboardButton('💼 Gsm detay', callback_data='gsmdetay'),
    )




    markup.add(
       types.InlineKeyboardButton('👔 İşyeri Ark.', callback_data='isyeriarkadasi'),
       types.InlineKeyboardButton('⏳ Hayat Hikayesi.', callback_data='hikaye'),
       types.InlineKeyboardButton('🗃️ Sgkyetkili', callback_data='sgkyetkili')

    )

    

    markup.add(
       types.InlineKeyboardButton('🏢 İş Yeri', callback_data='isyeri')

    )

    markup.add(
       types.InlineKeyboardButton('📜 Tapu', callback_data='tapu'),
       types.InlineKeyboardButton('🗺️ Parsel', callback_data='parsel')

    )






    markup.add(
       types.InlineKeyboardButton('🎭 Kuzen', callback_data='kuzen'), 
       types.InlineKeyboardButton('🌳 Sulale', callback_data='sulale'),
       types.InlineKeyboardButton('👨‍👩‍👧 Aile', callback_data='aile')

    )



    # 5 butonluk satır
    markup.add(
        types.InlineKeyboardButton('🛠️ Operator', callback_data='operator'),
        types.InlineKeyboardButton('⚙️ OperatorPro', callback_data='operatorpro')
    )

    # Alttaki satır: 3 buton
    markup.add(
        types.InlineKeyboardButton('🔥 SorguPro', callback_data='sorgupro'), 

    )

    




    # Komutlar menüsünde ana menüye dönüş butonu (opsiyonel)
    markup.add(types.InlineKeyboardButton("↩️ Geri", callback_data="back_to_main"))
    bot.edit_message_text(
        "ㅤㅤㅤ𝐌 𝐀 𝐄 𝐒 𝐓 𝐑 𝐎", 
        chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in [
    "sorgu", "tc", "adres", "sokaktum", "tcgsm", "gsmtc", "gsmdetay",
    "aile", "annebaba", "cocuk", "bin", "hane", "sulale", "sgkyetkili",
    "operator", "email", "cc", "telegram", "ip", "tapu", "parsel", "operatorpro",
    "kuzen", "isyeriarkadasi", "sorgupro", "kizlik", "hikaye", "apartman", "parsel", "operatorpro",
    "premiumsorgu","ttnet","universite","burc","isyeri"
])
def handle_command_help(call):
    help_text = "Bu komut hakkında bilgi bulunamadı."  # Varsayılan mesaj ekledik

    if call.data == 'sorgu':
        help_text = "/sorgu (Ad Soyad/il ilce) yazarak sorgula."
    elif call.data == 'tc':
        help_text = "/tc (TC numarası) yazarak sorgula."
    elif call.data == 'sorgupro':
        help_text = "/sorgupro (Ad Soyad/il ilce) yazarak sorgula."
    elif call.data == 'adres':
        help_text = "/adres (TC) yazarak adres sorgula."
    elif call.data == 'sokaktum':
        help_text = "/sokaktum (TC) yazarak sokak sakinlerini sorgula."
    elif call.data == 'tcgsm':
        help_text = "/tcgsm (TC) yazarak TC numarasına ait GSM sorgula."
    elif call.data == 'gsmtc':
        help_text = "/gsmtc (GSM) yazarak GSM numarasına ait TC sorgula."
    elif call.data == 'gsmdetay':
        help_text = "/gsmdetay (GSM) yazarak GSM numarasından detaylı bilgi alabilirsiniz."
    elif call.data == 'aile':
        help_text = "/aile (TC) yazarak tüm aile üyelerini sorgulayabilirsiniz."
    elif call.data == 'annebaba':
        help_text = "/annebaba (TC) yazarak kişinin anne baba ile ilgili bilgi alabilirsiniz."
    elif call.data == 'cocuk':
        help_text = "/cocuk (TC) yazarak kişinin çocuğuyla ilgili bilgi alabilirsiniz."
    elif call.data == 'hane':
        help_text = "/hane (TC) yazarak hane hakkında bilgi alabilirsiniz."
    elif call.data == 'sulale':
        help_text = "/sulale (TC) yazarak kişinin tüm sülalesini sorgulayabilirsiniz."
    elif call.data == 'sgkyetkili':
        help_text = "/sgkyetkili (TC) yazarak iş yeri yetkili bilgilerini sorgulayabilirsiniz."
    elif call.data == 'operator':
        help_text = "/operator (GSM numarası) yazarak operatör bilgilerini alabilirsiniz."
    elif call.data == 'apartman':
        help_text = "/apartman (TC) yazarak apartman bilgilerini alabilirsiniz."
    elif call.data == 'hikaye':
        help_text = "/hikaye (TC) yazarak hayat hikayesini alabilirsiniz."
    elif call.data == 'kizlik':
        help_text = "/kizlik (TC) yazarak kızlık soyadını alabilirsiniz."
    elif call.data == 'isyeriarkadasi':
        help_text = "/isyeriarkadasi (TC) yazarak işyeri arkadaşlarını alabilirsiniz."
    elif call.data == 'parsel':
        help_text = "/parsel (bilgi) yazarak parsel detaylarını alabilirsiniz."
    elif call.data == 'kuzen':
        help_text = "/kuzen (tc) yazarak kuzenlerini sorgulaya alabilirsiniz."
    elif call.data == 'operatorpro':
        help_text = "/operatorpro (GSM numarası) yazarak operatör bilgilerini alabilirsiniz."
    elif call.data == 'premiumsorgu':
        help_text = "/premiumsorgu (TC) yazarak premium sorgu yap."
    elif call.data == 'ttnet':
        help_text = "/ttnet (email)/(Adsoyad) yazarak ttnet sorgu yap."
    elif call.data == 'universite':
        help_text = "/universite (TC) yazarak universite sorgu yap."
    elif call.data == 'burc':
        help_text = "/burc (TC) yazarak burcunu sorgu yap."
    elif call.data == 'isyeri':
        new_text = "/isyeri işyeri bilgilerini alabilirsiniz"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("↩️ Geri", callback_data="commands"))

    bot.edit_message_text(
        help_text, 
        chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        reply_markup=markup
    )


# ─── ANA MENÜYE DÖNÜŞ ───────────────────────────────────────────────
@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=2)  # 2 buton üst üste
    markup.add(
        types.InlineKeyboardButton("❄️ Sorgular", callback_data="commands"),
        types.InlineKeyboardButton("🛠 Araçlar", callback_data="tools"),
        types.InlineKeyboardButton("👑 Admin", callback_data="admin")
    )

    bot.edit_message_text(
        "ㅤㅤㅤ𝐌 𝐀 𝐄 𝐒 𝐓 𝐑 𝐎  ", 
        chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        reply_markup=markup
    )





def is_user_member(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(str(e))
        return False






@bot.message_handler(commands=['annebaba'])
def anne_baba_sorgu(message):
    try:
        chat_id = message.chat.id
        
        # Komutun doğru yazıldığından emin olun
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /annebaba 12345678901")
            return
        
        tc_number = message.text.split()[1]  # TC kimlik numarası komuttan alınır

        url = f"https://siberizim.online/esrarkes/annebabasorgu/api.php?tc={tc_number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        # API yanıtını kontrol et
        if response.status_code != 200:
            bot.reply_to(message, "API'ye bağlanırken bir sorun oluştu.")
            return

        # API yanıtını JSON'a çevir
        try:
            data = response.json()
        except ValueError:
            bot.reply_to(message, "Geçerli bir yanıt alınamadı.")
            return
        
        # Cevapta veri var mı kontrol et
        if "data" in data and len(data["data"]) > 1:
            anne_baba_data = data["data"][1]  # Anne ve Baba bilgisi

            anne_baba_message = f"""
╭━━━━━━━━━━━━━━
┃ 👩‍🦰👨‍🦰 **Anne ve Baba Bilgileri**:
┃ ➥ **Anne Adı:** {anne_baba_data.get("ANNEADI", "Bilinmiyor")}
┃ ➥ **Anne TC:** {anne_baba_data.get("ANNETC", "Bilinmiyor")}
┃ ➥ **Baba Adı:** {anne_baba_data.get("BABAADI", "Bilinmiyor")}
┃ ➥ **Baba TC:** {anne_baba_data.get("BABATC", "Bilinmiyor")}
╰━━━━━━━━━━━━━━
"""

            bot.send_message(chat_id, anne_baba_message, parse_mode="Markdown")
        else:
            bot.reply_to(message, "Bu TC numarasına ait anne ve baba bilgisi bulunamadı.")
    
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /annebaba 12345678901")
    
    except Exception as e:
        print(f"Anne ve Baba sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")




@bot.message_handler(commands=['aile'])
def adress_sorgu(message):
    try:
        chat_id = message.chat.id
        tc_number = message.text.split()[1]  # TC kimlik numarası komuttan alınır

        # User-Agent başlığını ekliyoruz
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Yeni API URL'si
        url = f"https://api.ondex.uk/ondexapi/ailesorgu.php?tc={tc_number}"
        response = requests.get(url, headers=headers)  # headers ile istek gönderiyoruz
        data = response.json()

        if "Veri" in data:
            adres_list = []
            for birey in data["Veri"]:  # Liste içinde döngüyle gez
                adres_list.append(f"""
╭━━━━━━━━━━━━━━
┃➥ Yakinlik: {birey.get("Yakinlik", "Bilinmiyor")}
┃➥ TC: {birey.get("TCKN", "Bilinmiyor")}
┃➥ Ad: {birey.get("Adi", "Bilinmiyor")}
┃➥ Soyad: {birey.get("Soyadi", "Bilinmiyor")}
┃➥ Doğum Tarihi: {birey.get("DogumTarihi", "Bilinmiyor")}
╰━━━━━━━━━━━━━━
""")

            adres_message = "\n".join(adres_list)

            # Eğer mesaj 4000 karakterden uzunsa, TXT dosyası olarak gönder
            if len(adres_message) > 4000:
                with open("aile_sorgu_sonucu.txt", "w", encoding="utf-8") as file:
                    file.write(adres_message)
                
                with open("aile_sorgu_sonucu.txt", "rb") as file:
                    bot.send_document(chat_id, file, caption="Hazır.")
            else:
                bot.reply_to(message, adres_message)

        else:
            bot.reply_to(message, "Bu TC numarasına ait aile bilgisi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /aile 12345678901")
    except Exception as e:
        print(f"Aile sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")



# /adres komutu
@bot.message_handler(commands=['adres'])
def adress_sorgu(message):
    try:
        chat_id = message.chat.id
        tc_number = message.text.split()[1]  # TC kimlik numarası komuttan alınır

        # Yeni API URL'si
        url = f"https://api.ondex.uk/ondexapi/adressorgu.php?tc={tc_number}"

        # User-Agent başlığı ekle
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # API'ye istek gönder
        response = requests.get(url, headers=headers)

        # Yanıtın içeriğini kontrol edelim
        print("API Yanıtı:", response.text)  # Yanıtın içeriğini kontrol etmek için

        # JSON'a dönüştürme işlemi
        try:
            data = response.json()
        except ValueError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        if "Veri" in data:
            adres_data = data["Veri"]

            adres_message = f"""
╭━━━━━━━━━━━━━━
┃➥ TC: {adres_data["TCKN"]}
┃➥ Adı Soyadı: {adres_data["AdiSoyadi"]}
┃➥ VKN: {adres_data["VKN"]}
┃➥ Adres: {adres_data["Adres"]}
╰━━━━━━━━━━━━━━
"""
            bot.reply_to(message, adres_message)
        else:
            bot.reply_to(message, "Bu TC numarasına ait adres bilgisi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /adres 12345678901")
    except Exception as e:
        print(f"Adres sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")






# /gsmdetay komutu (Yeni API'ye göre güncellendi)
@bot.message_handler(commands=['gsmdetay'])
def gsmdetay_sorgu(message):
    try:
        chat_id = message.chat.id
        gsm_number = message.text.split()[1]  # GSM numarası komuttan alınır

        url = f"https://api.ondex.uk/ondexapi/gsmtcprosorgu.php?gsm={gsm_number}"

        # User-Agent başlığı ekle
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        # Yanıtın ne olduğunu kontrol edelim
        print("API Yanıtı:", response.text)  # Yanıtın içeriğini görmek için

        # JSON'a dönüştürme işlemi
        try:
            data = response.json()
        except ValueError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        if "Kisi" in data and len(data["Kisi"]) > 0:
            kisi = data["Kisi"][0]  # API dizinin ilk elemanında kişi bilgisi var

            gsmdetay_message = f"""
╭━━━━━━━━━━━━━━━━━━━━━━
┃➥ TC: {kisi["TCKN"]}
┃➥ Ad: {kisi["Adi"]}
┃➥ Soyad: {kisi["Soyadi"]}
┃➥ Doğum Tarihi: {kisi["DogumTarihi"]}
┃➥ Anne Adı: {kisi["AnneAdi"]} ({kisi["AnneTCKN"]})
┃➥ Baba Adı: {kisi["BabaAdi"]} ({kisi["BabaTCKN"]})
┃➥ Nüfus İl/İlçe: {kisi["NufusIl"]} / {kisi["NufusIlce"]}
┃➥ Uyruk: {kisi["Uyruk"]}
╰━━━━━━━━━━━━━━━━━━━━━━
"""
            bot.reply_to(message, gsmdetay_message)
        else:
            bot.reply_to(message, "Bu GSM numarasına ait bilgi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /gsmdetay 5393374789")
    except Exception as e:
        print(f"GSM detay sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")




# /gsmtc komutu
@bot.message_handler(commands=['gsmtc'])
def gsmtc_sorgu(message):
    try:
        chat_id = message.chat.id
        gsm_number = message.text.split()[1]  # GSM numarasını komuttan alın

        url = f"https://api.ondex.uk/ondexapi/gsmtcprosorgu.php?gsm={gsm_number}"

        # User-Agent başlığı ekleyin
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        # Yanıtın ne olduğunu kontrol edelim
        print("API Yanıtı:", response.text)

        # JSON'a dönüştürme işlemi
        try:
            data = response.json()
        except ValueError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        if "Kisi" in data:
            kisi = data["Kisi"][0]

            result_text = f"""\
╭━━━━━━━━━━━━━━
┃➥ Adı: {kisi['Adi']}
┃➥ Soyadı: {kisi['Soyadi']}
┃➥ TC: {kisi['TCKN']}
┃➥ Doğum Tarihi: {kisi['DogumTarihi']}
┃➥ Anne Adı: {kisi['AnneAdi']} ({kisi['AnneTCKN']})
┃➥ Baba Adı: {kisi['BabaAdi']} ({kisi['BabaTCKN']})
┃➥ Nüfus İl/İlçe: {kisi['NufusIl']} / {kisi['NufusIlce']}
┃➥ Uyruk: {kisi['Uyruk']}
╰━━━━━━━━━━━━━━"""

            bot.reply_to(message, result_text)
        else:
            bot.reply_to(message, "Bu GSM numarasına ait bilgiler bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /gsmtc <gsm_numarası>")
    except Exception as e:
        print(f"GSM sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")




        
        
     # /tc komutu
@bot.message_handler(commands=['tc'])
def tc_sorgu(message):
    try:
        chat_id = message.chat.id
        tc_number = message.text.split()[1]  # TC numarası komuttan alınır

        url = f"https://api.ondex.uk/ondexapi/tcsorgu.php?tc={tc_number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        # API yanıtını terminale yazdır (hata tespiti için)
        print("API Yanıtı:", response.text)

        # Yanıt kontrolü (boş veya geçersiz ise hata önler)
        if response.status_code != 200 or not response.text.strip():
            bot.reply_to(message, "API'den boş yanıt alındı, tekrar dene!")
            return
        
        try:
            data = response.json()
        except Exception as e:
            print("JSON dönüşüm hatası:", str(e))
            bot.reply_to(message, "API'den geçersiz veri alındı.")
            return

        if "Veri" in data:
            tc_data = data["Veri"]

            tc_message = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃➥ TC: {tc_data.get("TCKN", "Bilinmiyor")}
┃➥ Ad: {tc_data.get("Adi", "Bilinmiyor")}
┃➥ Soyad: {tc_data.get("Soyadi", "Bilinmiyor")}
┃➥ Cinsiyet: {tc_data.get("Cinsiyet", "Bilinmiyor")}
┃➥ Doğum Tarihi: {tc_data.get("DogumTarihi", "Bilinmiyor")}
┃➥ Anne Adı: {tc_data.get("AnneAdi", "Bilinmiyor")}
┃➥ Anne TC: {tc_data.get("AnneTCKN", "Bilinmiyor")}
┃➥ Baba Adı: {tc_data.get("BabaAdi", "Bilinmiyor")}
┃➥ Baba TC: {tc_data.get("BabaTCKN", "Bilinmiyor")}
┃➥ Memleket İl: {tc_data.get("MemleketIl", "Bilinmiyor")}
┃➥ Memleket İlçe: {tc_data.get("MemleketIlce", "Bilinmiyor")}
╰━━━━━━━━━━━━━━━━━━━━━
"""
            bot.reply_to(message, tc_message)
        else:
            bot.reply_to(message, "Bu TC numarasına ait bilgi bulunamadı.")
    
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /tc 12345678901")
    except requests.exceptions.RequestException as e:
        print(f"API bağlantı hatası: {str(e)}")
        bot.reply_to(message, "API ile bağlantı kurulamadı. Lütfen daha sonra tekrar deneyin.")
    except Exception as e:
        print(f"Genel hata: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")





import requests
import os

@bot.message_handler(commands=['sorgupro'])
def kimlik_sorgu(message):
    try:
        chat_id = message.chat.id
        parameters = ' '.join(message.text.split()[1:]).split()
        
        if len(parameters) < 2:
            bot.reply_to(message, "Geçersiz komut kullanımı. Örnek: /sorgupro Yezda Selvi Bursa Osmangazi")
            return
        
        query = {
            'ad': parameters[0],  # Ad
            'soyad': parameters[1]  # Soyad
        }
        
        # İl varsa ekliyoruz
        if len(parameters) > 2:
            query['il'] = parameters[2]  # İl
            # İlçe varsa ekliyoruz, ama ilçe zorunlu değil
            if len(parameters) > 3:
                query['ilce'] = parameters[3]

        # URL'yi oluşturuyoruz
        url = f"https://api.ondex.uk/ondexapi/adsoyadprosorgu.php?ad={query['ad']}&soyad={query['soyad']}"
        if 'il' in query:
            url += f"&il={query['il']}"
        if 'ilce' in query:
            url += f"&ilce={query['ilce']}"

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if "Veri" in data and isinstance(data["Veri"], list) and len(data["Veri"]) > 0:
            person_info = "╭━━━━━━━━━━━━━━━━━━━━━"
            for person in data["Veri"]:
                person_info += f"""
┃➥ TC: {person.get("TCKN", "Bilinmiyor")}
┃➥ Ad: {person.get("Adi", "Bilinmiyor")}
┃➥ Soyad: {person.get("Soyadi", "Bilinmiyor")}
┃➥ Doğum Tarihi: {person.get("DogumTarihi", "Bilinmiyor")}
┃➥ Anne Adı: {person.get("AnneAdi", "Bilinmiyor")}
┃➥ Anne TC: {person.get("AnneTCKN", "Bilinmiyor")}
┃➥ Baba Adı: {person.get("BabaAdi", "Bilinmiyor")}
┃➥ Baba TC: {person.get("BabaTCKN", "Bilinmiyor")}
┃➥ Nüfus İl: {person.get("NufusIl", "Bilinmiyor")}
┃➥ Nüfus İlçe: {person.get("NufusIlce", "Bilinmiyor")}
┃➥ Uyruk: {person.get("Uyruk", "Bilinmiyor")}
┃➥ Adres: {person.get("Adres", "Bilinmiyor")}
"""
            person_info += "╰━━━━━━━━━━━━━━━━━━━━━"

            if len(person_info) > 4000:
                file_name = f"data_{chat_id}.txt"
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(person_info.strip())
                with open(file_name, 'rb') as file:
                    bot.send_document(chat_id, file)
                os.remove(file_name)
            else:
                while len(person_info) > 4000:
                    bot.send_message(chat_id, person_info[:4000])
                    person_info = person_info[4000:]
                if len(person_info) > 0:
                    bot.send_message(chat_id, person_info.strip())
        else:
            bot.reply_to(message, "Bu bilgilerle ilgili herhangi bir sonuç bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")

 




@bot.message_handler(commands=['tapu'])
def tapu_sorgu(message):
    try:
        chat_id = message.chat.id
        parameters = message.text.split()
        
        if len(parameters) < 2:
            bot.reply_to(message, "Geçersiz komut kullanımı. Örnek: /tapu 12345678901")
            return
        
        tc = parameters[1]
        url = f"https://api.ondex.uk/ondexapi/tapusorgu.php?tc={tc}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if "Veri" in data and data["Veri"]:
            tapu_info = "╭━━━━━━━━━━━━━━━━━━━━━"
            
            for record in data["Veri"]:
                tapu_info += f"""
┃➥ Ad: {record.get("Name", "Bilinmiyor")}
┃➥ Soyad: {record.get("Surname", "Bilinmiyor")}
┃➥ Baba Adı: {record.get("BabaAdi", "Bilinmiyor")}
┃➥ TC: {record.get("Identify", "Bilinmiyor")}
┃➥ İl: {record.get("İlBilgisi", "Bilinmiyor")}
┃➥ İlçe: {record.get("İlceBilgisi", "Bilinmiyor")}
┃➥ Mahalle: {record.get("MahalleBilgisi", "Bilinmiyor")}
┃➥ Zemin Tipi: {record.get("ZeminTipBilgisi", "Bilinmiyor")}
┃➥ Ada: {record.get("AdaBilgisi", "Bilinmiyor")}
┃➥ Parsel: {record.get("ParselBilgisi", "Bilinmiyor")}
┃➥ Yüzölçümü: {record.get("YuzolcumBilgisi", "Bilinmiyor")} m²
┃➥ Ana Taşınmaz: {record.get("AnaTasinmazNitelik", "Bilinmiyor")}
┃➥ Bağımsız Bölüm No: {record.get("BagimsizBolumNo", "Bilinmiyor")}
┃➥ Hisse Payı: {record.get("HissePay", "Bilinmiyor")}/{record.get("HissePayda", "Bilinmiyor")}
┃➥ Edinme Sebebi: {record.get("EdinmeSebebi", "Bilinmiyor")}
┃➥ Tapu Tarihi: {record.get("TapuDate", "Bilinmiyor")}
┃➥ Yevmiye: {record.get("Yevmiye", "Bilinmiyor")}
"""
            
            tapu_info += "╰━━━━━━━━━━━━━━━━━━━━━"
            
            if len(tapu_info) > 4000:
                file_name = f"tapu_{chat_id}.txt"
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(tapu_info.strip())
                with open(file_name, 'rb') as file:
                    bot.send_document(chat_id, file)
                os.remove(file_name)
            else:
                while len(tapu_info) > 4000:
                    bot.send_message(chat_id, tapu_info[:4000])
                    tapu_info = tapu_info[4000:]
                if len(tapu_info) > 0:
                    bot.send_message(chat_id, tapu_info.strip())
        else:
            bot.reply_to(message, "Bu TC numarası için tapu bilgisi bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")








@bot.message_handler(commands=['hane'])
def gsmdetay_sorgu(message):
    try:
        chat_id = message.chat.id
        args = message.text.split()

        if len(args) < 2:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /hane 14570512634")
            return

        tc_number = args[1]
        url = f"https://api.ondex.uk/ondexapi/hanesorgu.php?tc={tc_number}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        print("API Yanıtı:", response.text)  # Yanıtı kontrol için ekrana yazdır

        try:
            data = response.json()  # JSON formatına çevir
        except json.JSONDecodeError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        # Eğer API "error" mesajı döndürüyorsa
        if "error" in data and data["error"] == "Sonuç bulunamadı":
            bot.reply_to(message, "Bu TC numarasına ait detaylı bilgi bulunamadı.")
            return

        # Kişi bilgileri "Veri" anahtarında
        kisi_listesi = data.get("Veri", [])

        if not kisi_listesi:
            bot.reply_to(message, "Bu TC numarasına ait detaylı bilgi bulunamadı.")
            return

        response_message = ""
        for member in kisi_listesi:
            response_message += f"""
╭━━━━━━━━━━━━━━━━━━━━━━
┃➥ TC: {member.get("KimlikNumarasi", "Yok")}
┃➥ Ad Soyad: {member.get("AdiSoyadi", "Yok")}
┃➥ Vergi Numarası: {member.get("VergiNumarasi", "Yok")}
┃➥ İkametgah: {member.get("Ikametgah", "Yok")}
╰━━━━━━━━━━━━━━━━━━━━━━
"""

        # Eğer mesaj 4000 karakterden kısa ise direkt gönder
        if len(response_message) <= 4000:
            bot.reply_to(message, response_message)
        else:
            file_name = f"hane_{chat_id}.txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(response_message)

            with open(file_name, 'rb') as f:
                bot.send_document(chat_id, f)

            os.remove(file_name)

    except Exception as e:
        print(f"Detay sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu, tekrar deneyin.")



# /sulale komutu
@bot.message_handler(commands=['sulale'])
def sulale_detay_sorgu(message):
    try:
        chat_id = message.chat.id
        tc_number = message.text.split()[1]  # TC numarası komuttan alınır

        url = f"https://api.ondex.uk/ondexapi/sulalesorgu.php?tc={tc_number}"

        # User-Agent başlığı ekle
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        # Yanıtın ne olduğunu kontrol edelim
        print("API Yanıtı:", response.text)  # Yanıtın içeriğini kontrol etmek için

        # JSON'a dönüştürme işlemi
        try:
            data = response.json()
        except ValueError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        if data.get("Veri"):  # Eğer Veri listesi varsa
            response_message = ""
            for member in data["Veri"]:
                response_message += f"""
╭━━━━━━━━━━━━━━━━━━━━━━
┃➥ Yakınlık: {member["Yakinlik"]}
┃➥ TC: {member["TCKN"]}
┃➥ Ad: {member["Adi"]}
┃➥ Soyad: {member["Soyadi"]}
┃➥ Doğum Tarihi: {member["DogumTarihi"]}
╰━━━━━━━━━━━━━━━━━━━━━━
"""

            # Eğer cevap 4000 karakterden kısa ise DM mesajı ile gönder
            if len(response_message) <= 4000:
                bot.reply_to(message, response_message)
            else:
                # Eğer cevap 4000 karakterden uzunsa .txt dosyasına kaydet
                file_name = f"data_{chat_id}.txt"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(response_message)

                # Dosyayı kullanıcıya gönder
                with open(file_name, 'rb') as f:
                    bot.send_document(chat_id, f)

                # Dosya silindi (isteğe bağlı)
                os.remove(file_name)
        else:
            bot.reply_to(message, "Bu TC numarasına ait sülale bilgisi bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /sulale 14570512634")
    except Exception as e:
        print(f"Sülale sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")




# /telegram komutu
@bot.message_handler(commands=['telegram'])
def telegram_sorgu(message):
    try:
        # API'ye username ile istek atıyoruz
        username = message.text.split()[1]  # Kullanıcı adı komuttan alınır
        url = f"https://api.ondex.uk/ondexapi/telegramsorgu.php?username={username}"

        # User-Agent başlığı ekle
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        # Kullanıcı bilgilerini alıyoruz
        kullanici_adi = data.get("KullaniciAdi", "Bilinmiyor")
        biografi = data.get("Biografi", "Bilinmiyor")

        # Kullanıcı bilgilerini içeren mesajı oluşturuyoruz
        response_message = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━
┃➥ Kullanıcı Adı: {kullanici_adi}
┃➥ Biografi: {biografi}
╰━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Mesajı kullanıcıya gönderiyoruz
        bot.reply_to(message, response_message)

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /telegram @kullaniciadi")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")





@bot.message_handler(commands=['hava2'])
def get_weather(message):
    try:
        # Hava durumu API'sine istek atıyoruz
        response = requests.get(
            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/buzovna/today?unitGroup=metric&key=4L79NNF3DNJBTQWVTYZ5DPGS8&contentType=json"
        )
        
        if response.status_code == 200:
            # API'den dönen yanıtı JSON formatında alıyoruz
            weather_data = response.json()
            
            # Gerekli verileri alıyoruz
            current_conditions = weather_data.get("currentConditions", {})
            days = weather_data.get("days", [])
            
            if current_conditions and days:
                # Günlük hava durumu bilgilerini biçimlendiriyoruz
                day = days[0]
                message_text = (
                    f"🌤️ Hava Durumu Bilgisi Baku 🌤️\n"
                    f"• Tarih: {current_conditions.get('datetime')}\n"
                    f"• Sıcaklık:{current_conditions.get('temp')}°C\n"
                    f"• Hissedilen Sıcaklık: {current_conditions.get('feelslike')}°C\n"
                    f"• Max Sıcaklık: {day.get('tempmax')}°C\n"
                    f"• Min Sıcaklık:{day.get('tempmin')}°C\n"
                    f"• Durum: {current_conditions.get('conditions')}\n"
                    f"• Rüzgar Hızı: {current_conditions.get('windspeed')} km/h\n"
                )
                # Kullanıcıya hava durumu mesajını gönderiyoruz
                bot.send_message(message.chat.id, message_text)
            else:
                bot.send_message(message.chat.id, "Hava durumu bilgisi alınamadı.")
        else:
            bot.send_message(message.chat.id, f"API hatası: {response.status_code}")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"Bir hata oluştu: {e}")









# Komutları işleyecek fonksiyon
@bot.message_handler(commands=['usd', 'azn','try','brl','eur'])
def get_exchange_rate(message):
    try:
        # Kullanıcının yazdığı komutu alıyoruz (usd, azn)
        command = message.text.strip('/')

        # API URL'sini oluşturuyoruz
        api_url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{command}.json"
        
        # Döviz kuru API'sine istek atıyoruz
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # API'den dönen yanıtı JSON formatında alıyoruz
            data = response.json()

            # Kullanıcının seçtiği para biriminin diğer para birimlerine göre değerlerini alıyoruz
            if data:
                message_text = f"💰 {command.upper()} Döviz Kuru Bilgisi 💰\n"
                
                # Para birimlerine göre değerler
                if command == 'usd':
                    required_currencies = ['azn', 'try', 'brl', 'eur']
                elif command == 'azn':
                    required_currencies = ['usd', 'eur', 'try', 'brl']
                elif command == 'try':
                    required_currencies = ['usd', 'eur', 'try', 'brl']
                elif command == 'brl':
                    required_currencies = ['usd', 'eur', 'try', 'azn']
                elif command == 'eur':
                    required_currencies = ['usd', 'azn', 'try', 'brl']
                for currency in required_currencies:
                    value = data.get(command, {}).get(currency)
                    if value:
                        message_text += f"• 1 {command.upper()} = {value} {currency.upper()}\n"
                
                # Eğer mesaj çok uzunsa, parçalara ayırarak gönderiyoruz
                while len(message_text) > 4096:
                    bot.send_message(message.chat.id, message_text[:4096])
                    message_text = message_text[4096:]

                # Kalan mesajı gönderiyoruz
                bot.send_message(message.chat.id, message_text)
            else:
                bot.send_message(message.chat.id, f"{command.upper()} kuru bilgisi alınamadı.")
        else:
            bot.send_message(message.chat.id, f"API hatası: {response.status_code}")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"Bir hata oluştu: {e}")







# /operator komutu
@bot.message_handler(commands=['operator'])
def operator_sorgu(message):
    try:
        # API'ye GSM numarası ile istek atıyoruz
        gsm = message.text.split()[1]  # GSM numarası komuttan alınır
        url = f"https://api.ondex.uk/ondexapi/operator.php?gsm={gsm}"

        # User-Agent başlığı ekle
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        # API yanıtını yazdır (debugging için)
        print(data)

        # 'Veri' anahtarına erişim sağlanıyor
        phone = data.get("Veri", {}).get("phone", "Bilinmiyor")
        operator = data.get("Veri", {}).get("operator", "Bilinmiyor")

        # Kullanıcı bilgilerini içeren mesajı oluşturuyoruz
        response_message = f"""
        
╭━━━━━━━━━━━━━━━━━━━━━━━
┃➥Numara: {phone}
┃➥Operatör: {operator}
╰━━━━━━━━━━━━━━━━━━━━━━━
"""

        # Mesajı kullanıcıya gönderiyoruz
        bot.reply_to(message, response_message)

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /operator 5393374789")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")







@bot.message_handler(commands=['email'])
def email_sorgu(message):
    try:
        email = message.text.split()[1]  # Kullanıcıdan email adresi al
        url = f"https://api.ondex.uk/ondexapi/emailsorgu.php?email={email}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if "Veri" in data:
            email_data = data["Veri"]
            response_message = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━
┃➥ Email: {email_data.get("Email", "Bilinmiyor")}
┃➥ Kullanıcı Adı: {email_data.get("Name", "Bilinmiyor")}
┃➥ Domain: {email_data.get("Domain", "Bilinmiyor")}
┃➥ Uzantı: {email_data.get("Tld", "Bilinmiyor")}
┃➥ Domain (Tam): {email_data.get("Domain_All", "Bilinmiyor")}
┃➥ Workspace: {"Evet" if email_data.get("Workspace") else "Hayır"}
┃➥ Microsoft 365: {"Evet" if email_data.get("Microsoft_365") != "-" else "Hayır"}
╰━━━━━━━━━━━━━━━━━━━━━━━
"""
            bot.reply_to(message, response_message)
        else:
            bot.reply_to(message, "Bu email adresine ait bilgi bulunamadı.")

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /email example@gmail.com")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")






@bot.message_handler(commands=['iban'])
def iban_sorgula(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Lütfen bir IBAN girin! Örnek: `/iban TR1234567890`")
            return

        iban_no = args[1]
        url = f"https://sowixfree.xyz/sowixapi/iban.php?iban={iban_no}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            result = (f"**IBAN Bilgileri:**\n"
                      f"🏦 **Ad:** {data.get('Banka Adı:', 'Bilinmiyor')}\n"
                      f"🔢 **Kod:** {data.get('Banka Kodu:', 'Bilinmiyor')}\n"
                      f"💳 **Swift:** {data.get('Banka Swift:', 'Bilinmiyor')}\n"
                      f"🏦 **Hesap No:** {data.get('Hesap No:', 'Bilinmiyor')}\n"
                      f"📍 **İl:** {data.get('İl:', 'Bilinmiyor')}\n"
                      f"📍 **İlçe:** {data.get('İlçe:', 'Bilinmiyor')}\n"
                      f"📞 **Tel:** {data.get('Tel:', 'Bilinmiyor')}\n"
                      f"📠 **Fax:** {data.get('Fax:', 'Bilinmiyor')}\n"
                      f"🏠 **Adres:** {data.get('Adres:', 'Bilinmiyor')}\n"
)
        else:
            result = "API'den geçerli bir yanıt alınamadı."

        bot.send_message(message.from_user.id, result, parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.from_user.id, f"Hata oluştu: {e}")








@bot.message_handler(commands=['cocuk'])
def send_child_info(message):
    try:
        # TC Kimlik numarasını komuttan al
        tc_number = message.text.split()[1]

        # API'ye istek at
        url = f"https://siberizim.online/esrarkes/cocuksorgu/api.php?tc={tc_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            bot.reply_to(message, f"API'ye bağlanırken bir hata oluştu. Hata Kodu: {response.status_code}")
            return

        data = response.json()

        # Eğer veri boşsa veya yanlış formattaysa hata mesajı ver
        if not data or not data.get("success") or not isinstance(data.get("data"), list):
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı veya kayıt bulunamadı.")
            return
        
        # İlk kişinin (ana kişi) bilgilerini atla, sadece çocukları gönder
        children = data["data"][1:]  # İlk kişi ana kişi olduğu için [1:] ile sadece çocuklar kalır
        
        if not children:
            bot.reply_to(message, "Bu TC numarasına ait çocuk bilgileri bulunamadı.")
            return
        
        # Tüm çocuk kayıtlarını mesaj olarak gönder
        for record in children:
            mesaj = (
                f" *Çocuk Bilgileri*\n"
                f" *TC:* {record.get('TC', 'Bilinmiyor')}\n"
                f" *İsim:* {record.get('ADI', 'Bilinmiyor')} {record.get('SOYADI', 'Bilinmiyor')}\n"
                f" *Doğum Tarihi:* {record.get('DOGUMTARIHI', 'Bilinmiyor')}\n"
                f" *Ölüm Tarihi:* {record.get('OLUMTARIHI', 'Bilinmiyor')}\n"
                f" *Doğum Yeri:* {record.get('DOGUMYERI', 'Bilinmiyor')}\n"
                f" *Memleket:* {record.get('MEMLEKETIL', 'Bilinmiyor')} - {record.get('MEMLEKETILCE', 'Bilinmiyor')} ({record.get('MEMLEKETKOY', 'Bilinmiyor')})\n"
                f" *Telefon:* {record.get('GSM', 'Bilinmiyor')}\n"
                f" *Baba Adı:* {record.get('BABAADI', 'Bilinmiyor')} | *TC:* {record.get('BABATC', 'Bilinmiyor')}\n"
                f" *Anne Adı:* {record.get('ANNEADI', 'Bilinmiyor')} | *TC:* {record.get('ANNETC', 'Bilinmiyor')}\n"
                f" *Medeni Hal:* {record.get('MEDENIHAL', 'Bilinmiyor')}\n"
                f" *Cinsiyet:* {record.get('CINSIYET', 'Bilinmiyor')}\n"
                f" *Yakınlık:* {record.get('Yakınlık', 'Bilinmiyor')}\n"
            )

            # Mesajı gönder
            bot.send_message(message.chat.id, mesaj, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /cocuk <TC Kimlik No>")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")



@bot.message_handler(commands=['bin'])
def send_bin_info(message):
    try:
        # BIN numarasını komuttan al
        bin_number = message.text.split()[1]

        # API'ye istek at
        url = f"https://sowixfree.xyz/sowixapi/bin.php?bin={bin_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            bot.reply_to(message, f"API'ye bağlanırken bir hata oluştu. Hata Kodu: {response.status_code}")
            return

        data = response.json()

        # API'den gelen veri boşsa veya hatalıysa mesaj gönder
        if not data or 'bin' not in data:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı veya kayıt bulunamadı.")
            return
        
        # Mesaj formatı
        mesaj = (
            f"💳 *BIN Bilgileri*\n"
            f"🏦 *Banka:* {data.get('bank', 'Bilinmiyor')}\n"
            f"🌍 *Ülke:* {data.get('country', 'Bilinmiyor')}\n"
            f"💰 *Kart Türü:* {data.get('level', 'Bilinmiyor')}\n"
            f"📟 *Kart Markası:* {data.get('brand', 'Bilinmiyor')}\n"
            f"💼 *Tip:* {data.get('type', 'Bilinmiyor')}\n"
        )

        # Mesajı gönder
        bot.send_message(message.chat.id, mesaj, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /bin <BIN numarası>")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")






@bot.message_handler(commands=['imei'])
def send_imei_info(message):
    try:
        # IMEI numarasını komuttan al
        imei_number = message.text.split()[1]

        # API'ye istek at
        url = f"https://sowixfree.xyz/sowixapi/imei.php?imei={imei_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            bot.reply_to(message, f"API'ye bağlanırken bir hata oluştu. Hata Kodu: {response.status_code}")
            return

        data = response.json()

        # API'den gelen veri boşsa veya hatalıysa mesaj gönder
        if not data or 'imei' not in data:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı veya kayıt bulunamadı.")
            return
        
        # Mesaj formatı
        mesaj = (
            f"📱 *IMEI Bilgileri*\n"
            f"🆔 *IMEI:* {data.get('imei', 'Bilinmiyor')}\n"
            f"🔒 *Cihaz Durumu:* {data.get('status', 'Bilinmiyor')}\n"
            f"🏷️ *Marka:* {data.get('brand', 'Bilinmiyor')}\n"
            f"💼 *Model:* {data.get('model', 'Bilinmiyor')}\n"
            f"🌍 *Ülke:* {data.get('country', 'Bilinmiyor')}\n"
        )

        # Mesajı gönder
        bot.send_message(message.chat.id, mesaj, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /imei <IMEI numarası>")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")





@bot.message_handler(commands=['cc'])
def cc_checker(message):
    bot.send_message(message.chat.id, "📛 Şu an bakım aşamasında. Lütfen daha sonra tekrar deneyin.")





@bot.message_handler(commands=['resim'])
def resim(message):
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        bot.reply_to(message, "Lütfen sana uygun resim bulabilmem için İngilizce kelime yaz Örnek : \n/resim mercedes")
        return

    arama = args[1]
    api = f"https://magicimage.darkhacker7301.workers.dev/?search={arama}"

    try:
        response = requests.get(api)
        if response.status_code == 200:
            json_data = response.json()
            images = json_data.get("images", [])

            if images:
                image = random.choice(images)
                image_response = requests.get(image)
                if image_response.status_code == 200:
                    image = io.BytesIO(image_response.content)
                    image.seek(0)                    
                    bot.send_photo(message.chat.id, image, caption=f" arama sonuçlarına göre en uygun resim: {arama}")
                else:
                    bot.reply_to(message, "hata oluştu")
            else:
                bot.reply_to(message, "resim bulunamadı")
        else:
            bot.reply_to(message, "api hatası")
    except Exception as e:
        bot.reply_to(message, f"hata oluştu: {e}")






@bot.message_handler(commands=['yaz'])
def yaz_command(message):
    try:
        
        text = message.text.replace('/yaz ', '')

        
        formatted_text = text.replace(' ', '%20')

        
        api_url = f'http://apis.xditya.me/write?text={formatted_text}'

        
        response = requests.get(api_url)

        if response.status_code == 200:
            
            bot.send_photo(message.chat.id, photo=("@maestrochecker.jpg", response.content))
        else:
            bot.reply_to(message, '💪')

    except Exception as e:
        bot.reply_to(message, 'sg')




        





@bot.message_handler(commands=['qr'])
def qr_command(message):
    try:
        text = message.text.replace('/qr ', '').strip()

        if not text:
            bot.reply_to(message, "Lütfen bir metin girin! Örnek: `/qr Merhaba Dünya`", parse_mode="Markdown")
            return

        api_url = f'https://apis.xditya.me/qr/gen?text={text}'

        response = requests.get(api_url)

        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.content)
        else:
            bot.reply_to(message, "QR kod oluşturulamadı, lütfen tekrar deneyin!")

    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")










# Admin Komutu
@bot.message_handler(commands=["admin"])
def admin(message):
    bot.send_message(message.chat.id, "👤 Admin: @ichramall")

@bot.message_handler(commands=["live"])
def live(message):
    try:
        chat_id = -1002326374972  # Buraya GRUP veya KANAL ID'sini yaz
        member_count = bot.get_chat_members_count(chat_id)  # Alternatif fonksiyon
        bot.send_message(message.chat.id, f"📊 Toplam Üye Sayısı: {member_count}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Hata oluştu: {e}")



















@bot.message_handler(commands=['kardes'])
def kardes_sorgu(message):
    try:
        chat_id = message.chat.id
        args = message.text.split()

        if len(args) < 2:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /kardes 12345678901")
            return

        tc_number = args[1]  # TC kimlik numarası komuttan alınır
        url = f"https://talaruscheck.site/apiler/kardes.php?tc={tc_number}"  # API URL'sini doğru şekilde ekle
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:  # API'den başarılı yanıt aldığından emin ol
            if "success" in data and data["success"] == "true":
                kardes_listesi = data.get("data", [])
                
                if kardes_listesi:
                    # "Kendisi" bilgisini ilk başta ekliyoruz
                    kendisi = kardes_listesi[0]
                    kendisi_message = f"""
╭━━━━━━━━━━━━━━
┃ **Adı:** {kendisi.get("ADI", "Bilinmiyor")}
┃ **Soyadı:** {kendisi.get("SOYADI", "Bilinmiyor")}
┃ **Doğum Tarihi:** {kendisi.get("DOGUMTARIHI", "Bilinmiyor")}
┃ **Nüfus İl:** {kendisi.get("NUFUSIL", "Bilinmiyor")}
┃ **Nüfus İlçe:** {kendisi.get("NUFUSILCE", "Bilinmiyor")}
┃ **Anne Adı:** {kendisi.get("ANNEADI", "Bilinmiyor")}
┃ **Anne TC:** {kendisi.get("ANNETC", "Bilinmiyor")}
┃ **Baba Adı:** {kendisi.get("BABAADI", "Bilinmiyor")}
┃ **Baba TC:** {kendisi.get("BABATC", "Bilinmiyor")}
┃ **Uyruğu:** {kendisi.get("UYRUK", "Bilinmiyor")}
┃ **Yakınlık:** {kendisi.get("yakinlik", "Bilinmiyor")}
╰━━━━━━━━━━━━━━
"""
                    
                    # "Kardeşler" kısmını ekliyoruz
                    kardes_message = "╭━━━━━━━━━━━━━━\n┃ **Kardeşler**:\n"
                    for kardes in kardes_listesi[1:]:  # İlk eleman "kendisi" olduğu için, 1'den başlıyoruz
                        kardes_message += f"""
╭━━━━━━━━━━━━━━
┃ **Adı:** {kardes.get("ADI", "Bilinmiyor")}
┃ **Soyadı:** {kardes.get("SOYADI", "Bilinmiyor")}
┃ **Doğum Tarihi:** {kardes.get("DOGUMTARIHI", "Bilinmiyor")}
┃ **Nüfus İl:** {kardes.get("NUFUSIL", "Bilinmiyor")}
┃ **Nüfus İlçe:** {kardes.get("NUFUSILCE", "Bilinmiyor")}
┃ **Anne Adı:** {kardes.get("ANNEADI", "Bilinmiyor")}
┃ **Anne TC:** {kardes.get("ANNETC", "Bilinmiyor")}
┃ **Baba Adı:** {kardes.get("BABAADI", "Bilinmiyor")}
┃ **Baba TC:** {kardes.get("BABATC", "Bilinmiyor")}
┃ **Uyruğu:** {kardes.get("UYRUK", "Bilinmiyor")}
┃ **Yakınlık:** {kardes.get("yakinlik", "Bilinmiyor")}
╰━━━━━━━━━━━━━━
"""
                    
                    # Eğer mesaj 4000 karakterden uzun olursa, dosya olarak gönder
                    if len(kardes_message) + len(kendisi_message) > 4000:
                        with open("kardes_sorgu.txt", "w", encoding="utf-8") as file:
                            file.write(kendisi_message + kardes_message)
                        with open("kardes_sorgu.txt", "rb") as file:
                            bot.send_document(chat_id, file, caption="Kardeş bilgileri:")
                    else:
                        bot.send_message(chat_id, kendisi_message + kardes_message, parse_mode="Markdown")
                else:
                    bot.reply_to(message, "Bu TC numarasına ait kardeş bilgisi bulunamadı.")
        
            else:
                bot.reply_to(message, "API'den geçerli bir yanıt alınamadı.")
        
        else:
            bot.reply_to(message, "API isteği başarısız oldu. Lütfen tekrar deneyin.")
    
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /kardes 12345678901")
    except requests.exceptions.RequestException as e:
        print(f"API isteği hatası: {e}")
        bot.reply_to(message, "API bağlantısında bir sorun oluştu.")
    except Exception as e:
        print(f"Kardeş sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")








@bot.message_handler(commands=['vesika'])
def send_health_info(message):
    try:
        # TC Kimlik numarasını komuttan al
        tc_number = message.text.split()[1]

        # API'ye istek at
        url = f"http://talaruscheck.site/apiler/eokul.php?tc={tc_number}"
        response = requests.get(url)

        if response.status_code != 200:
            bot.reply_to(message, f"API'ye bağlanırken bir hata oluştu. Hata Kodu: {response.status_code}")
            return

        data = response.json()

        # API'den gelen success yanıtını kontrol et
        if data.get("success") != "true":
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı.")
            return

        # TC Kimlik ve Vesika bilgileri
        tc = data.get("TC", "Bilinmiyor")
        vesika = data.get("VESIKA", "Bilinmiyor")

        # Eğer vesika base64 formatında ise çözülmesi gerekiyor
        if vesika != "Bilinmiyor":
            # Base64'ü çöz
            img_data = base64.b64decode(vesika)

            # Görseli bellek üzerinde bir dosyaya çevir
            img_file = BytesIO(img_data)
            img_file.name = 'vesika.png'

            # PNG dosyasını DM olarak gönder
            bot.send_photo(message.chat.id, photo=img_file)
            return

        # Eğer vesika bilgisi yoksa, mesajı basit şekilde gönder
        mesaj = (
            f" *TC:* {tc}\n"
            f" *Vesika:* {vesika}\n"
        )

        # Mesajı gönder
        bot.send_message(message.chat.id, mesaj, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /vesika <TC Kimlik No>")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")

    

















@bot.message_handler(commands=['fatura'])
def send_fatura_info(message):
    try:
        # GSM numarasını komuttan al
        gsm_number = message.text.split()[1]

        # API URL'si
        url = f"https://pro.sowixfree.xyz/sowix/borç.php?gsm={gsm_number}"

        # API'ye istek atarken User-Agent başlığı ekle
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            bot.reply_to(message, f"API'ye bağlanırken bir hata oluştu. Hata Kodu: {response.status_code}")
            return

        data = response.json()

        # Eğer API yanıtı geçerli değilse
        if "sonuc" not in data:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı.")
            return

        # Abonelik bilgisi ve fatura detaylarını al
        abonelik_bilgisi = data["sonuc"].get("abonelik_bilgisi", "Bilinmiyor")
        faturalar = data["sonuc"].get("faturalar", [])

        # Fatura bilgilerini formatla
        fatura_mesaj = ""
        for fatura in faturalar:
            fatura_mesaj += (
                f"📜 *Fatura No:* {fatura.get('fatura_no', 'Bilinmiyor')}\n"
                f"📅 *Son Ödeme Tarihi:* {fatura.get('son_odeme_tarihi', 'Bilinmiyor')}\n"
                f"💰 *Fatura Tutarı:* {fatura.get('fatura_tutari', 'Bilinmiyor')}\n"
                f"💵 *Hizmet Ücreti:* {fatura.get('hizmet_ucreti', 'Bilinmiyor')}\n"
                f"💳 *Toplam Tutar:* {fatura.get('toplam_tutar', 'Bilinmiyor')}\n\n"
            )

        # Fatura yoksa mesajı değiştir
        if not fatura_mesaj:
            fatura_mesaj = "Fatura bilgisi bulunmamaktadır."

        # Mesajı oluştur
        mesaj = (
            f"📱 *Abonelik Bilgisi:* {abonelik_bilgisi}\n\n"
            f"{fatura_mesaj}"
        )

        # Mesajı gönder
        bot.send_message(message.chat.id, mesaj, parse_mode='Markdown')

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /fatura <GSM Numarası>")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")













@bot.message_handler(commands=['kizlik'])
def kizlik_soyadi_sorgula(message):
    try:
        # TC Kimlik numarasını al
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /kizlik <TC Kimlik No>")
            return

        tc_number = parts[1]

        # API'ye istek at
        url = f"https://siberizim.online/esrarkes/kızlık.php?tc={tc_number}"
        response = requests.get(url)

        if response.status_code != 200:
            bot.reply_to(message, f"API'ye bağlanırken bir hata oluştu. Hata Kodu: {response.status_code}")
            return

        data = response.json()

        # API'den gelen success yanıtını kontrol et
        if data.get("success") != "true":
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı.")
            return

        kizlik_soyadi = data.get("kizliksoyadi", "Bilinmiyor")

        # Mesajı gönder
        bot.send_message(message.chat.id, f"👩‍🦰 *Kızlık Soyadı:* {kizlik_soyadi}", parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")




# Kullanıcı kullanım sayacı
user_usage = {}
usage_limit = 3  # Günlük kullanım limiti

# Günlük sıfırlama işlemi (24 saatlik süre)
reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

# Kullanıcı kullanım sayısını kontrol ve reset et
def reset_usage():
    global reset_time, user_usage
    now = datetime.now()
    if now >= reset_time:
        user_usage = {}  # Resetle
        reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

# API'den veri çekme fonksiyonu (User-Agent ve yeniden deneme sistemi ile)
def get_api_data(url, max_retries=3, delay=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Hatası: {response.status_code}, Tekrar Deneniyor...")
        except requests.exceptions.RequestException as e:
            print(f"Hata: {e}, Tekrar Deneniyor...")
        time.sleep(delay)
    return None

# Komut /log işleyicisi
@bot.message_handler(commands=['log'])
def get_log_info(message):
    reset_usage()  # Kullanıcı kullanım sayacını kontrol et ve resetle

    try:
        user_id = message.from_user.id  # Kullanıcıyı belirle

        # Kullanıcının kullanım sayısını kontrol et
        if user_id in user_usage:
            if user_usage[user_id] >= usage_limit:
                bot.reply_to(message, "Günlük kullanım limitiniz doldu. Lütfen yarın tekrar deneyin.")
                return
        else:
            user_usage[user_id] = 0  # Eğer kullanıcı ilk kez komut kullanıyorsa, sayacı başlat

        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Geçersiz kullanım! Örnek: /log netflix.com")
            return
        
        site = args[1]
        url = f"https://luaxtia.u.cname.dev/log?ara=https://{site}"
        data = get_api_data(url)

        if not data or "results" not in data or not isinstance(data["results"], list):
            bot.reply_to(message, "API'den geçerli hesap bilgisi alınamadı.")
            return

        # API'den gelen logları al
        hesaplar = data["results"][:10]  # Sadece ilk 10 hesabı al

        if not hesaplar:
            bot.reply_to(message, "Bu site için hesap bulunamadı.")
            return

        # Logları txt dosyasına kaydet
        file_path = f"log_{user_id}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(hesaplar))

        # Txt dosyasını kullanıcıya gönder
        with open(file_path, "rb") as file:
            bot.send_document(message.chat.id, file)

        # Kullanıcı kullanım sayısını bir artır
        user_usage[user_id] += 1

    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")






@bot.message_handler(commands=['tcpro'])
def tcpro_sorgu(message):
    try:
        chat_id = message.chat.id
        args = message.text.split()

        if len(args) < 2:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /tcpro 14570512634")
            return

        tc_number = args[1]
        url = f"https://api.ondex.uk/ondexapi/tcprosorgu.php?tc={tc_number}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        print("API Yanıtı:", response.text)  # Yanıtı kontrol için ekrana yazdır

        try:
            data = response.json()  # JSON formatına çevir
        except json.JSONDecodeError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        # Eğer API "error" mesajı döndürüyorsa
        if "error" in data and data["error"] == "Sonuç bulunamadı":
            bot.reply_to(message, "Bu TC numarasına ait detaylı bilgi bulunamadı.")
            return

        # Kişi bilgileri "Veri" anahtarında
        kisi = data.get("Veri", {})

        if not kisi:
            bot.reply_to(message, "Bu TC numarasına ait detaylı bilgi bulunamadı.")
            return

        # GSM numaralarını düzgün şekilde alıyoruz
        gsm_numbers = ', '.join(gsm[0] for gsm in kisi.get("GSM", []))

        response_message = f"""
╭━━━━━━━━━━━━━━━━━━━━━━
┃➥ TC: {kisi.get("TCKN", "Yok")}
┃➥ Ad: {kisi.get("Adi", "Yok")}
┃➥ Soyad: {kisi.get("Soyadi", "Yok")}
┃➥ Cinsiyet: {kisi.get("Cinsiyet", "Yok")}
┃➥ Doğum Tarihi: {kisi.get("DogumTarihi", "Yok")}
┃➥ Ölüm Tarihi: {kisi.get("OlumTarihi", "Yok")}
┃➥ Doğum Yeri: {kisi.get("DogumYeri", "Yok")}
┃➥ Medeni Hal: {kisi.get("MedeniHal", "Yok")}
┃➥ Anne Adı: {kisi.get("AnneAdi", "Yok")}
┃➥ Baba Adı: {kisi.get("BabaAdi", "Yok")}
┃➥ Adres İl: {kisi.get("AdresIl", "Yok")}
┃➥ Adres İlçe: {kisi.get("AdresIlce", "Yok")}
┃➥ Memleket İl: {kisi.get("MemleketIl", "Yok")}
┃➥ Memleket İlçe: {kisi.get("MemleketIlce", "Yok")}
┃➥ Memleket Köy: {kisi.get("MemleketKoy", "Yok")}
┃➥ Aile Sıra No: {kisi.get("AileSiraNo", "Yok")}
┃➥ Birey Sıra No: {kisi.get("BireySiraNo", "Yok")}
┃➥ 2023 Adres: {kisi.get("2023Adres", "Yok")}
┃➥ 2015 Adres: {kisi.get("2015Adres", "Yok")}
┃➥ Vergi Numarası: {kisi.get("VergiNumarasi", "Yok")}
┃➥ GSM: {gsm_numbers}
╰━━━━━━━━━━━━━━━━━━━━━━
"""

        # Eğer mesaj 4000 karakterden kısa ise direkt gönder
        if len(response_message) <= 4000:
            bot.reply_to(message, response_message)
        else:
            file_name = f"tcpro_{chat_id}.txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(response_message)

            with open(file_name, 'rb') as f:
                bot.send_document(chat_id, f)

            os.remove(file_name)

    except Exception as e:
        print(f"Detay sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu, tekrar deneyin.")






@bot.message_handler(commands=['sorgu'])
def adsoyad_sorgu(message):
    try:
        chat_id = message.chat.id
        args = message.text.split()

        if len(args) < 3:
            bot.reply_to(message, "Geçersiz komut. Kullanım: /sorgu Yezda Selvi Bursa Osmangazi")
            return

        ad = args[1]
        soyad = args[2]
        il = args[3] if len(args) > 3 else None
        ilce = args[4] if len(args) > 4 else None

        # URL'yi oluştur
        url = f"https://api.ondex.uk/ondexapi/adsoyadprosorgu.php?ad={ad}&soyad={soyad}"
        if il and ilce:
            url += f"&il={il}&ilce={ilce}"

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        print("API Yanıtı:", response.text)  # Yanıtı kontrol etmek için ekrana yazdır

        try:
            data = response.json()
        except json.JSONDecodeError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        kisi_listesi = data.get("Veri", [])
        if not kisi_listesi:
            bot.reply_to(message, "Bu ad-soyad bilgisine ait detaylı bilgi bulunamadı.")
            return

        mesajlar = []
        for kisi in kisi_listesi:
            gsm_numbers = ', '.join(kisi.get("GSM", []))
            
            mesaj = f"""
╭━━━━━━━━━━━━━━━━━━━━━━
┃➥ Ad: {kisi.get("Adi", "Yok")}
┃➥ Soyad: {kisi.get("Soyadi", "Yok")}
┃➥ TC: {kisi.get("TCKN", "Yok")}
┃➥ Doğum Tarihi: {kisi.get("DogumTarihi", "Yok")}
┃➥ Anne Adı: {kisi.get("AnneAdi", "Yok")}
┃➥ Anne TCKN: {kisi.get("AnneTCKN", "Yok")}
┃➥ Baba Adı: {kisi.get("BabaAdi", "Yok")}
┃➥ Baba TCKN: {kisi.get("BabaTCKN", "Yok")}
┃➥ Nüfus İl: {kisi.get("NufusIl", "Yok")}
┃➥ Nüfus İlçe: {kisi.get("NufusIlce", "Yok")}
┃➥ Adres: {kisi.get("Adres", "Yok")}
┃➥ Uyruk: {kisi.get("Uyruk", "Yok")}
╰━━━━━━━━━━━━━━━━━━━━━━
            """
            mesajlar.append(mesaj)

        tum_mesaj = "\n".join(mesajlar)

        if len(tum_mesaj) <= 4000:
            bot.reply_to(message, tum_mesaj)
        else:
            file_name = f"sorgu_{chat_id}.txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(tum_mesaj)

            with open(file_name, 'rb') as f:
                bot.send_document(chat_id, f)

            os.remove(file_name)

    except Exception as e:
        print(f"Sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu, tekrar deneyin.")








@bot.message_handler(commands=['isyeriarkadas'])
def isyeri_arkadas_sorgu(message):
    try:
        # Kullanıcının mesajındaki TC'yi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]  # /isyeriarkadas [TC]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /isyeriarkadas 61342404970")
            return
        
        tc_number = parameters[0]  # TC numarasını al
        
        # API'yi çağır
        url = f"https://api.ondex.uk/ondexapi/isyeriarkadasisorgu.php?tc={tc_number}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if data.get("Veri"):
            result = "İşyeri Arkadaşları\n╭━━━━━━━━━━━━━━━━━━━━━\n"
            for person in data["Veri"]:
                result += f"""
┃➥ Ad Soyad: {person.get("AdiSoyadi", "Bilinmiyor")}
┃➥ Kimlik Numarası: {person.get("KimlikNumarasi", "Bilinmiyor")}
┃➥ Çalışma Durumu: {person.get("CalismaDurumu", "Bilinmiyor")}
┃➥ İşe Giriş Tarihi: {person.get("IseGirisTarihi", "Bilinmiyor")}
"""
            result += "╰━━━━━━━━━━━━━━━━━━━━━"
            
            if len(result) > 4000:
                file_name = f"isyeri_arkadas_{chat_id}.txt"
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(result.strip())
                with open(file_name, 'rb') as file:
                    bot.send_document(chat_id, file)
                os.remove(file_name)
            else:
                while len(result) > 4000:
                    bot.send_message(chat_id, result[:4000])
                    result = result[4000:]
                if len(result) > 0:
                    bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu TC numarasıyla ilgili işyeri arkadaşı bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")












@bot.message_handler(commands=['dcsorgu'])
def discord_sorgu(message):
    try:
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut kullanım. Örnek: /dcsorgu 529046672219832344")
            return
        
        user_id = parameters[0]
        url = f"https://api.ondex.uk/ondexapi/discordsorgu.php?id={user_id}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if 'Veri' in data:
            discord_info = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃Discord Sorgu Sonuçları:
┃➥ Kullanıcı Adı: {data['Veri'].get('username', 'Bilinmiyor')}
┃➥ Global Adı: {data['Veri'].get('global_name', 'Bilinmiyor')}
┃➥ Avatar: {data['Veri'].get('avatar_url', 'Bilinmiyor')}
┃➥ Token: {data['Veri'].get('token', 'Bilinmiyor')}
╰━━━━━━━━━━━━━━━━━━━━━
"""
            bot.send_message(chat_id, discord_info)
        else:
            bot.reply_to(message, "Bu ID'ye ait bir kullanıcı bulunamadı.")
    
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")











@bot.message_handler(commands=['dcsunucu'])
def discord_sunucu_sorgu(message):
    try:
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut kullanımı. Örnek: /dcsunucu kFdG88w")
            return

        davet_kodu = parameters[0]
        url = f"https://api.ondex.uk/ondexapi/discord_sunucu_sorgu.php?davet={davet_kodu}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)

        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return

        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return

        if 'Invitation_Information' in data:
            server_info = data['Invitation_Information']
            inviter_info = data.get('Inviter_Information', {})

            # Sunucu Özelliklerini küçük harfe dönüştür ve alt alta sıralanmış şekilde birleştir
            server_features = server_info.get('Server_Features', 'Bilinmiyor')
            server_features = server_features.lower().replace(" /", "\n/")  # Alt alta sıralanması için

            sunucu_mesaj = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃Discord Sunucu Sorgu Sonuçları:
┃➥ Sunucu Adı: {server_info.get('Server_Name', 'Bilinmiyor')}
┃➥ Sunucu ID: {server_info.get('Server_ID', 'Bilinmiyor')}
┃➥ Davet Linki: {server_info.get('Invitation', 'Bilinmiyor')}
┃➥ Kanal Adı: {server_info.get('Channel_Name', 'Bilinmiyor')}
┃➥ Kanal ID: {server_info.get('Channel_ID', 'Bilinmiyor')}
┃➥ Açıklama: {server_info.get('Server_Description', 'Bilinmiyor')}
┃➥ NSFW: {'Evet' if server_info.get('Server_NSWF', False) else 'Hayır'}
┃➥ NSFW Level : {server_info.get('Server_NSFW_Level', 'Bilinmiyor')}
┃➥ Doğrulama Seviyesi: {server_info.get('Server_Verification_Level', 'Bilinmiyor')}
┃➥ Premium Abone Sayısı: {server_info.get('Server_Premium_Subscription_Count', 'Bilinmiyor')}
┃➥ Sunucu Simgesi: {server_info.get('Server_Icon', 'Bilinmiyor')}
┃➥ Sunucu Özellikleri:
{server_features}
╰━━━━━━━━━━━━━━━━━━━━━
Davet Sahibi
╭━━━━━━━━━━━━━━━━━━━━━
┃➥ Davetiye Sahibi: {inviter_info.get('Global_Name', 'Bilinmiyor')} ({inviter_info.get('Username', 'Bilinmiyor')})
┃➥ Davet Eden ID: {inviter_info.get('ID', 'Bilinmiyor')}
┃➥ Davet Eden Avatar: {inviter_info.get('Avatar', 'Bilinmiyor')}
┃➥ Accent Rengi: {inviter_info.get('Accent_Color', 'Bilinmiyor')}
┃➥ Banner Rengi: {inviter_info.get('Banner_Color', 'Bilinmiyor')}
╰━━━━━━━━━━━━━━━━━━━━━
"""
            bot.send_message(chat_id, sunucu_mesaj)
        else:
            bot.reply_to(message, "Bu davet koduna ait bir sunucu bulunamadı.")

    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")













@bot.message_handler(commands=['isyeri'])
def isyeri_sorgu(message):
    try:
        # Kullanıcının mesajındaki TC'yi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]  # /isyeri [TC]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /isyeri 61342404970")
            return
        
        tc_number = parameters[0]  # TC numarasını al
        
        # API'yi çağır
        url = f"https://api.ondex.uk/ondexapi/isyerisorgu.php?tc={tc_number}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if data.get("Kisi"):
            kimlik = data["Kisi"]
            isyeri = data["Isyeri"]
            
            result = " İşyeri Sorgu Sonucu\n"
            result += "╭━━━━━━━━━━━━━━━━━━━━━"  # Çizgiyi tekrar ekliyoruz.

            # Kullanıcı ve işyeri bilgilerini listeye ekliyoruz.
            result += f"""
┃➥ Ad Soyad : {kimlik["AdiSoyadi"]}
┃➥ Kimlik Numarası: {kimlik["KimlikNumarasi"]}
┃➥ Çalışma Durumu : {kimlik["CalismaDurumu"]}
┃➥ İşe Giriş Tarihi: {kimlik["IseGirisTarihi"]}
┃➥ İşyeri Ünvanı  : {isyeri["IsyeriUnvani"]}
┃➥ İşyeri Sektörü : {isyeri["IsyeriSektoru"]}
┃➥ Tehlike Sınıfı : {isyeri["TehlikeSinifi"]}
┃➥ NACE Kodu : {isyeri["NaceKodu"]}
┃➥ İşyeri SGK Sicil No: {isyeri["IsyeriSGKSicilNo"]}
"""

            result += "╰━━━━━━━━━━━━━━━━━━━━━\n"  # Çizgi sonlandırma.

            # Sonucun uzunluğu 4000'den fazla ise dosya olarak gönder
            if len(result) > 4000:
                file_name = f"isyeri_sorgu_{chat_id}.txt"
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(result.strip())
                with open(file_name, 'rb') as file:
                    bot.send_document(chat_id, file)
                os.remove(file_name)
            else:
                bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu TC numarasıyla ilgili işyeri bilgisi bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")






import time

# Kullanıcıların günlük kullanım sayısını tutmak için bir dictionary
user_usage = {}

@bot.message_handler(commands=['dcgen'])
def dcgen(message):
    chat_id = message.chat.id
    current_time = time.time()
    daily_limit = 3  # Kullanıcı başına günlük 2 kullanım limiti
    
    # Kullanıcı geçmiş verisini kontrol et
    if chat_id in user_usage:
        last_used_time, usage_count = user_usage[chat_id]
        
        # Eğer günün ilk kullanımına geçtiyse, sayacı sıfırlıyoruz
        if current_time - last_used_time > 86400:  # 86400 saniye = 24 saat
            usage_count = 0
        
        # Kullanım limitini kontrol et
        if usage_count >= daily_limit:
            bot.reply_to(message, "Bugün bu komutu 2 kez kullandınız. Lütfen yarın tekrar deneyin.")
            return
    else:
        usage_count = 0
    
    # API'yi çağır
    url = f"https://api.ondex.uk/ondexapi/discordnitrogenerator.php?adet=500"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    response = requests.get(url, headers=headers)
    print("API Yanıt Kodu:", response.status_code)
    print("API Yanıt İçeriği:", response.text)
    
    if response.status_code != 200:
        bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
        return
    
    try:
        data = response.json()
    except Exception as e:
        bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
        return
    
    if data.get("nitrolar"):
        nitrolar = data["nitrolar"]
        result = "\n".join(nitrolar)  # Linkleri sadec alt alta yaz
        
        # Kullanıcıyı güncelle
        user_usage[chat_id] = (current_time, usage_count + 1)

        # Eğer cevap uzun ise dosya olarak gönder
        if len(result) > 4000:
            file_name = f"dcgen_{chat_id}.txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(result.strip())
            with open(file_name, 'rb') as file:
                bot.send_document(chat_id, file)
            os.remove(file_name)
        else:
            bot.send_message(chat_id, result.strip())
    else:
        bot.reply_to(message, "API'den geçerli bir veri alınamadı.")




@bot.message_handler(commands=['liveshot'])
def liveshot(message):
    try:
        # Kullanıcının mesajındaki URL'yi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]  # /liveshot [url]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /liveshot google.com")
            return
        
        url = parameters[0]  # Siteyi al
        
        # API'yi çağır
        api_url = f"https://api.ondex.uk/ondexapi/liveshot.php?url={url}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(api_url, headers=headers, timeout=10)  # 10 saniye zaman aşımı
        print("API Yanıt Kodu:", response.status_code)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return

        data = response.json()

        if data["status"] == "success":
            # Base64 görseli al
            image_base64 = data["image"]
            
            # Base64 görseli dosya olarak indirip göndermek için
            from io import BytesIO
            import base64
            image_data = base64.b64decode(image_base64)
            image_file = BytesIO(image_data)
            image_file.name = "liveshot_image.png"
            
            bot.send_photo(chat_id, image_file)
        else:
            bot.reply_to(message, "Veri alınırken bir hata oluştu.")
    
    except requests.exceptions.Timeout:
        bot.reply_to(message, "API zaman aşımına uğradı. Lütfen daha sonra tekrar deneyin.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")





@bot.message_handler(commands=['ping'])
def ping_sorgu(message):
    try:
        # Kullanıcıdan IP adresini al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /ping google.com")
            return
        
        ip_address = parameters[0]  # IP adresini al
        
        # API'yi çağırmak için URL'yi ayarla
        url = f"https://api.ondex.uk/ondexapi/pingsorgu.php?ip={ip_address}"

        # User-Agent başlığını ayarla
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # API'yi çağır
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if data.get("ip_adresi"):
            # Ping süresi ve renkli ışık belirleme
            lowest_ping = data['gecikme_zamanları']['en_düşük']
            avg_ping = data['gecikme_zamanları']['ortalama']
            highest_ping = data['gecikme_zamanları']['en_yüksek']

            if float(avg_ping) < 100:
                ping_status = "🟢 Hızlı Ping"
            elif 100 <= float(avg_ping) < 200:
                ping_status = "🟡 Orta Ping"
            else:
                ping_status = "🔴 Yavaş Ping"

            result = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃ Ping Sorgu Sonucu:
┃
┃ ➥ IP Adresi: {data['ip_adresi']}
┃ ➥ Gönderilen Paketler: {data['paketler']['gönderilen']}
┃ ➥ Alınan Paketler: {data['paketler']['alinan']}
┃ ➥ Kaybolan Paket Yüzdesi: {data['paketler']['kaybolan_paket_yüzdesi']}%
┃
┃ ➥ En Düşük Gecikme: {lowest_ping} ms
┃ ➥ Ortalama Gecikme: {avg_ping} ms
┃ ➥ En Yüksek Gecikme: {highest_ping} ms
┃ ➥ Gecikme Sapması: {data['gecikme_zamanları']['sapma']} ms
┃
┃ ➥ Ping Durumu: {ping_status}
╰━━━━━━━━━━━━━━━━━━━━━
            """
            
            bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu IP adresi ile ilgili ping bilgisi bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")






@bot.message_handler(commands=['port'])
def port_sorgu(message):
    try:
        # Kullanıcıdan host bilgisi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /port google.com")
            return
        
        host = parameters[0]  # Host bilgisi
        
        # User-Agent eklemek için headers oluştur
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # API'yi çağır
        url = f"https://api.ondex.uk/ondexapi/portscanner.php?host={host}"
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if data.get("Host"):
            result = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃ Port Scanner Sonucu:
┃
┃➥ Host: {data['Host']}
┃➥ Latency: {data['Latency']}
┃➥ Filtrelenmiş Portlar: {data['Filtered Ports']}
┃
┃➥ Açık Portlar:
"""
            
            for port in data['Open Ports']:
                result += f"┃➥ Port: {port['Port']}, Durum: {port['State']}, Servis: {port['Service']}\n"
            
            result += "╰━━━━━━━━━━━━━━━━━━━━━"
            
            bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu host ile ilgili port taraması bilgisi bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")






@bot.message_handler(commands=['ssl'])
def ssl_sorgu(message):
    try:
        # Kullanıcıdan host bilgisi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /ssl google.com")
            return
        
        host = parameters[0]  # Host bilgisi
        
        # User-Agent eklemek için headers oluştur
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # API'yi çağır
        url = f"https://api.ondex.uk/ondexapi/ssltlssorgu.php?host={host}"
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if data.get("hostname"):
            result = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃ SSL/TLS Sorgu Sonucu:
┃
┃➥ Hostname: {data['hostname']}
┃➥ Issuer: {data['results'][0]['issuer_name']}
┃➥ Common Name: {data['results'][0]['common_name']}
┃➥ Not Before: {data['results'][0]['not_before']}
┃➥ Not After: {data['results'][0]['not_after']}
┃➥ Serial Number: {data['results'][0]['serial_number']}
┃
┃➥ Diğer Sertifikalar:
"""
            
            for cert in data['results']:
                result += f"┃➥ Issuer: {cert['issuer_name']}, Common Name: {cert['common_name']}, Not Before: {cert['not_before']}\n"
            
            result += "╰━━━━━━━━━━━━━━━━━━━━━"
            
            # Eğer sonuç 4000 karakterden fazla ise txt olarak gönder
            if len(result) > 4000:
                with open("ssl_sertifika.txt", "w", encoding='utf-8') as file:
                    file.write(result)
                bot.send_document(chat_id, open("ssl_sorgu_result.txt", 'rb'))
            else:
                bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu host ile ilgili SSL/TLS sorgu bilgisi bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")






@bot.message_handler(commands=['parsel'])
def parsel_sorgu(message):
    try:
        # Kullanıcıdan Ada, Parsel, Mahalle bilgilerini al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 3:
            bot.reply_to(message, "Geçersiz komut. Örnek: /parsel 1363 2 tarabya")
            return
        
        ada = parameters[0]  # Ada bilgisi
        parsel = parameters[1]  # Parsel bilgisi
        mahalle = parameters[2]  # Mahalle bilgisi
        
        # User-Agent eklemek için headers oluştur
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # API'yi çağır
        url = f"https://api.ondex.uk/ondexapi/parselsorgu.php?ada={ada}&parsel={parsel}&mahalle={mahalle}"
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if data.get("Veri"):
            result = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃ Parsel Sorgu Sonucu:
┃
┃➥ Ada: {ada}
┃➥ Parsel: {parsel}
┃➥ Mahalle: {mahalle}
┃
┃➥ Bulunan Kişiler:
"""
            for entry in data['Veri']:
                result += f"┃➥ Ad: {entry['Name']} {entry['Surname']}\n"
                result += f"┃➥ Baba Adı: {entry['BabaAdi']}\n"
                result += f"┃➥ Kimlik: {entry['Identify']}\n"
                result += f"┃➥ İL: {entry['İlBilgisi']}\n"
                result += f"┃➥ İlçe: {entry['İlceBilgisi']}\n"
                result += f"┃➥ Mahalle: {entry['MahalleBilgisi']}\n"
                result += f"┃➥ Zemin Tipi: {entry['ZeminTipBilgisi']}\n"
                result += f"┃➥ Ada Bilgisi: {entry['AdaBilgisi']}\n"
                result += f"┃➥ Parsel Bilgisi: {entry['ParselBilgisi']}\n"
                result += f"┃➥ Yüzölçümü: {entry['YuzolcumBilgisi']} m²\n"
                result += f"┃➥ Ana Taşınmaz Nitelik: {entry['AnaTasinmazNitelik']}\n"
                result += f"┃➥ Blok Bilgisi: {entry['BlokBilgisi']}\n"
                result += f"┃➥ Bağımsız Bölüm No: {entry['BagimsizBolumNo']}\n"
                result += f"┃➥ Arsa Pay: {entry['ArsaPay']}"
                result += f"┃➥ Arsa Payda:{entry['ArsaPayda']}\n"
                result += f"┃➥ Bağımsız Bölüm Nitelik: {entry['BagimsizBolumNitelik']}\n"
                result += f"┃➥ İştirak No: {entry['IstirakNo']}\n"
                result += f"┃➥ Hisse Pay: {entry['HissePay']}"
                result += f"┃➥ Hissede Pay: {entry['HissePayda']}\n"
                result += f"┃➥ Edinme Sebebi: {entry['EdinmeSebebi']}\n"
                result += f"┃➥ Tapu Tarihi: {entry['TapuDate']}\n"
                result += f"┃➥ Yevmiye: {entry['Yevmiye']}\n"
                result += "┃━━━━━━━━━━━━━━━━━━━━━\n"
            
            result += "╰━━━━━━━━━━━━━━━━━━━━━"
            
            # Eğer sonuç 4000 karakteri geçiyorsa, parçalara ayırarak DM olarak gönder
            if len(result) > 4000:
                parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
                for part in parts:
                    bot.send_message(chat_id, part.strip())
            else:
                bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu parsel ile ilgili herhangi bir bilgi bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")



@bot.message_handler(commands=['sulalepro'])
def sulale_pro(message):
    try:
        # Kullanıcıdan TC bilgisi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /sulalepro 11111111110")
            return
        
        tc = parameters[0]  # TC Kimlik numarası
        
        # User-Agent eklemek için headers oluştur
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # API'yi çağır
        url = f"https://api.ondex.uk/ondexapi/sulaleprosorgu.php?tc={tc}"
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if data.get("Veri"):
            result = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃ Sülale Pro Sonucu:
"""
            for person in data['Veri']:
                result += f"""
╭━━━━━━━━━━━━━━
┃➥ TCKN: {person['TCKN']}
┃➥ Adı: {person['Adi']}
┃➥ Soyadı: {person['Soyadi']}
┃➥ Doğum Tarihi: {person['DogumTarihi']}
┃➥ Anne Adı: {person['AnneAdi']}
┃➥ Anne TCKN: {person['AnneTCKN']}
┃➥ Baba Adı: {person['BabaAdi']}
┃➥ Baba TCKN: {person['BabaTCKN']}
┃➥ Nüfus İl: {person['NufusIl']}
┃➥ Nüfus İlçe: {person['NufusIlce']}
┃➥ Uyruk: {person['Uyruk']}
╰━━━━━━━━━━━━━━
"""
            
            # Eğer mesaj 4000 karakterden uzun ise, parçalara ayırarak göndereceğiz
            if len(result) > 4000:
                # Mesajı 4000 karakterlik parçalara ayır
                parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
                
                # Her bir parçayı DM olarak gönder
                for part in parts:
                    bot.send_message(chat_id, part.strip())
            else:
                bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu TC kimlik numarasıyla ilgili veriye ulaşılamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")








@bot.message_handler(commands=['kuzen'])
def kuzen(message):
    try:
        # Kullanıcıdan TC bilgisi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /kuzen 11111111110")
            return
        
        tc = parameters[0]  # TC Kimlik numarası
        
        # User-Agent eklemek için headers oluştur
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # API'yi çağır
        url = f"https://api.ondex.uk/ondexapi/sulaleprosorgu.php?tc={tc}"
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        # Hata kontrolü: Eğer "error" varsa, sonuç bulunamadı
        if data.get("error") == "Sonuç bulunamadı":
            bot.reply_to(message, "Bu TC kimlik numarasıyla ilgili kuzen bilgisine ulaşılamadı.")
            return
        
        if data.get("Veri"):
            result = ""
            for person in data['Veri']:
                # Yakinlik sadece Kuzeni (Anne) ve Kuzeni (Baba) olmalı
                if person['Yakinlik'] in ['Kuzeni (Anne)', 'Kuzeni (Baba)']:
                    result += f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃ Kuzen Sorgu Sonucu:
┃➥ Yakınlık: {person['Yakinlik']}
┃➥ TCKN: {person['TCKN']}
┃➥ Adı: {person['Adi']}
┃➥ Soyadı: {person['Soyadi']}
┃➥ Doğum Tarihi: {person['DogumTarihi']}
┃➥ Anne Adı: {person['AnneAdi']}
┃➥ Anne TCKN: {person['AnneTCKN']}
┃➥ Baba Adı: {person['BabaAdi']}
┃➥ Baba TCKN: {person['BabaTCKN']}
┃➥ Nüfus İl: {person['NufusIl']}
┃➥ Nüfus İlçe: {person['NufusIlce']}
┃➥ Uyruk: {person['Uyruk']}
╰━━━━━━━━━━━━━━━━━━━━━
"""
            
            # Eğer metin 4000 karakterden uzunsa, parçalara ayır
            if len(result) > 4000:
                result = result.strip()
                # Parçaları oluştur
                num_parts = math.ceil(len(result) / 4000)
                
                for i in range(num_parts):
                    part = result[i*4000:(i+1)*4000]
                    bot.send_message(chat_id, part)
            else:
                bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu TC kimlik numarasıyla ilgili kuzen bilgisine ulaşılamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")








@bot.message_handler(commands=['operatorpro'])
def operator2(message):
    try:
        # Kullanıcıdan GSM numarası bilgisi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /operator2 +905333333333")
            return
        
        gsm = parameters[0]  # GSM numarası
        
        # User-Agent eklemek için headers oluştur
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # API'yi çağır
        url = f"https://api.ondex.uk/ondexapi/gunceloperator.php?gsm={gsm}"
        response = requests.get(url, headers=headers)
        print("API Yanıt Kodu:", response.status_code)
        print("API Yanıt İçeriği:", response.text)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, "API'den gelen veri geçersiz. JSON hatası.")
            return
        
        if data.get("guncel_operator"):
            operator_info = data['guncel_operator'][0]
            result = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃ Güncel Operatör Sorgu Sonucu:
┃
┃➥ Numara: {operator_info['telefon_numarasi']}
┃➥ Operatör: {operator_info['guncel_operator']}
┃➥ Geçerlilik Durumu: {operator_info['gecerli_numara']}
┃➥ Ülke Kodu: {operator_info['ulke_kodu']}
┃➥ Mobil Ağ Kodu: {operator_info['mobil_ag_kodu']}
┃➥ Mobil Ülke Kodu: {operator_info['mobil_ulke_kodu']}
┃➥ Logo: {operator_info['icon']}
╰━━━━━━━━━━━━━━━━━━━━━
"""
            bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Bu numara ile ilgili operatör bilgisi bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")




import requests
import base64
import io
from PIL import Image  # Bu satırı ekledim
from telebot import TeleBot



@bot.message_handler(commands=['qr'])
def qr_code(message):
    try:
        # Kullanıcıdan komut sonrası metni al
        text = ' '.join(message.text.split()[1:])
        
        if not text:
            bot.reply_to(message, "Lütfen bir metin girin. Örnek: /qr Merhaba")
            return
        
        # User-Agent başlığını ekleyerek API'ye istek gönder
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # API URL'si
        url = f"https://api.prtcl.icu/ondexapi/qrcodegenerator.php?text={text}"
        
        response = requests.get(url, headers=headers)
        
        # Yanıtı kontrol et
        if response.status_code == 200:
            # API yanıtının base64 veri olup olmadığını kontrol et
            if response.text.startswith('data:image/png;base64,'):
                # Base64 verisini çöz
                image_data = base64.b64decode(response.text.split(',')[1])
                
                # Base64 verisini image formatına dönüştür
                image = Image.open(io.BytesIO(image_data))
                
                # Fotoğrafı kaydet
                image_path = 'qr_code.png'
                image.save(image_path)
                
                # Kullanıcıya QR kodunu gönder
                bot.send_photo(message.chat.id, open(image_path, 'rb'))
            else:
                bot.reply_to(message, "QR kodu oluşturulurken bir hata oluştu.")
        else:
            bot.reply_to(message, f"Hata oluştu. API yanıt kodu: {response.status_code}")
    
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")












@bot.message_handler(commands=['sms'])
def handle_sms(message):
    # Komuttan gelen telefon numarasını al
    command = message.text.split()
    if len(command) != 2 or not command[1].isdigit():
        bot.reply_to(message, "Lütfen geçerli bir telefon numarası girin! Örnek: /sms 5333333333")
        return

    phone = command[1]
    api_url = f"https://tungsten-good-sheet.glitch.me/sms?phone={phone}"

    # "Gönderiliyor..." mesajını gönder
    sent_message = bot.reply_to(message, "Gönderiliyor...")

    try:
        response = requests.get(api_url)
        # API yanıtını kontrol et
        if response.status_code == 200:
            json_response = response.json()
            if "✅" in json_response.get("message", ""):
                # Başarıyla dönerse, "Bombardıman başarılı ✅" mesajı ve GIF'i aynı anda gönder
                bot.edit_message_text("Bombardıman başarılı ✅", sent_message.chat.id, sent_message.message_id)
                bot.send_animation(sent_message.chat.id, "https://media.tenor.com/SWiGXYOM8eMAAAAC/russia-soviet.gif")
            else:
                # Eğer başarılı değilse
                bot.edit_message_text("SMS gönderilemedi!", sent_message.chat.id, sent_message.message_id)
        else:
            bot.edit_message_text("SMS gönderilemedi!", sent_message.chat.id, sent_message.message_id)
    except requests.exceptions.RequestException:
        # Hata durumunda
        bot.edit_message_text("SMS gönderilemedi!", sent_message.chat.id, sent_message.message_id)











def send_long_message(chat_id, message):
    # Telegram'a gönderilecek mesaj 4096 karakterden fazla ise parçalar halinde gönder
    for i in range(0, len(message), 4096):
        bot.send_message(chat_id, message[i:i+4096])

@bot.message_handler(commands=['sokak'])
def sokak_sorgu(message):
    args = message.text.split()
    
    if len(args) < 2:
        bot.reply_to(message, "Lütfen bir TC kimlik numarası girin! Örnek: /sokak 12345678901")
        return

    tc_no = args[1]
    api_url = f"https://api.ondex.uk/ondexapi/sokaksorgu.php?tc={tc_no}"

    # User-Agent başlığını ekliyoruz
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers)
        data = response.json().get("Veri", [])

        if not data:
            bot.reply_to(message, "Bu TC numarası için sonuç bulunamadı.")
            return

        txt_content = ""
        for item in data:
            txt_content += "╭━━━━━━━━━━━━━━\n"
            txt_content += f"┃➥ Ad Soyad : {item['AdiSoyadi']}\n"
            txt_content += f"┃➥ TC: {item['KimlikNo']}\n"
            txt_content += f"┃➥ Doğum Yeri : {item['DogumYeri']}\n"
            txt_content += f"┃➥ Ikametgah : {item['Ikametgah']}\n"
            txt_content += "╰━━━━━━━━━━━━━━\n\n"

        # Eğer txt_content 4000 karakterden küçükse TXT dosyası olarak gönder
        if len(txt_content) < 4000:
            file_path = f"sokak_sorgu_{tc_no}.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(txt_content)

            with open(file_path, "rb") as file:
                bot.send_document(message.chat.id, file)

            os.remove(file_path)  # Dosyayı gönderdikten sonra sil
        else:
            # 4000 karakterden fazlaysa mesajı parçalara ayır ve gönder
            send_long_message(message.chat.id, txt_content)

    except Exception as e:
        bot.reply_to(message, "Bir hata oluştu, lütfen tekrar deneyin.")
        print(f"Hata: {e}")





def send_long_message(chat_id, message):
    # Telegram'a gönderilecek mesaj 4096 karakterden fazla ise parçalar halinde gönder
    for i in range(0, len(message), 4096):
        bot.send_message(chat_id, message[i:i+4096])







@bot.message_handler(commands=['apartman'])
def apartman_sorgu(message):
    args = message.text.split()
    
    if len(args) < 2:
        bot.reply_to(message, "Lütfen bir TC kimlik numarası girin! Örnek: /apartman 12345678901")
        return

    tc_no = args[1]
    api_url = f"https://api.ondex.uk/ondexapi/apartmansorgu.php?tc={tc_no}"

    # User-Agent başlığını ekliyoruz
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers)
        data = response.json().get("Veri", [])

        if not data:
            bot.reply_to(message, "Bu TC numarası için sonuç bulunamadı.")
            return

        txt_content = ""
        for item in data:
            txt_content += "╭━━━━━━━━━━━━━━\n"
            txt_content += f"┃➥ Ad Soyad : {item['AdiSoyadi']}\n"
            txt_content += f"┃➥ TC: {item['KimlikNo']}\n"
            txt_content += f"┃➥ Doğum Yeri : {item['DogumYeri']}\n"
            txt_content += f"┃➥ Ikametgah : {item['Ikametgah']}\n"
            txt_content += "╰━━━━━━━━━━━━━━\n\n"

        # Eğer txt_content 4000 karakterden küçükse TXT dosyası olarak gönder
        if len(txt_content) < 4000:
            file_path = f"apartman_sorgu_{tc_no}.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(txt_content)

            with open(file_path, "rb") as file:
                bot.send_document(message.chat.id, file)

            os.remove(file_path)  # Dosyayı gönderdikten sonra sil
        else:
            # 4000 karakterden fazlaysa mesajı parçalara ayır ve gönder
            send_long_message(message.chat.id, txt_content)

    except Exception as e:
        bot.reply_to(message, "Bir hata oluştu, lütfen tekrar deneyin.")
        print(f"Hata: {e}")


@bot.message_handler(commands=['hava'])
def hava_durumu(message):
    try:
        # Kullanıcıdan konum bilgisi al
        chat_id = message.chat.id
        parameters = message.text.split()[1:]

        if len(parameters) != 1:
            bot.reply_to(message, "Geçersiz komut. Örnek: /hava Baku")
            return
        
        konum = parameters[0]  # Konum bilgisi
        
        # API'yi çağır
        url = f"https://tilki.dev/api/hava-durumu?konum={konum}"
        response = requests.get(url)
        print("API Yanıt Kodu:", response.status_code)
        
        if response.status_code != 200:
            bot.reply_to(message, "API'den yanıt alınamadı. Lütfen daha sonra tekrar deneyin.")
            return
        
        data = response.json()
        
        if data.get("konum"):
            # Hava durumu, sıcaklık, konum bilgisi
            hava_durumu = data["havadurumu"]
            sicaklik = data["sicaklik"]
            enlem = data["enlem"]
            uzunluk = data["uzunluk"]
            saat_dilimi = data["saatdilimi"]
            uyari = data["uyari"] if data["uyari"] else "Yok"  # Uyarı boşsa "Yok" yaz
            gozlem_noktasi = data["gozlem_noktasi"]
            
            # Hava durumu türüne göre emoji seçme
            if "cloud" in hava_durumu.lower():
                emoji = "☁️"  # Bulutlu
            elif "rain" in hava_durumu.lower():
                emoji = "🌧️"  # Yağmurlu
            elif "snow" in hava_durumu.lower():
                emoji = "❄️"  # Kar
            elif "clear" in hava_durumu.lower():
                emoji = "🌞"  # Güneşli
            elif "storm" in hava_durumu.lower():
                emoji = "⛈️"  # Fırtına
            elif "drizzle" in hava_durumu.lower():
                emoji = "🌦️"  # Çiseliyor
            elif "fog" in hava_durumu.lower():
                emoji = "🌫️"  # Sis
            else:
                emoji = "🌤️"  # Diğer durumlar (parçalı bulutlu vb.)
            
            # Hava durumu mesajını oluştur
            result = f"""
╭━━━━━━━━━━━━━━━━━━━━━
┃ Hava Durumu:
┃
┃➥ Konum: {data['konum']}
┃➥ Enlem: {enlem}, Uzunluk: {uzunluk}
┃➥ Hava Durumu: {hava_durumu} {emoji}
┃➥ Sıcaklık: {sicaklik}°C
┃➥ Gözlem Noktası: {gozlem_noktasi}
┃➥ Saat Dilimi: {saat_dilimi}
┃➥ Uyarı: {uyari}
╰━━━━━━━━━━━━━━━━━━━━━
            """
            
            bot.send_message(chat_id, result.strip())
        else:
            bot.reply_to(message, "Hava durumu verisi alınamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")







@bot.message_handler(commands=['hikaye'])
def hikaye_sorgu(message):
    args = message.text.split()
    
    if len(args) < 2:
        bot.reply_to(message, "Lütfen bir TC kimlik numarası girin! Örnek: /hikaye 12345678901")
        return

    tc_no = args[1]
    api_url = f"https://api.ondex.uk/ondexapi/hayathikayesisorgu.php?tc={tc_no}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers)
        
        # JSON olup olmadığını kontrol et
        try:
            data = response.json()
        except json.JSONDecodeError:
            bot.reply_to(message, "Sunucudan geçerli bir yanıt alınamadı.")
            return

        # "Veri" içinde "hikaye" anahtarı olup olmadığını kontrol et
        if "Veri" not in data or "hikaye" not in data["Veri"]:
            bot.reply_to(message, "Bu TC numarası için sonuç bulunamadı.")
            return

        hikaye = data["Veri"]["hikaye"]

        # Boşlukları ekleyerek metni formatla
        formatted_hikaye = hikaye.replace("  ", "\n\n")  # Çift boşlukları paragraflar arasında boşlukla değiştir

        # Eğer mesaj 4000 karakterden azsa direkt gönder
        if len(formatted_hikaye) < 4000:
            bot.send_message(message.chat.id, f"📖 Hayat Hikayesi:\n\n{formatted_hikaye}")
        else:
            # Eğer 4000 karakterden uzunsa parçalayarak gönder
            for part in [formatted_hikaye[i:i+4000] for i in range(0, len(formatted_hikaye), 4000)]:
                bot.send_message(message.chat.id, part)

    except Exception as e:
        bot.reply_to(message, "Bir hata oluştu, lütfen tekrar deneyin.")
        print(f"Hata: {e}")





@bot.message_handler(commands=['sorguil'])
def sorguil_handler(message):
    args = message.text.split()
    
    # args[0] = /sorguil, args[1]=ad, args[2]=il, args[3]=ilçe (opsiyonel)
    if len(args) < 3:
        bot.reply_to(message, "Lütfen doğru formatta kullanın: /sorguil <ad> <il> [ilçe]")
        return

    ad = args[1]
    il = args[2]
    ilce = args[3] if len(args) >= 4 else ""
    
    # API URL'sini oluşturuyoruz
    api_url = f"http://talaruscheck.site/apiler/adililce.php?ad={ad}&il={il}&ilce={ilce}"
    
    # User-Agent başlığını ekleyelim
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        data = response.json()
        
        if not data.get("success", False) or not data.get("data"):
            bot.reply_to(message, "Sonuç bulunamadı.")
            return
        
        txt_content = ""
        # Tüm kayıtları döngüyle ekleyelim
        for person in data["data"]:
            txt_content += "╭━━━━━━━━━━━━━━━━━━━━━\n"
            txt_content += f"┃➥ Ad Soyad     : {person['ADI']} {person['SOYADI']}\n"
            txt_content += f"┃➥ TC           : {person['TC']}\n"
            txt_content += f"┃➥ Doğum Tarihi : {person['DOGUMTARIHI']}\n"
            txt_content += f"┃➥ Nüfus İl     : {person['NUFUSIL']}\n"
            txt_content += f"┃➥ Nüfus İlçe   : {person['NUFUSILCE']}\n"
            txt_content += f"┃➥ Anne Adı     : {person['ANNEADI']} - TC: {person['ANNETC']}\n"
            txt_content += f"┃➥ Baba Adı     : {person['BABAADI']} - TC: {person['BABATC']}\n"
            txt_content += f"┃➥ Uyruk        : {person['UYRUK']}\n"
            txt_content += "╰━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Eğer tüm API cevabı 4000 karakterden fazlaysa, txt dosyası oluşturup gönder
        if len(txt_content) > 4000:
            file_path = f"sorguil_{ad}_{il}.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(txt_content)
            with open(file_path, "rb") as file:
                bot.send_document(message.chat.id, file)
            os.remove(file_path)
        else:
            # 4000 karakterden azsa direkt mesaj olarak gönder
            bot.send_message(message.chat.id, txt_content)

    except Exception as e:
        bot.reply_to(message, "Bir hata oluştu, lütfen tekrar deneyin.")
        print(f"Hata: {e}")











# /universite komutu
@bot.message_handler(commands=['universite'])
def universite_sorgu(message):
    try:
        chat_id = message.chat.id
        tc_number = message.text.split()[1]  # TC numarasını komuttan alın

        url = f"https://siberizim.online/esrarkes/uni.php?tc={tc_number}"

        # User-Agent başlığı ekleyin
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        # Yanıtın ne olduğunu kontrol edelim
        print("API Yanıtı:", response.text)

        # JSON'a dönüştürme işlemi
        try:
            data = response.json()
        except ValueError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        if "universite_bilgileri" in data:
            university_data = data["universite_bilgileri"]
            tcpro_data = data["tcpro_bilgileri"]

            result_text = f"""\
╭━━━━━━━━━━━━━━
┃➥ Adı: {university_data['Ad']}
┃➥ Soyadı: {university_data['Soyad']}
┃➥ TC No: {university_data['TC No']}
┃➥ Doğum Tarihi: {university_data['Doğum Tarihi']}
┃➥ Baba Adı: {university_data['Baba Adı']}
┃➥ Anne Adı: {university_data['Anne Adı']}
┃➥ Bölüm: {university_data['Bölüm']}
┃➥ Aile Sıra No: {tcpro_data['Aile Sıra No']}
┃➥ Birey Sıra No: {tcpro_data['Birey Sıra No']}
┃➥ Medeni Hal: {tcpro_data['Medeni Hal']}
┃➥ Cinsiyet: {tcpro_data['Cinsiyet']}
┃➥ GSM: {tcpro_data['GSM'] if tcpro_data['GSM'] else 'Bilgi Yok'}
╰━━━━━━━━━━━━━━"""

            bot.reply_to(message, result_text)
        else:
            bot.reply_to(message, "Bu TC numarasına ait üniversite bilgileri bulunamadı.")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /universite <tc_numarası>")
    except Exception as e:
        print(f"Üniversite sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")











# /ttnet komutu
@bot.message_handler(commands=['ttnet'])
def ttnet_sorgu(message):
    try:
        chat_id = message.chat.id
        query = message.text.split(maxsplit=1)  # Kullanıcıdan gelen sorguyu al

        # Eğer kullanıcı eposta ile sorgulama yapıyorsa
        if "@" in query[1]:
            url = f"https://siberizim.online/esrarkes/ttnet.php?eposta={query[1]}"

        # Eğer kullanıcı ad soyad ile sorgulama yapıyorsa
        else:
            url = f"https://siberizim.online/esrarkes/ttnet.php?adsoyad={query[1]}"

        # User-Agent başlığı ekleyin
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        # Yanıtın ne olduğunu kontrol edelim
        print("API Yanıtı:", response.text)

        # JSON'a dönüştürme işlemi
        try:
            data = response.json()
        except ValueError:
            bot.reply_to(message, "API'den geçersiz bir yanıt alındı. Lütfen tekrar deneyin.")
            return

        result_text = ""
        if "EPOSTA" in data[0]:
            # Eposta sorgusu yapıldıysa
            for item in data:
                result_text += f"""\
╭━━━━━━━━━━━━━━
┃➥ Eposta: {item['EPOSTA']}
┃➥ GSM: {item['GSM']}
┃➥ Adres: {item['ADRES']}
┃➥ Şehir: {item['SEHIR']}
╰━━━━━━━━━━━━━━
"""
        elif "ADSOYAD" in data[0]:
            # Ad Soyad sorgusu yapıldıysa
            for item in data:
                result_text += f"""\
╭━━━━━━━━━━━━━━
┃➥ Ad Soyad: {item['ADSOYAD']}
┃➥ GSM: {item['GSM']}
┃➥ Adres: {item['ADRES']}
┃➥ Şehir: {item['SEHIR']}
╰━━━━━━━━━━━━━━
"""

        # Eğer metin 4000 karakterden fazla ise, txt dosyasına kaydedip gönderelim
        if len(result_text) > 4000:
            # Dosyaya yazma
            with open("result.txt", "w", encoding="utf-8") as file:
                file.write(result_text)

            # Dosyayı gönderme
            with open("result.txt", "rb") as file:
                bot.send_document(chat_id, file)
            
            # Dosyayı sildik
            os.remove("result.txt")
        else:
            # Eğer metin 4000'den küçükse, direkt olarak mesaj olarak gönder
            bot.reply_to(message, result_text)

    except IndexError:
        bot.reply_to(message, "Geçersiz komut. Kullanım: /ttnet <ad soyad veya eposta>")
    except Exception as e:
        print(f"TTNet sorgulama hatası: {str(e)}")
        bot.reply_to(message, "Bir hata oluştu.")
















@bot.message_handler(commands=['check'])
def check_sorgusu(message):
    try:
        # Kullanıcıdan kart numarasını al
        card_number = message.text.split()[1]
        
        # API URL'si
        url = f"https://www.xchecker.cc/api.php?cc={card_number}"
        headers = {
            'user-agent': 'Mozilla/5.0'
        }
        
        # API'yi çağır
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()  # API yanıtını JSON olarak al
            cc_number = data.get("ccNumber", "Bilinmiyor")
            bank_name = data.get("bankName", "Bilinmiyor")
            status = data.get("status", "Bilinmiyor")
            details = data.get("details", "Bilinmiyor")

            if status.lower() == "live":
                status_text = "✅ 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝"
            else:
                status_text = "❌ 𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝"

            # Mesaj formatını değiştirdik
            result_text = f"""
╭━━━━━━━━━━━━━━
┃➥ Kart Numarası: {cc_number}
┃➥ Durum: {status_text}
┃➥ Yanıt: {status}
┃➥ Zaman: {response.elapsed.total_seconds():.2f} saniye
╰━━━━━━━━━━━━━━
            """
            bot.reply_to(message, result_text)
        else:
            bot.reply_to(message, f"❗ Error (Status: {response.status_code})")
    except IndexError:
        bot.reply_to(message, "Geçersiz kart numarası. Kullanım: /check  1111000011110000|01|30|000")
    except Exception as e:
        bot.reply_to(message, "Bir hata oluştu.")
        print(f"Check sorgulama hatası: {e}")






@bot.message_handler(commands=['dns'])
def dns_sorgu(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "⚠️ Lütfen bir domain adı girin!\nÖrnek: `/dns google.com`", parse_mode="Markdown")
            return
        
        domain = args[1]
        url = f"https://api.ondex.uk/ondexapi/dnssorgu.php?host={domain}"

        # User-Agent ekleyerek istek atıyoruz
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("status") != "OK":
            bot.reply_to(message, "⚠️ Geçersiz veya bulunamayan domain.", parse_mode="Markdown")
            return
        
        hostname = data.get("hostname", "Bilinmiyor")
        a_records = "\n┃➥ ".join([f"{r['address']} (TTL: {r['ttl']})" for r in data["records"].get("A", [])]) or "Bulunamadı"
        mx_records = "\n┃➥ ".join([f"{r['exchange']} (Öncelik: {r['priority']})" for r in data["records"].get("MX", [])]) or "Bulunamadı"
        ns_records = "\n┃➥ ".join([r['nameserver'] for r in data["records"].get("NS", [])]) or "Bulunamadı"
        soa_record = data["records"].get("SOA", [{}])[0]
        soa_info = f"{soa_record.get('nameserver', 'Bulunamadı')} | {soa_record.get('hostmaster', 'Bulunamadı')}"

        result_text = f"""
╭━━━━━━━━━━━━━━
┃🌐 *DNS Sorgu Sonucu*
┃➥ *Hostname:* {hostname}
┃
┃📍 *A Kayıtları:*  
┃➥ {a_records}
┃
┃📧 *MX Kayıtları:*  
┃➥ {mx_records}
┃
┃🖥 *NS Kayıtları:*  
┃➥ {ns_records}
┃
┃🔧 *SOA Kayıtları:*  
┃➥ {soa_info}
╰━━━━━━━━━━━━━━
"""

        bot.send_message(message.from_user.id, result_text, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, "⚠️ Bir hata oluştu.")
        print(f"DNS sorgu hatası: {e}")












import requests

@bot.message_handler(commands=['isyeri'])
def isyeri_sorgu(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Lütfen bir TC kimlik numarası girin.\nÖrnek: `/isyeri 12345678901`", parse_mode="Markdown")
        return

    tc = args[1]
    api_url = f"https://api.ondex.uk/ondexapi/isyerisorgu.php?tc={tc}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(api_url, headers=headers)
        data = response.json()

        if "Kisi" not in data or "Isyeri" not in data:
            bot.reply_to(message, "⚠️ Geçerli bir kayıt bulunamadı.")
            return

        kisi = data["Kisi"]
        isyeri = data["Isyeri"]

        result_text = f"""
╭━━━━━━━━━━━━━━
┃ İŞYERİ SORGU SONUCU
┃➥ Ad Soyad: {kisi.get("AdiSoyadi", "Bilinmiyor")}
┃➥ Kimlik Numarası: {kisi.get("KimlikNumarasi", "Bilinmiyor")}
┃➥ Çalışma Durumu: {kisi.get("CalismaDurumu", "Bilinmiyor")}
┃➥ İşe Giriş Tarihi: {kisi.get("IseGirisTarihi", "Bilinmiyor")}
┃
┃ İŞYERİ BİLGİLERİ
┃➥ Ünvan: {isyeri.get("IsyeriUnvani", "Bilinmiyor")}
┃➥ Sektör: {isyeri.get("IsyeriSektoru", "Bilinmiyor")}
┃➥ Tehlike Sınıfı: {isyeri.get("TehlikeSinifi", "Bilinmiyor")}
┃➥ NACE Kodu: {isyeri.get("NaceKodu", "Bilinmiyor")}
┃➥ SGK Sicil No: {isyeri.get("IsyeriSGKSicilNo", "Bilinmiyor")}
╰━━━━━━━━━━━━━━
"""

        bot.reply_to(message, result_text)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Bir hata oluştu: {str(e)}")














@bot.message_handler(commands=['ip'])
def ip_info(message):
    args = message.text.split(maxsplit=1)
    
    # Eğer IP adresi sağlanmamışsa veya IP adresi geçersizse, işlem yapma
    if len(args) <= 1 or not is_valid_ip(args[1]):
        return  # Hiçbir şey yapmadan return ediyoruz, yani bot cevap vermez.
    
    ip_address = args[1]
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        if response.status_code == 200:
            ip_info = response.json()
            if ip_info["status"] == "success":
                # Daha okunabilir bir mesaj formatı
                formatted_message = (
                    f"🌐 **IP Bilgileri** 🌐\n"
                    f"• **IP Adresi:** {ip_info.get('query')}\n"
                    f"• **Ülke:** {ip_info.get('country')} ({ip_info.get('countryCode')})\n"
                    f"• **Bölge:** {ip_info.get('regionName')} ({ip_info.get('region')})\n"
                    f"• **Şehir:** {ip_info.get('city')}\n"
                    f"• **Posta Kodu:** {ip_info.get('zip')}\n"
                    f"• **Zaman Dilimi:** {ip_info.get('timezone')}\n"
                    f"• **ISP:** {ip_info.get('isp')}\n"
                    f"• **Organizasyon:** {ip_info.get('org')}\n"
                    f"• **Koordinatlar:** {ip_info.get('lat')}, {ip_info.get('lon')}\n"
                    f"• **AS Bilgisi:** {ip_info.get('as')}\n"
                )
                bot.send_message(message.chat.id, formatted_message, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "IP bilgisi bulunamadı.")
        else:
            bot.send_message(message.chat.id, f"API hatası: {response.status_code}")
    except Exception as e:
        bot.send_message(message.chat.id, f"API isteği sırasında bir hata oluştu: {e}")


# IP adresinin geçerliliğini kontrol eden fonksiyon
def is_valid_ip(ip):
    # IP adresi formatının geçerli olup olmadığını kontrol eder
    if re.match(r"^(?!.*[^\d\.])(?=\d{1,3}(\.\d{1,3}){3}$)(?!.*\.\.)(?!^\.)[0-9.]+$", ip):
        return True
    return False














@bot.message_handler(commands=['sgkyetkili'])
def sgk_yetkili_sorgu(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Lütfen bir TC kimlik numarası girin.\nÖrnek: `/sgkyetkili 12345678901`", parse_mode="Markdown")
        return

    tc = args[1]
    api_url = f"https://api.ondex.uk/ondexapi/isyeriyetkilisorgu.php?tc={tc}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if "Veri" not in data or not data["Veri"]:
            bot.reply_to(message, "⚠️ Geçerli bir kayıt bulunamadı.")
            return

        yetkili_listesi = data["Veri"]
        result_text = f"""
╭━━━━━━━━━━━━━━
┃ 📌 İŞYERİ YETKİLİ SORGUSU
┃━━━━━━━━━━━━━━
"""

        for yetkili in yetkili_listesi:
            result_text += f"""┃➥ 👤 Yetkili: {yetkili.get("AdiSoyadi", "Bilinmiyor")}
┃➥ 🆔 Kimlik No: {yetkili.get("KimlikNumarasi", "Bilinmiyor")}
┃➥ 📍 Yetkililik Durumu: {yetkili.get("YetkililikDurumu", "Bilinmiyor")}
┃➥ 🔹 Yetkili Türü: {yetkili.get("YetkiliTuru", "Bilinmiyor")}
┃➥ 🏷 Yetkili Kodu: {yetkili.get("YetkiliKodu", "Bilinmiyor")}
┃━━━━━━━━━━━━━━
"""

        result_text += "╰━━━━━━━━━━━━━━"

        bot.reply_to(message, result_text)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Bir hata oluştu: {str(e)}")









        



while True:
    try:
        bot.polling(none_stop=True, timeout=10, long_polling_timeout=10)
    except Exception as e:
        print(f"Hata oluştu: {e}")
        time.sleep(5)  # 5 saniye bekleyip tekrar başlat
