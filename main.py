
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "COLE_SEU_TOKEN_AQUI"
FIVESIM_API_KEY = "COLE_SUA_API_KEY_AQUI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("WhatsApp (BR)", callback_data='whatsapp')],
        [InlineKeyboardButton("Instagram (BR)", callback_data='instagram')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bem-vindo ao ZapFast! Escolha um serviço abaixo:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    service = query.data
    headers = {"Authorization": f"Bearer {FIVESIM_API_KEY}"}
    response = requests.get("https://5sim.net/v1/user/profile", headers=headers)

    if response.status_code == 200:
        await query.edit_message_text(f"Número para {service.upper()} reservado com sucesso! (simulado)")
    else:
        await query.edit_message_text("Erro ao conectar com a 5sim. Verifique sua API Key.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
