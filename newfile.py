print("starting bot...")
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8402788211:AAF_gK47Uw-rck9ZYqhuk2G0m_7mCI226kU"
CHANNEL = "@noughtretails"

# ---- START COMMAND ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL[1:]}")],
        [InlineKeyboardButton("✅ Verify Membership", callback_data="verify")]
    ]

    text = (
        f"🔥 *Welcome {user}!* 🔥\n\n"
        "🎁 *NOUGHT RETAILS GIVEAWAY BOT*\n\n"
        "📌 *How to participate:*\n"
        "1️⃣ Join our Telegram channel\n"
        "2️⃣ Click *Verify Membership*\n"
        "3️⃣ Get access to giveaways 🤑\n\n"
        "👇 Tap below to continue"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ---- VERIFY FUNCTION ----
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)

        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text(
                "🎉 *Verification Successful!*\n\n"
                "✅ You are now eligible for giveaways 🤑\n\n"
                "📢 Stay active in the channel!",
                parse_mode="Markdown"
            )
        else:
            await query.answer(
                "❌ You must join the channel first!",
                show_alert=True
            )

    except Exception as e:
        await query.answer(
            "⚠️ Bot error! Make sure bot is admin.",
            show_alert=True
        )

# ---- RUN BOT ----
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify, pattern="verify"))

print("🤖 Bot is running...")
app.run_polling()
