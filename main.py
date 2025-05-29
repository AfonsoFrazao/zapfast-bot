import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7293365088:AAFvTLxHmRpDi4jyn_ZLZ4eFFxbll68CZUc"
FIVESIM_API_KEY = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9..."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📲 WhatsApp", callback_data="whatsapp")],
        [InlineKeyboardButton("📸 Instagram", callback_data="instagram")],
        [InlineKeyboardButton("✈️ Telegram", callback_data="telegram")],
        [InlineKeyboardButton("📘 Facebook", callback_data="facebook")],
        [InlineKeyboardButton("🔍 Google/YouTube/Gmail", callback_data="google")],
        [InlineKeyboardButton("🏦 Nubank / Inter / PicPay", callback_data="bancos")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Olá! Bem-vindo ao *ZapFast*.\nEscolha o serviço desejado abaixo:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    service = query.data

    if service == "whatsapp":
        await query.edit_message_text(
            "✅ Para continuar, envie o pagamento de *R$ 11,00* via Pix:\n\n"
            "🔑 *Chave Pix:* 40752756800\n"
            "📛 *Nome:* ZapFast\n\n"
            "🕓 Após o pagamento, aguarde o recebimento do número virtual."
        )
        return

    # Simulação de consulta à 5sim
    headers = {"Authorization": f"Bearer {FIVESIM_API_KEY}"}
    response = requests.get(f"https://5sim.net/v1/user/profile", headers=headers)

    if response.status_code == 200:
        await query.edit_message_text(
            f"✅ Número virtual para *{service}* reservado com sucesso! (simulado)"
        )
    else:
        await query.edit_message_text("❌ Erro ao conectar com a 5sim. Verifique sua API Key.")

# Inicialização do bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# Webhook para Render
app.run_webhook(
    listen="0.0.0.0",
    port=10000,
    webhook_url="https://zapfast-bot.onrender.com/"
)
