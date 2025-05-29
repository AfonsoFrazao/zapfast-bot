import requests
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = "7293365088:AAFvTLxHmRpDi4jyn_ZLZ4eFFxbll68CZUc"

user_data = {}

service_prices = {
    "whatsapp": 12.99,
    "instagram": 13.99,
    "telegram": 7.99,
    "facebook": 12.99,
    "google": 10.99,
    "nubank": 14.99
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔥 Serviços", "💰 Saldo"],
        ["🔁 Recarregar", "📘 Dicas de Uso"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Bem-vindo ao ZapFast!\nEscolha uma opção abaixo:", reply_markup=reply_markup)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text == "🔥 serviços":
        keyboard = [
            [
                InlineKeyboardButton("WhatsApp", callback_data="servico_whatsapp"),
                InlineKeyboardButton("Instagram", callback_data="servico_instagram")
            ],
            [
                InlineKeyboardButton("Telegram", callback_data="servico_telegram"),
                InlineKeyboardButton("Facebook", callback_data="servico_facebook")
            ],
            [
                InlineKeyboardButton("Google/YouTube/Gmail", callback_data="servico_google"),
                InlineKeyboardButton("Nubank / Inter / PicPay", callback_data="servico_nubank")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 Olá! Bem-vindo ao *ZapFast*.\nEscolha o serviço desejado abaixo:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("servico_"):
        servico = data.replace("servico_", "")
        user_data[query.from_user.id] = {"servico": servico}
        preco = service_prices.get(servico, 0.00)

        msg = (
            f"🌎 *País:* Brasil\n"
            f"⚙️ *Serviço:* {servico.capitalize()}\n"
            f"💵 *Valor:* R$ {preco:.2f}\n"
            f"📱 *Operadora:* Qualquer Operadora\n\n"
            f"✅ 274 Disponíveis!\n"
            f"NOTA: Os valores variam de acordo com o país. Use /paises"
        )

        keyboard = [
            [InlineKeyboardButton("RECEBER SMS", callback_data="receber_sms")],
            [InlineKeyboardButton("OPERADORAS", callback_data="operadoras")],
            [InlineKeyboardButton("CANCELAR", callback_data="cancelar")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=msg, reply_markup=reply_markup, parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, message_handler))
app.add_handler(CallbackQueryHandler(callback_handler))
app.run_webhook(
    listen="0.0.0.0",
    port=10000,
    webhook_url="https://zapfast-bot.onrender.com/"
)
