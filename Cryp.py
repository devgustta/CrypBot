import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import sqlite3

load_dotenv()

TELEGRAM_API_ID = os.getenv("API_ID") 
TELEGRAM_API_HASH = os.getenv("API_HASH") 
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")




app = Client(
    "Cryp_bot",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
    bot_token=TELEGRAM_BOT_TOKEN,
)

estado = {}

pages = {
    'cotacoes': {
        'fav': InlineKeyboardButton('⭐ Favoritos', callback_data='favorito'),
        'alerta': InlineKeyboardButton('⌚ Alertas', callback_data='alertas:getAlerta'),
        'url': InlineKeyboardButton('💸 Apoia-me', url='https://buymeacoffee.com/GSPBR'),
        'back': InlineKeyboardButton('🏠 Home', callback_data='home'),
        'texto': 'Informe o nome da crypto que deseja saber a cotação atual!!'
    },
    'favorito': {
        'cotacoes': InlineKeyboardButton('📈 Cotações', callback_data='cotacoes'),
        'alerta': InlineKeyboardButton('⌚ Alertas', callback_data='alertas:getAlerta'),
        'url': InlineKeyboardButton('💸 Apoia-me', url='https://buymeacoffee.com/GSPBR'),
        'back': InlineKeyboardButton('🏠 Home', callback_data='home'),
        'texto': 'Lista de modas favoritas'
    },
    'alertas': {
        'cotacoes': InlineKeyboardButton('📈 Cotações', callback_data='cotacoes'),
        'fav': InlineKeyboardButton('⭐ Favoritos', callback_data='favorito'),
        'url': InlineKeyboardButton('💸 Apoia-me', url='https://buymeacoffee.com/GSPBR'),
        'back': InlineKeyboardButton('🏠 Home', callback_data='home'),
        'texto': ''
    },
    'home': {
        'cotacoes': InlineKeyboardButton('📈 Cotações', callback_data='cotacoes'),
        'fav': InlineKeyboardButton('⭐ Favoritos', callback_data='favorito'),
        'alerta': InlineKeyboardButton('⌚ Alertas', callback_data='alertas:getAlerta'),
        'url':InlineKeyboardButton('💸 Apoia-me', url='https://buymeacoffee.com/GSPBR'),
        'texto': 'Seja Bem Vindo!\nEscolha a opção'
    }
}


@app.on_callback_query()
async def callback(client, callback_query):
    user_id = callback_query.from_user.id
    page_name = callback_query.data  # Salva a página atual do usuário
    estado[user_id] = page_name  # Salva a página no dicionário de acordo com o usuário

    #Separando algun dados necessarios
    data = callback_query.data.split(':')
    action = data[0]
    #func = data[1]

    if action == 'alertas':
        page = pages[action]
        callback_query.data = action
    page = pages[callback_query.data]
    
    if callback_query.data == 'cotacoes':
        await callback_query.message.edit_text(
            page['texto'],
            reply_markup=InlineKeyboardMarkup(
                [
                    [page['fav'], page['alerta']],
                    [page['url'], page['back']]
                ]
            )
        )
    elif callback_query.data == 'favorito':
        await callback_query.edit_message_text(
            page['texto'],
            reply_markup=InlineKeyboardMarkup(
                [
                    [page['cotacoes'], page['alerta']],
                    [page['url'], page['back']],
                ]
            )
        )
    elif callback_query.data == 'alertas':
        await callback_query.edit_message_text(
            page['texto'],
            reply_markup=InlineKeyboardMarkup(
                [
                    [page['cotacoes'], page['fav']],
                    [page['url'], page['back']]
                ]
            )
        )
    elif callback_query.data == 'home':
        await callback_query.edit_message_text(
            page['texto'],
            reply_markup=InlineKeyboardMarkup(
                [
                    [page['cotacoes'], page['fav']],
                    [page['alerta'], page['url']]
                ]
            )
        )


@app.on_message(filters.command("preço"))
async def price(client, message):
    user_id = message.from_user.id
    current_page = estado.get(user_id, 'home')

    if current_page == 'cotacoes':
        print(user_id)

        if message.text == 'bitcoin' or 'Bitcoin':
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=brl&ids=bitcoin"

            headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": "CG-RPP5icdeq6BxNv1MofCPKsm9"
            }

            response = requests.get(url, headers=headers)

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                # Converte a resposta para um dicionário Python
                data = response.json()

                # `data` é uma lista de dicionários, acessar o primeiro item
                bitcoin_data = data[0]

                # Exibe o preço atual do Bitcoin
                current_price = bitcoin_data['current_price']
                await message.reply(f"O preço atual do Bitcoin é: {current_price} BRL")
                print(f"O preço atual do Bitcoin é: {current_price} BRL ")
            else:
                print(f"Erro na requisição: {response.status_code}")
       
    else:
        await message.reply('Essa pergunta só será respondida na página cotações')

    
@app.on_message(filters.command("listar"))
async def list(client, message):
    user_id = message.from_user.id
    current_page = estado.get(user_id, 'home')
    if current_page == "favorito":
     await message.reply("LISTA DE MOEDAS FAVORITAS")

    else:
     await message.reply("Essa opção só é válida na opção Favoritos")

@app.on_message(filters.sticker)
async def sticker(client, message):
    await app.send_sticker(message.chat.id, message.sticker.file_id)

@app.on_message(filters.photo | filters.video)
async def photo_video(client, message):
    await message.reply("Espero que não seja **nuds**!😳")


@app.on_message((filters.voice | filters.audio) & filters.private)
async def audio_voice(client, message):
    await message.reply("Audio não, pls")
    
@app.on_message(filters.command("start") | filters.command("menu"))
async def start(client, message):
    inline_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('📈 Cotações', callback_data='cotacoes'),
                InlineKeyboardButton('⭐ Favoritos', callback_data='favorito')
            ],
            [
                InlineKeyboardButton('⌚ Alertas', callback_data= 'alertas:getAlerta'),
                InlineKeyboardButton('💸 Apoia-me', url='https://buymeacoffee.com/GSPBR')
            ]
        ]
    )
    print(message.chat.username, message.text)
    await app.send_animation(message.chat.id, 'https://www.criptonoticias.com/wp-content/uploads/2020/05/bitcoin-montana-rusa.gif')
    await message.reply('Seja Bem Vindo!\nEscolha a opção', reply_markup=inline_markup)
    # Conectando ao banco de dados
    conn = sqlite3.connect('infos.db')
    cursor = conn.cursor()

@app.on_message()
async def verifica_msg(client, message):
    print(message.chat.username, message.text)
    print(message.from_user.id)
    user_id = message.from_user.id
    current_page = estado.get(user_id, 'home')

    if current_page == 'cotacoes':
        await price(client, message)
    

if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        print(f"Erro ao rodar o bot: {e}")