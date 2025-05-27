
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7862970938:AAEM6nt5pxM-0msXg9w9hhlJyi_YJ0J6j94"
FIVESIM_API_KEY = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Nzk4MDY3NzQsImlhdCI6MTc0ODI3MDc3NCwicmF5IjoiOWI5OWQzYzZiMTRkM2E4M2RlMThhNGNiOWJhMDRmZGEiLCJzdWIiOjMyNDUzODh9.FY1nfeNlEgTOEJzyTr1VvdTXJRGK3FePQEdY8U7H0kkHGbxMhv9FplRl_vn4YvE10nTaMbQkIAcitnUKy0duFTivUfVb_KmHZEfd5tZB-1Gf6bxOmL7WnXonCvTXQsRoyiJzpCOUdhMj2NXhk7aw9ZDIpPqmEFQbmGQRPovrzds15fknM2vrXPVad5i0WN1IKRV0JxvaOHuM5osjmJXbn9g1r-vvxwFbxD69ciPQOL4iDh_oxL-GDWDCBk13UrjWKVsuJmNgc7RTJfcnj5w6W8Nu_dVcR4Rn-Hp16fchnx-u7wbZWlpakb68mw1YhLWV2KQb1868Vj5dKLW5IJm0SA"

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

app.run_webhook(listen="0.0.0.0", port=10000, webhook_url="https://zapfast-bot.onrender.com/")
