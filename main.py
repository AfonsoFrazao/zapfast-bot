import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7293365088:AAFvTLxHmRpDi4jyn_ZLZ4eFFxbll68CZUc"
FIVESIM_API_KEY = "SUA_API_KEY_AQUI"  # Substitua pela sua API Key válida da 5sim

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔥 Serviços", "📊 Saldo"],
        ["💳 Recarregar", "📍 Países"],
        ["🤝 Afiliados", "📘 Dicas de Uso"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text("⌛ Carregando menu...")
    await update.message.reply_text(
        "👋 Olá! Bem-vindo ao ZapFast.\nEscolha uma das opções abaixo para começar:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    service = query.data

    # Pagamento via Pix para WhatsApp
    if service == "whatsapp":
        await query.edit_message_text(
            "✅ Para continuar, envie o pagamento de R$ 11,00 via Pix:\n\n"
            "🏦 *Chave Pix*: `40752756800`\n"
            "🔖 *Nome*: ZapFast\n\n"
            "📩 Após o pagamento, aguarde o recebimento do número virtual."
        )
        return  # Interrompe o processo até pagamento

    headers = {"Authorization": f"Bearer {FIVESIM_API_KEY}"}
    response = requests.get(f"https://5sim.net/v1/user/check/{service}", headers=headers)

    if response.status_code == 200:
        await query.edit_message_text(f"Número para {service} reservado com sucesso! (simulado)")
    else:
        await query.edit_message_text("Erro ao conectar com a 5sim. Verifique sua API Key.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_webhook(
    listen="0.0.0.0",
    port=10000,
    webhook_url="https://zapfast-bot.onrender.com/"
)
