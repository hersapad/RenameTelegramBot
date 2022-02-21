from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
Merhaba! {}

{} botuna hoşgeldiniz!

Belgeleri ve diğer bazı özelliklere sahip dosyaları yeniden adlandırmak için beni kullanabilirsiniz.. Öğrenmek için `/help` yazın !


    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton(text="🏠 Ana sayfaya dön 🏠", callback_data="home")],
    ]

    # Rest Buttons
    buttons = [
        [
            InlineKeyboardButton("Nasıl kullanılır?", callback_data="help"),
            InlineKeyboardButton("🎪 Hakkında 🎪", callback_data="about")
        ]
    ]

    # Help Message
    HELP = """
Yeniden adlandırmak için bir dosya gönderin. Bot, dosyayı yeniden adlandıracaktır.

1) Dosyanıza küçük resim eklemek için bir resim gönderin ve /thumbnail komutu ile resmi yanıtlayın.
2) Videolarınız standart olarak video formatında yüklenecektir. Bunu değiştirmek için /settings komutunu kullanın.

✨ **Kullanılabilir Komutlar** ✨

/thumbnail - Küçük resim ayarları
/settings - Bot ayarları
/about - Bot Hakkında
/help - Yardım Mesajı
/start - Botu Başlat
    """

    # About Message
    ABOUT = """
**About This Bot** 

Bu bot, telegramdaki dosyalarınızı yeniden adlandırma konusunda size yardımcı olacaktır.

    """
