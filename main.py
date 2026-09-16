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
    # Bot 1: 100 câu chửi cũ
    [
        "Địt mẹ cái giống loài này mình sao rich ra đẻ bụi các đạo thái à con chó rách =))=))",
        "Con đĩ mẹ mày đẻ ra mày lục đàng phê thuốc hay ngậm các thê hằng độc cứt =))=))",
        "Địt mẹ cái mặt mày nhìn như cái bồn cầu công cộng ai qua cụng ỉ nhà vậy em =))=))",
        "Thằng chó đẻ hãm lồn, bú liếm cái bãi rác xả hội mà cả tưởng mình thượng đẳng à =))=))",
        "Địt mẹ mày ngậm chặt cái mồm thối hoắc bốc mùi cứt trôi sông lại đi con lồn lồi =))=))",
        "Con mẹ mày xưa chó khách làng chơi tiếp thê mới lòi ra cái thứ quái thai như mày =))=))",
        "Địt mẹ sông bẩn thỉu rác rưởi đến mức con giòi bọ con nó chê không thèm kí sinh =))=))",
        "Thằng nhà quê rách ruột, mở mồm ra là sủa bậy như con chó ghẻ bị ngứa đái giữa đường =))=))",
        "Địt mẹ cái loài ăn bám đái khai, mặt dày hơn thớt đâm không thủng =))=))",
        "Con đĩ mẹ mày lúc mang thai mày chắc nuốt nhầm tinh trùng của một tiểu đòi trâu chó =))=))",
        "Địt mẹ cái thôi vô ơn bạc nghĩa, cần cả vảo đái bò mẹ sinh ra mày hả con =))=))",
        "Thằng mặt lồn bẩn vãy đàn bà, ra đường gặp đàn ông chắc quỳ xuống bưng chân thờ phụ sau =))=))",
        "Địt mẹ cái tướng đi lăng quăng như con giòi bọ trong hố phân trâu =))=))",
        "Con mẹ mày bán thân nuôi mồi ăn gộc chó đẻ lấy tiền mua sữa cho mày bú cạn bã =))=))",
        "Địt mẹ thằng hèn hạ chỉ đâm trốn sau bàn phím sủa đống nhớ con chó đái mặt xích =))=))",
        "Thằng óc lồn đầu đất, não toàn cứt đái cặn mứa cứt thích đi đày đời thiên hạ =))=))",
        "Địt mẹ cái loài chó đã bất thầy chó ăn cứt cắn càn sủa vớ vẩn kẹp cho băng dược =))=))",
        "Con đĩ mẹ bị người ta thông đít dọc bơ muỗng nên đẻ ra cái giống mày ngưu đột biến =))=))",
        "Địt mẹ cái quân phản phúc ăn hại, sống chật đất tốn không khí của nhân loại =))=))",
        "Thằng giặc rác một thứ, mồ mả tổ tiên mày thối hoắc bốc rùa cái lỗ đít của mày =))=))",
        "Địt mẹ cái loài đần bà hóa, đi đứng éo chạc hàng ngày bị người ta đút bát lồn =))=))",
        "Con mẹ lục đẻ ra mày xuống cống nên cái đầu mày toàn bùn nhão với dòi bọ =))=))",
        "Địt mẹ thằng ranh con chưa mọc lông đít đòi ra gió hỗn bà mả nhà người ta =))=))",
        "Thằng chó ghẻ ăn cứt đái bò, loài mày bỏ nhục nhục bọt vao mặt thằng bẩn bãi bọt =))=))",
        "Địt mẹ cái loài mặt thớt trơn trện, đi đến đâu người ta khinh bỉ đuổi như đuổi hủi đến đấy =))=))",
        "Con đĩ mẹ đang hàng chợ chó táp suốt đêm mồm lồn sấu xà ra cái giống mặt hãm =))=))",
        "Địt mẹ thằng bẩn thỉu không biết hôn thua dạy như một cục cứt trôi sông mình mất hết một trôi =))=))",
        "Thằng óc cật bò con chó lợm mồm, gây rặn, lại rước bãy gió mồi chúi khôn à =))=))",
        "Địt mẹ cái thứ bất đĩ ngồi khóc sông quê hương, bản thân không đáng một hột lỗi =))=))",
        "Con mẹ mày chức tước hưu mồi lồn vì sinh ra cái thằng con vô dụng đái và láo tặc sự =))=))",
        "Địt mẹ cái giống ký sinh trùng bám vào xã hội, nhìn mặt là muốn nhet giẻ rách vào mồm =))=))",
        "Thằng chó rách không nhà không cửa, đi xin từng bãi nước bọt thừa hè đế giật khát =))=))",
        "Địt mẹ cái mồm thối hoắc toàn mùi tôm với cứt chó lại còn thích lên mặt khôn ngoan =))=))",
        "Con đĩ mẹ mày lần đi khôn ai thèm mua nên đẻ ra mày đẻ bù chui gạt đũi =))=))",
        "Địt mẹ cái tướng ngồi ngậm mặt lên trời đớp ruồi bọng tàn rách rưới vãi lồn =))=))",
        "Thằng mặt lồn ăn cám đáng nuốt cay, cả hô nhà mày pơi lại không đáng một công lông đái =))=))",
        "Địt mẹ cái thôi chó đần rước vào xó tối sủa đông, gặp bố mày lá cúp đuôi chạy mất dép =))=))",
        "Con mẹ bị chó đái cả vào mồm lúc mang thai nên đẻ ra mày tính nết y như súc vật =))=))",
        "Địt mẹ cái thứ kê hít keo chó lù lù mẹ nó trí khôn, mồ mả mả là lạ nghệ mùi ngủ ngục =))=))",
        "Thằng rách con táp tàn làm giảng hào mồng những tối văn ôn gối khóc thét gọi tên mẹ =))=))",
        "Địt mẹ cái giống nòi đỏ bi, đi đến đâu thối đến đấy như bãi phân trâu tươi giữa hè =))=))",
        "Con đĩ mẹ bị thằng địt đến mức lòi trĩ ra ngoài nên đẻ mày ra bị đứt não bẩm sinh =))=))",
        "Địt mẹ cái thằng bất hiếu, nhìn mặt là biết kiếp sau nó cũng bị người ta đánh chết người đuổi =))=))",
        "Thằng bần tiện sống mòn sống mỏi, hằng ngày ăn cứt gạt mưa mà tưởng mình là đại gia ngầm =))=))",
        "Địt mẹ cái thứ rẻ rách không ai thèm ngó ngàng, gặp người đàng hoàng chó bố phải đeo khẩu trang =))=))",
        "Con mẹ bị đẻ ra giữa bãi tha ma đường đón rác bươm lôi ra cái bồ đàng thai hài của mày =))=))",
        "Địt mẹ cái thôi ngồi cống ngủ si, gặp bố mày lá cái mồm mày lại cúp như chó cụp đuôi =))=))",
        "Thằng chó đẻ ăn hại đái bậy, cuối đời mày chỉ xứng đáng làm phân bón cho cây rau muống cống nạng =))=))",
        "Địt mẹ cái quân lừa thầy phản bạn, loại mày sống không bằng con súc vật chết trôi sông =))=))",
        "Con đĩ mẹ hôi hết cống vì lúc đỏ không bập chết mày từ trong trứng nước cho đỡ đất đái =))=))",
        "Thằng ranh con bố chấp cả họ nhà mày xếp hàng vào đây để bố đụ tập thể một lượt 😂😂",
        "Địt mẹ cái thứ rác rưởi xã hội, vứt xuống cống cho giòi nó tha cho bẩn chết 😂😂",
        "Loại mày chỉ đáng làm đồ chơi tinh dục cho lũ chó hoang đương xó chó 😂😂",
        "Địt mẹ sáu nhà chó đái cần cán, gặp bố mày lá tê ra quân ngay lập tức 😂😂",
        "Thằng đầu đất não phẳng lỳ như thớt, nội tiếng người đéo hiểu lại thích sủa tiếng chó 😂😂",
        "Địt mẹ cái thứ một sách bú đủ, ngoài đời chắc bị người ta đảm cho hằng ngày không dám hó 😂😂",
        "Con chó ghẻ láo lắc thái thúy, luôn mẹ mày đi chợ trong sạch không khí loài người 😂😂",
        "Địt mẹ thích tỏ ra nguy hiểm nhưng thực chất chỉ là một con lợn con ải hài 😂😂",
        "Thằng nhà quê tập đòi làm sang, ra phô tường minh là hotboy hóa ra là thằng hề rách 😂😂",
        "Địt mẹ sống lỗi với anh em bạn bè, ra đường sớm muộn gì cũng bị đánh gãy tay chân 😂😂",
        "Loại mày đi đến đâu người ta khinh bỉ như nhục bọt đen đầy, nhục như vài cái lồn 😂😂",
        "Địt mẹ bố tưởng mày là chị thánh hóa chó, cái loại hạ đáng tuổi lồn sánh vai 😂😂",
        "Thằng ranh con bố cậm mồm chó lái không bố cứt lưới vứt cho cái sâu bẩy giỏi 😂😂",
        "Địt mẹ cái thứ chuyên nghiệp bố liên xuyên quốc gia, đi đâu cũng bố địt người ta 😂😂",
        "Con đĩ mẹ mày chó khóc rồng mồi đêm vì sinh ra cái thằng con vô bất tài vô ơn hại 😂😂",
        "Địt mẹ sống không bằng con súc vật, nhìn cái mặt là muốn lấy dép lào đập cho nát bét 😂😂",
        "Thằng mất thớt thích ăn cứt chùa mắm tôm, loại mày bố đảm cho không nhận ra bố đẻ 😂😂",
        "Địt mẹ cái thứ chuyên bám váy đàn bà, hèn hạ đến mức con gái nó cũng khinh 😂😂",
        "Loại mày vứt xuống cống hôi thối còn lâu nhà cái đám nước đen ngòm 😂😂",
        "Địt mẹ suốt ngày tỏa nề nản xem nhà này so bó và rung một mày cái răng sún hả con 😂😂",
        "Thằng hèn hạ chi biết rúc đầu vào mảnh hồ để sủa bậy chứ ngoài đời run như cầy sấy 😂😂",
        "Địt mẹ cái thứ ăn cháo đá bát, phản chủ muôn đời không ngóc đầu lên được 😂😂",
        "Con lợn nái sề nhà mày cái mồm thối lai cho thiên hạ nó và cái coi 😂😂",
        "Địt mẹ thích bắt tông với bố à, loại mày bố chấp cả lũ súc sinh một lúc 😂😂",
        "Thằng đầu tôm não úng thủy, học hành đéo đến đâu nên chôn ra đường làm súc vật 😂😂",
        "Địt mẹ sống bẩn thỉu như con các cục ghẻ trôi hè nắng gắt 😂😂",
        "Loại mày bố đảm cho không trượt phát nào, nằm ngửa ăn vã giữa đường như chó phèo 😂😂",
        "Địt mẹ cái đống rác rưởi đi đông, đi đến đâu rước hôi về đến đấy 😂😂",
        "Thằng óc lồn não lão thảo vệ chết mẹ mày tại trận bây giờ chó đấy mà sủa 😂😂",
        "Địt mẹ sủa to lên chó xem người ta có tát cho vỡ mồm mày không thằng hại 😂😂",
        "Con chó rách nát khốn khổ tấm bố mồng bỏ chó một cứt bay mau bây giờ 😂😂",
        "Địt mẹ cái mặt dày hơn thớt lợn quay, bị chửi ngập mặt vẫn cứ trơ ra cười hề hề 😂😂",
        "Thằng nhà quê ất ơ gốc cây công viên, đời rách một mớt mà cứ sĩ diện hão 😂😂",
        "Địt mẹ sống bẩn thỉu hèn hạ đủ tiền, loại mày sinh ra là một sự sỉ nhục cho giống loài 😂😂",
        "Loại mày sinh ra đời chỉ làm mất lỗi thề kỹ cua tao hòa và thượng đế 😂😂",
        "Địt mẹ thích kiếm lời ngon ngọt hay thích ăn đấm vô đãi bảo bố nốt tiếng 😂😂",
        "Thằng ranh con chó đẻ lái giống hồ mang nhưng tiền ăn sáng vẫn ngửa tay xin mẹ 😂😂",
        "Địt mẹ sủa ngu vài câu rồi cút rùa đi, nghe nhức cả đái tai chui không nổi 😂😂",
        "Con đĩ mẹ mày vô ơn bội nghĩa đẻ ra cái thằng ăn côn đồ như thính nhà mày 😂😂",
        "Địt mẹ sống vô đạo hướng không có tương lai, tương lai duy nhất là nhà tù hoặc nghĩa địa 😂😂",
        "Thằng già chết bằm mẹ mày đi chợ trong sạch xã hội loài người, đúng xúc vật hèn 😂😂",
        "Địt mẹ làm trò hề cho thiên hạ xem xong rồi giờ trốn ở xó nào mà khóc thế 😂😂",
        "Loại mày bố gặp đương bố chó nhân đầy, gãy xương sống mới chó buông tha 😂😂",
        "Địt mẹ sủa lắm thế cái mồm không mỏi à, hay thích để bố khâu mồm lại bảng chỉ thép 😂😂",
        "Thằng ăn hại nhà chó sung rụng, suốt ngày chỉ biết mở mồm hùa rồi hớp cháo loãng 😂😂",
        "Địt mẹ cái thứ bần rẻ lượng cho quý sứ, gặp lũi là cán chui như chó nhà hoạn nạn 😂😂",
        "Con chó rách sủa tiếp đi chó sủa cắn nhưng hèn hạ, bố đang nghe nhạc hiếu đuổi chúng sinh 😂😂",
        "Địt mẹ sống như nhục như chó cái đầu bựa rác rưởi không ai thèm nhặt 😂😂",
        "Con chó rách sủa tiếp đi chó sủa cắn nhưng hèn hạ, bố đang nghe nhạc hiếu đuổi chúng sinh 😂😂",
        "Địt mẹ sống như nhục như chó cái đầu bựa rác rưởi không ai thèm nhặt 😂😂",
        "Thằng chó đẻ ăn hại đái bậy, cuối đời mày chỉ xứng đáng làm phân bón cho cây rau muống cống nạng 😂😂"
    ],
    # Bot 2: TomMod.No1
    ["𝐓𝐨𝐦𝐌𝐨𝐝.𝐍𝐨1 😂🤪"] * 50,
    # Bot 3: Bai Tom Roi Aa
    ["𝘽ạ𝙞 𝙏𝙤𝙢 𝙍ồ𝙞 À𝙖 ⌨"] * 50,
    # Bot 4: Ao Mang Xa Hoi A Em
    ["Ả𝗼 𝗠ạ𝗻𝗴 𝗫ã 𝗛ộ𝗶 À 𝗘𝗺 𓀢𓀠"] * 50,
    # Bot 5: TomMod Hot Mọi Nền Tảng
    ["TomMod Hot Mọi Nền Tảng 🌐🪷"] * 50,
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
            for text in texts:
                if not is_spamming:
                    break
                await bot.send_message(chat_id=chat_id, text=text)
                await asyncio.sleep(0.1)
            bot_index += 1
        except RetryAfter as e:
            print(f"Bot {bot_index+1} bị chặn, chờ {e.retry_after}s, chuyển bot khác...")
            bot_index += 1
        except Exception as e:
            print(f"Lỗi bot {bot_index+1}: {e}")
            bot_index += 1
            await asyncio.sleep(1)


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
