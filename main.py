import requests
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = "7293365088:AAFvTLxHmRpDi4jyn_ZLZ4eFFxbll68CZUc"
FIVESIM_API_KEY = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Nzk4MDY3NzQsImlhdCI6MTc0ODI3MDc3NCwicmF5IjoiOWI5OWQzYzZiMTRkM2E4M2RlMThhNGNiOWJhMDRmZGEiLCJzdWIiOjMyNDUzODh9.FY1nfeNlEgTOEJzyTr1VvdTXJRGK3FePQEdY8U7H0kkHGbxMhv9FplRl_vn4YvE10nTaMbQkIAcitnUKy0duFTivUfVb_KmHZEfd5tZB-1Gf6bxOmL7WnXonCvTXQsRoyiJzpCOUdhMj2NXhk7aw9ZDIpPqmEFQbmGQRPovrzds15fknM2vrXPVad5i0WN1IKRV0JxvaOHuM5osjmJXbn9g1r-vvxwFbxD69ciPQOL4iDh_oxL-GDWDCBk13UrjWKVsuJmNgc7RTJfcnj5w6W8Nu_dVcR4Rn-Hp16fchnx-u7wbZWlpakb68mw1YhLWV2KQb1868Vj5dKLW5IJm0SA"

# Comando /start com menu principal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔥 Serviços", "💰 Saldo"],
        ["🔁 Recarregar", "📍 Países"],
        ["🤝 Afiliados", "📘 Dicas de Uso"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False
    )
    await update.message.reply_text("⌛ Carregando menu...")
    await update.message.reply_text(
        "👋 Olá! Bem-vindo ao *ZapFast*.\nEscolha uma das opções abaixo para começar:",
        reply_markup=reply_markup
    )

# Mensagem quando usuário digita "Serviços"
async def servicos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("WhatsApp", callback_data="whatsapp"),
            InlineKeyboardButton("Instagram", callback_data="instagram"),
        ],
        [
            InlineKeyboardButton("Telegram", callback_data="telegram"),
            InlineKeyboardButton("Facebook", callback_data="facebook"),
        ],
        [
            InlineKeyboardButton("Google/YouTube/Gmail", callback_data="google"),
            InlineKeyboardButton("Nubank / Inter / PicPay", callback_data="bancos"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Olá! Bem-vindo ao *ZapFast*.\nEscolha o serviço desejado abaixo:",
        reply_markup=reply_markup
    )

# Quando o usuário clica em um botão do InlineKeyboard
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    service = query.data

    # Simulação de pagamento apenas para WhatsApp
    if service == "whatsapp":
        await query.edit_message_text(
            "✅ Para continuar, envie o pagamento de R$ 11,00 via Pix:\n\n"
            "🔑 *Chave Pix:* 40752756800\n"
            "📛 *Nome:* ZapFast\n\n"
            "🕓 Após o pagamento, aguarde o recebimento do número virtual."
        )
        return

    # Simulação de verificação de número para demais serviços
    headers = {"Authorization": f"Bearer {FIVESIM_API_KEY}"}
    response = requests.get(f"https://5sim.net/v1/user/check/{service}", headers=headers)

    if response.status_code == 200:
        await query.edit_message_text(f"Número para {service} reservado com sucesso! (simulado)")
    else:
        await query.edit_message_text("Erro ao conectar com a 5sim. Verifique sua API Key.")

# Construção da aplicação
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🔥 Serviços"), servicos))
app.add_handler(CallbackQueryHandler(button))

app.run_webhook(
    listen="0.0.0.0",
    port=10000,
    webhook_url="https://zapfast-bot.onrender.com/"
)
