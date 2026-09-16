async def spam_loop(chat_id, context):
    global is_spamming
    bot_index = 0
    while is_spamming:
        if bot_index > 4:
            bot_index = 0
        try:
            bot = context.bot_data['bots'][bot_index]
            texts = SPAM_TEXTS[bot_index]
            # GỘP TẤT CẢ CÂU THÀNH 1 TIN NHẮN DUY NHẤT
            message = "\n".join(texts)
            await bot.send_message(chat_id=chat_id, text=message)
            await asyncio.sleep(0.1)
            bot_index += 1
        except RetryAfter as e:
            print(f"Bot {bot_index+1} bị chặn, chuyển bot khác...")
            bot_index += 1
        except Exception as e:
            print(f"Lỗi bot {bot_index+1}: {e}")
            bot_index += 1
