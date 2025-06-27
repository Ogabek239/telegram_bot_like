from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler,
)
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query

load_dotenv()
token = os.getenv("token")

count_db = TinyDB("count_db.json")
user_db = TinyDB("user_db.json")

User = Query()

if not count_db:
    count_db.insert({"like": 0, "dislike": 0})

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    full_name = update.message.from_user.full_name
    
    if not user:
        user_db.insert({
            "chat_id": chat_id,
            "username": username,
            "full_name": full_name,
            "choice": None
        })
    bot = context.bot

    keyboard1 = InlineKeyboardButton(
        f"dislike 👎 {g_dislike}", callback_data="1dislike"
    )
    keyboard2 = InlineKeyboardButton(f"like 👍 {d_like}", callback_data="1like")
    reply_markup = InlineKeyboardMarkup([[keyboard1, keyboard2]])

    bot.send_message(
        chat_id=chat_id,
        text="Hello @" + update.message.chat.username,
        reply_markup=reply_markup,
    )


def query(update: Update, context: CallbackContext):
    global g_dislike, d_like

    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
        button = update.callback_query.data

        if button == "1like":
            current_choice = "like"
        elif button == "1dislike":
            current_choice = "dislike"
        else:
            return

        for user1 in user_db:
            if user1["chat_id"] == chat_id:
                user = user1
            return


        
        user = user_list[0]
        previous_choice = user.get("choice")

        if previous_choice == current_choice:
            return

        if previous_choice == "like":
            d_like -= 1
        elif previous_choice == "dislike":
            g_dislike -= 1

        if current_choice == "like":
            d_like += 1
        else:
            g_dislike += 1

        count_db.truncate()
        count_db.insert({"like": d_like, "dislike": g_dislike})

        user_db.update({"choice": current_choice}, lambda u: u["chat_id"] == chat_id)

        keyboard1 = InlineKeyboardButton(
            f"dislike 👎 {g_dislike}", callback_data="1dislike"
        )
        keyboard2 = InlineKeyboardButton(f"like 👍 {d_like}", callback_data="1like")
        reply_markup = InlineKeyboardMarkup([[keyboard1, keyboard2]])

        update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)


updater = Updater(token=token)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(callback=query, pattern="1"))

updater.start_polling()
updater.idle()
