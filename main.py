from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7293365088:AAFvTLxHmRpDi4jyn_ZLZ4eFFxbll68CZUc"

# Lista de serviços com preços
servicos = {
    "WhatsApp": 12.99,
    "Instagram": 13.99,
    "Telegram": 7.99,
    "Facebook": 12.99,
    "Google/YouTube/Gmail": 10.99,
    "Nubank / Inter / PicPay": 14.99
}

# Teclado principal
main_keyboard = [
    ["🔥 Serviços", "💰 Saldo"],
    ["🔁 Recarregar", "📘 Dicas de Uso"]
]
main_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

# Teclado de serviços
def gerar_menu_servicos():
    botoes = [
        [InlineKeyboardButton(serv1, callback_data=serv1), InlineKeyboardButton(serv2, callback_data=serv2)]
        for serv1, serv2 in zip(list(servicos.keys())[::2], list(servicos.keys())[1::2])
    ]
    return InlineKeyboardMarkup(botoes)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bem-vindo ao ZapFast!\nEscolha uma opção abaixo:", reply_markup=main_markup)

# Resposta ao botão "Serviços"
async def responder_servicos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔥 Serviços":
        await update.message.reply_text(
            "👋 Olá! Bem-vindo ao *ZapFast*.\nEscolha o serviço desejado abaixo:",
            reply_markup=gerar_menu_servicos(),
            parse_mode="Markdown"
        )

# Callback dos botões de serviços
async def servico_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    servico = query.data
    valor = servicos.get(servico, 0)

    await query.edit_message_text(
        f"📍 País: Brasil\n"
        f"⚙️ Serviço: {servico}\n"
        f"💵 Valor: R$ {valor:.2f}\n"
        f"📱 Operadora: Qualquer Operadora\n\n"
        f"✅ 274 Disponíveis!\n"
        f"NOTA: Os valores variam de acordo com o país. Use o botão '📍 Países' para mais informações.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 RECEBER SMS", callback_data=f"receber_{servico}")],
            [InlineKeyboardButton("❌ Cancelar", callback_data="cancelar")]
        ])
    )

# Resposta ao botão "📘 Dicas de Uso"
async def dicas_uso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "📘 Dicas de Uso":
        await update.message.reply_text(
            "📘 *Dicas de Uso do ZapFast*\n\n"
            "🔹 Use o *menu principal* para navegar entre as opções.\n"
            "🔹 Ao clicar em *Serviços*, escolha o aplicativo desejado e depois selecione *Receber SMS* para gerar o número virtual.\n"
            "🔹 Certifique-se de ter saldo suficiente antes de gerar um número. Você pode verificar ou recarregar na opção *Recarregar*.\n"
            "🔹 Após gerar o número, use ele no app selecionado e aguarde o recebimento do SMS.\n"
            "🔹 Caso precise de ajuda, use o botão de *Afiliados* para suporte ou orientações.\n\n"
            "ℹ️ Os créditos são utilizados por serviço. Verifique os valores antes de cada compra.",
            parse_mode="Markdown"
        )

# Inicialização do bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🔥 Serviços"), responder_servicos))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📘 Dicas de Uso"), dicas_uso))
app.add_handler(CallbackQueryHandler(servico_callback))
app.run_polling()
