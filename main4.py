from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
import os

# Carregar os documentos da web
loader = WebBaseLoader("https://www.cccoliseuinformatica.com.br/")
lista_documentos = loader.load()
documento = ''.join(doc.page_content for doc in lista_documentos)

# Configurar a API do LangChain
api_key = "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"
os.environ["GROQ_API_KEY"] = api_key

chat = ChatGroq(model='llama-3.3-70b-versatile')
template = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente amigável chamado OficinaMicroBot, que tem acesso às seguintes informações para dar suas respostas: {documentos_informados}'),
    ('user', '{input}')
])

chain = template | chat

# Função para processar mensagens
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text  # Mensagem do usuário
    try:
        resposta = chain.invoke({'documentos_informados': documento, 'input': user_message})
        await update.message.reply_text(resposta.content)  # Resposta do LangChain
    except Exception as e:
        await update.message.reply_text(f"Erro ao processar sua mensagem: {e}")

# Função inicial do bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Olá! Eu sou o OficinaMicroBot. Pergunte-me algo sobre a loja!")

# Configurar o bot
def main():
    TOKEN = "7131894683:AAE1MdN-DghbLqSk3oxH2kXWCRB13F1OqyE"  # Substitua pelo token do BotFather
    app = ApplicationBuilder().token(TOKEN).build()

    # Registrar os comandos e handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar o bot
    print("Bot iniciado...")
    app.run_polling()

if __name__ == '__main__':
    main()

