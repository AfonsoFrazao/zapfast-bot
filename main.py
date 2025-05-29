import requests
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Dicionário de saldo (simulado)
user_balances = {}

def get_balance(user_id):
    return user_balances.get(user_id, 0.0)

def set_balance(user_id, amount):
    user_balances[user_id] = amount

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_balances:
        set_balance(user_id, 0.0)

    keyboard = [
        ["🔥 Serviços", "💰 Saldo"],
        ["🔁 Recarregar", "📘 Dicas de Uso"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False
    )
    await update.message.reply_text(
        "👋 Bem-vindo ao ZapFast!\nEscolha uma opção abaixo:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "🔥 Serviços":
        keyboard = [
            [InlineKeyboardButton("WhatsApp", callback_data="whatsapp"),
             InlineKeyboardButton("Instagram", callback_data="instagram")],
            [InlineKeyboardButton("Telegram", callback_data="telegram"),
             InlineKeyboardButton("Facebook", callback_data="facebook")],
            [InlineKeyboardButton("Google/YouTube/Gmail", callback_data="google")],
            [InlineKeyboardButton("Nubank/Inter/PicPay", callback_data="bancos")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Escolha o serviço desejado:", reply_markup=reply_markup)

    elif text == "💰 Saldo":
        balance = get_balance(user_id)
        await update.message.reply_text(f"💰 Seu saldo atual é: R$ {balance:.2f}")

    elif text == "🔁 Recarregar":
        set_balance(user_id, get_balance(user_id) + 10.99)
        await update.message.reply_text("✅ R$ 10,99 adicionados ao seu saldo com sucesso!")

    elif text == "📘 Dicas de Uso":
        await update.message.reply_text("💡 Dica: Use os serviços com atenção ao país e plataforma desejados.")

async def service_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    service = query.data
    await query.answer()

    balance = get_balance(user_id)
    price = 10.99

    if balance >= price:
        new_balance = balance - price
        set_balance(user_id, new_balance)
        await query.edit_message_text(
            f"✅ Compra de número para *{service.upper()}* autorizada!\n\n"
            f"💸 R$ {price:.2f} foi debitado do seu saldo.\n"
            f"💰 Saldo atual: R$ {new_balance:.2f}\n\n"
            "📦 Aguarde o envio do número virtual..."
        )
    else:
        keyboard = [[InlineKeyboardButton("💰 Recarregar Saldo", callback_data="recarregar")]]
        await query.edit_message_text(
            f"❌ Saldo insuficiente para comprar número de {service.title()}.\n\n"
            f"💰 Seu saldo atual: R$ {balance:.2f}\n"
            "Para continuar, recarregue seu saldo:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def inline_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "recarregar":
        user_id = query.from_user.id
        set_balance(user_id, get_balance(user_id) + 10.99)
        await query.edit_message_text("✅ R$ 10,99 recarregados com sucesso!\nTente novamente a compra agora.")

# TOKEN DO BOT
BOT_TOKEN = "7293365088:AAFvTLxHmRpDi4jyn_ZLZ4eFFxbll68CZUc"

# EXECUÇÃO DO BOT
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(CallbackQueryHandler(service_handler))
app.add_handler(CallbackQueryHandler(inline_callback, pattern="recarregar"))

app.run_webhook(
    listen="0.0.0.0",
    port=10000,
    webhook_url="https://zapfast-bot.onrender.com/"
)
