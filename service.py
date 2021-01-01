import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def doc_list_markup(docs, callback_data_func, doc_name_func=lambda doc: doc):
    keyboard = [
        [
            InlineKeyboardButton(doc_name_func(doc), callback_data=callback_data_func(doc))
        ] for doc in docs
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def validate_action_on_single_doc(update, context, action_type):
    action, doc_name = update.callback_query.data.split(" ", 1)
    logging.info(action)
    logging.info(doc_name)

    if not action == action_type:
        logging.error(f"Action : {action} (expected : {action_type})")
        return

    if not context.chat_data.get(doc_name):
        logging.warning(f"Document {doc_name} does not exist.")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Document {doc_name} does not exist."
        )
        return

    return doc_name
