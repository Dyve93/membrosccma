from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import BOT_TOKEN
from db import *
from carteirinha import gerar_carteirinha
from datetime import datetime

criar_banco()

def start(update: Update, context: CallbackContext):
    mensagem = (
        "Bem-vindo ao sistema de membros!\n\n"
        "Comandos disponíveis:\n"
        "/add - Adicionar membro\n"
        "/edit - Editar membro\n"
        "/del - Excluir membro\n"
        "/buscar - Buscar membro\n"
        "/ativos - Listar membros ativos\n"
        "/aniversariantes - Ver aniversariantes\n"
        "/carteirinha - Ver sua carteirinha"
    )
    update.message.reply_text(mensagem)

def add(update: Update, context: CallbackContext):
    try:
        dados = ' '.join(context.args).split(',')
        nome, nasc, end, func, stat = [d.strip() for d in dados]
        user_id = update.effective_user.id
        adicionar_membro(nome, nasc, end, func, stat, user_id)
        path = gerar_carteirinha(nome, nasc, end, func, stat)
        update.message.reply_photo(photo=open(path, 'rb'), caption="Carteirinha criada!")
    except:
        update.message.reply_text("Erro! Use: /add Nome, DD/MM/AAAA, Endereço, Função, Ativo/Inativo")

def edit(update: Update, context: CallbackContext):
    try:
        dados = ' '.join(context.args).split(',')
        id_m, nome, nasc, end, func, stat = [d.strip() for d in dados]
        editar_membro(int(id_m), nome, nasc, end, func, stat)
        update.message.reply_text("Membro editado com sucesso!")
    except:
        update.message.reply_text("Erro! Use: /edit ID, Nome, DD/MM/AAAA, Endereço, Função, Ativo/Inativo")

def delete(update: Update, context: CallbackContext):
    try:
        id_m = int(context.args[0])
        excluir_membro(id_m)
        update.message.reply_text("Membro excluído com sucesso.")
    except:
        update.message.reply_text("Erro! Use: /del ID")

def ativos(update: Update, context: CallbackContext):
    membros = buscar_membros("Ativo")
    msg = "\n".join([f"{m[0]} - {m[1]} - {m[4]}" for m in membros])
    update.message.reply_text(f"Membros ativos:\n{msg}")

def aniversariantes(update: Update, context: CallbackContext):
    mes = datetime.now().month
    membros = buscar_aniversariantes(mes)
    msg = "\n".join([f"{m[1]} - {m[2]}" for m in membros])
    update.message.reply_text(f"Aniversariantes do mês:\n{msg}")

def buscar(update: Update, context: CallbackContext):
    nome = ' '.join(context.args)
    membros = buscar_por_nome(nome)
    if not membros:
        update.message.reply_text("Nenhum membro encontrado.")
        return
    for m in membros:
        path = gerar_carteirinha(m[1], m[2], m[3], m[4], m[5])
        update.message.reply_photo(photo=open(path, 'rb'), caption=f"ID: {m[0]} - {m[1]}")

def carteirinha(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    membro = buscar_por_user_id(user_id)
    if not membro:
        update.message.reply_text("Você ainda não está cadastrado. Peça para um administrador usar /add.")
        return
    path = gerar_carteirinha(membro[1], membro[2], membro[3], membro[4], membro[5])
    update.message.reply_photo(photo=open(path, 'rb'), caption=f"Sua carteirinha, {membro[1]}!")

updater = Updater(BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("add", add))
dp.add_handler(CommandHandler("edit", edit))
dp.add_handler(CommandHandler("del", delete))
dp.add_handler(CommandHandler("ativos", ativos))
dp.add_handler(CommandHandler("aniversariantes", aniversariantes))
dp.add_handler(CommandHandler("buscar", buscar))
dp.add_handler(CommandHandler("carteirinha", carteirinha))

updater.start_polling()
updater.idle()
