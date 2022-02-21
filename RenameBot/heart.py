import shutil
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from RenameBot.functions import progress
from RenameBot.database import SESSION
from RenameBot.database.users_sql import Users

extensions = ["mp4", "mkv", "avi", "pdf"]


@Client.on_message(filters.private & (filters.document | filters.video) & ~filters.edited & filters.incoming)
async def _rename(bot: Client, msg: Message):
    # New Name
    q = SESSION.query(Users).get(msg.from_user.id)
    if q.running:
        await msg.reply("Tek seferde bir dosya gönderin !", quote=True)
        return
    q.running = True
    try:
        new_name_message = await bot.ask(
            msg.chat.id,
            "Dosyanın yeni adını giriniz ! \n\nİşlemi durdurmak için `/cancel` komutunu veriniz !",
            filters=filters.user(msg.from_user.id) & filters.text,
        )
        # Cancel 1
        cancelled = await is_cancel(new_name_message)
        if cancelled:
            await new_name_message.reply("İşlem durduruldu !", quote=True)
            return
        # Extension
        if msg.video:
            old_name = msg.video.file_name
        else:
            old_name = msg.document.file_name
        new_name = new_name_message.text
        if "." in old_name:
            extension = old_name.rsplit(".", 1)[1]
            if "." not in new_name:
                new_name = new_name + "." + extension
        surely_question = await bot.send_message(
            msg.chat.id,
            f"Dosyayı '`{new_name}`' şeklinde adlandırmak istediğinize emin misiniz ? \n\nEğer yanıtınız evet ise, 'y' veya 'yes' ile, \ndeğilse, 'n' veya 'no' ile yanıtlayın.  \nIptal etmek için `/cancel` komutunu gönderin"
            f"\n\n[ Bu, yalnızca olası yazım hatalarını önlemek için sorulmaktadır. ]"
        )
        surely = await bot.listen(msg.chat.id, timeout=300, filters=filters.user(msg.from_user.id) & filters.text)
        # Cancel 2
        cancelled = await is_cancel(surely)
        if cancelled:
            await new_name_message.reply("İşlem iptal edildi !", quote=True)
            return
        if surely.text.lower() in ["n", "no"]:
            new_name = (await bot.ask(msg.chat.id, "\nDosyanın yeni adını giriniz! \n")).text
            if "." in old_name:
                extension = old_name.rsplit(".", 1)[1]
                if "." not in new_name:
                    new_name = new_name + "." + extension
        await surely_question.delete()
        await surely.delete()
        # Thumbnail
        q = SESSION.query(Users).get(msg.from_user.id)
        if q.thumbnail_status and q.thumbnail:
            thumb = BytesIO(q.thumbnail)
            thumb.name = "image.jpg"
        else:
            thumb = None
        # Downloading
        downloading = await msg.reply("**İndiriliyor...**")
        file_path = await msg.download(progress=progress, progress_args=(downloading, "İndiriliyor..."))
        await downloading.edit("**İndirildi.**")
        await downloading.delete()

        # Uploading
        uploading = await downloading.reply("**Yükleniyor...**")
        if msg.caption is None:
            caption = ""
        else:
            caption = msg.caption
        if q.video_to == "video":
            await bot.send_video(chat_id=msg.chat.id, video=file_path, file_name=new_name, caption=caption,
                                 thumb=thumb, progress=progress, progress_args=(uploading, "Yükleniyor..."))
        else:
            await bot.send_document(chat_id=msg.chat.id, document=file_path, file_name=new_name, caption=caption,
                                    thumb=thumb, progress=progress, progress_args=(uploading, "Yükleniyor..."))
        SESSION.close()
        await uploading.edit("**Yüklendi!**")
        await uploading.delete()
    except Exception as e:
        await msg.reply(
            f"Error : {e} \n\nİşlem başarısız !")
    finally:
        q = SESSION.query(Users).get(msg.from_user.id)
        q.running = False
        SESSION.commit()
        try:
            shutil.rmtree("downloads")
        except FileNotFoundError:
            pass


async def is_cancel(msg):
    if msg.text.startswith("/cancel"):
        return True
    else:
        return False
