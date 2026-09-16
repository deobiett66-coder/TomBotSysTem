import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN_BOT")
MY_UID = 8352636820


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
    await update.message.reply_text("BOT 1 (Chủ): Đã sẵn sàng!")


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
        f"🌐 Ngôn ngữ: {user.language_code}\n"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def auto_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    context.bot_data['auto_delete'] = True
    await update.message.reply_text("Đã BẬT tự động xóa tin nhắn.")


async def auto_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_UID:
        return
    await delete_cmd(update)
    context.bot_data['auto_delete'] = False
    await update.message.reply_text("Đã TẮT tự động xóa tin nhắn.")


async def delete_by_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if context.bot_data.get('auto_delete', False):
        sender_id = update.effective_user.id if update.effective_user else None
        if sender_id == MY_UID:
            try:
                await update.message.delete()
            except Exception as e:
                print(f"Không thể xóa: {e}")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("f", info))
    app.add_handler(CommandHandler("o", auto_on))
    app.add_handler(CommandHandler("t", auto_off))
    app.add_handler(MessageHandler(filters.ALL, delete_by_uid))
    app.run_polling()
