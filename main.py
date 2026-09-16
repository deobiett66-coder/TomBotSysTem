import os
import asyncio
from telegram import Update, Bot
from telegram.error import RetryAfter
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN_1 = os.getenv("TOKEN_1")
TOKEN_2 = os.getenv("TOKEN_2")
TOKEN_3 = os.getenv("TOKEN_3")
TOKEN_4 = os.getenv("TOKEN_4")
TOKEN_5 = os.getenv("TOKEN_5")

TOKENS = [TOKEN_1, TOKEN_2, TOKEN_3, TOKEN_4, TOKEN_5]
MY_UID = 8352636820

SPAM_TEXTS = [
    # Bot 1: 5 câu, tất cả in đậm
    [
        "**Địt mẹ cái giống loài này mình sao rich ra đẻ bụi các đạo thái à con chó rách =))=))**",
        "**Con đĩ mẹ mày đẻ ra mày lục đàng phê thuốc hay ngậm các thê hằng độc cứt =))=))**",
        "**Địt mẹ cái mặt mày nhìn như cái bồn cầu công cộng ai qua cụng ỉ nhà vậy em =))=))**",
        "**Thằng chó đẻ hãm lồn, bú liếm cái bãi rác xả hội mà cả tưởng mình thượng đẳng à =))=))**",
        "**Địt mẹ mày ngậm chặt cái mồm thối hoắc bốc mùi cứt trôi sông lại đi con lồn lồi =))=))**"
    ],
    # Bot 2: 30 câu in đậm
    ["**𝐓𝐨𝐦𝐌𝐨𝐝.𝐍𝐨1 😂🤪**"] * 30,
    # Bot 3: 30 câu in đậm
    ["**𝘽ạ𝙞 𝙏𝙤𝙢 𝙍ồ𝙞 À𝙖 ⌨**"] * 30,
    # Bot 4: 30 câu in đậm
    ["**Ả𝗼 𝗠ạ𝗻𝗴 𝗫ã 𝗛ộ𝗶 À 𝗘𝗺 𓀢𓀠**"] * 30,
    # Bot 5: 30 câu in đậm
    ["**TonMod Hot Mạng Xã Hội 🪷**"] * 30,
]

is_spamming = False


async def delete_cmd(update):
    try:
        if update.message and update.effective_user and update.effective_user.id == MY_UID:
            await update.message.delete()
    except Exception as e:
        print(f"Lỗi xóa: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    await update.message.reply_text("HỆ THỐNG 5 BOT: Sẵn sàng!")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    user = update.effective_user
    text = (
        f"👑 **THÔNG TIN CHỦ SỞ HỮU**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🆔 UID: `{user.id}`\n"
        f"📛 Tên: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'Không có'}\n"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def auto_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    context.bot_data['auto_delete'] = True
    await update.message.reply_text("Đã BẬT auto xóa.")


async def auto_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    context.bot_data['auto_delete'] = False
    await update.message.reply_text("Đã TẮT auto xóa.")


async def delete_by_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if context.bot_data.get('auto_delete', False):
        if update.effective_user and update.effective_user.id == MY_UID:
            try:
                await update.message.delete()
            except:
                pass


async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_spamming
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    if is_spamming:
        return
    is_spamming = True
    asyncio.create_task(spam_loop(update.effective_chat.id, context))


async def spam_loop(chat_id, context):
    global is_spamming
    bot_index = 0
    while is_spamming:
        if bot_index > 4:
            bot_index = 0
        try:
            bot = context.bot_data['bots'][bot_index]
            texts = SPAM_TEXTS[bot_index]
            # GỘP 30 CÂU THÀNH 1 TIN NHẮN
            message = "\n".join(texts[:30])
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
            await asyncio.sleep(0.1)
            bot_index += 1
        except RetryAfter as e:
            print(f"Bot {bot_index+1} bị chặn, chuyển bot khác...")
            bot_index += 1
        except Exception as e:
            print(f"Lỗi bot {bot_index+1}: {e}")
            bot_index += 1


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_spamming
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    is_spamming = False


if __name__ == "__main__":
    bots = [Bot(token) for token in TOKENS if token]
    app = ApplicationBuilder().token(TOKEN_1).build()
    app.bot_data['bots'] = bots
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("f", info))
    app.add_handler(CommandHandler("o", auto_on))
    app.add_handler(CommandHandler("t", auto_off))
    app.add_handler(CommandHandler("all", spam))
    app.add_handler(CommandHandler("dall", stop))
    app.add_handler(MessageHandler(filters.ALL, delete_by_uid))
    app.run_polling()
