import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from uuid import uuid4
from shared_docs_bot.service import doc_list_markup, validate_action_on_single_doc


UPDATE_DOC = "UPDATE_DOC"


def list_docs_to_update(update, context):
    docs = list(context.chat_data.keys())

    update.message.reply_text(
        "Select a document to update" if docs else "No document to display.",
        reply_markup=doc_list_markup(
            docs, callback_data_func=lambda doc: f"{UPDATE_DOC} {doc}"
        ),
    )


def update_doc(update, context):
    query = update.callback_query

    doc_name = validate_action_on_single_doc(update, context, UPDATE_DOC)
    if not doc_name:
        return

    text = context.chat_data.get(doc_name)["text"]

    keyboard = [
        [
            InlineKeyboardButton(
                "Click to update document above",
                switch_inline_query_current_chat=doc_name + "\n" + text,
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.chat_data[doc_name]["text"],
        reply_markup=reply_markup,
    )
    query.answer()


def update_inline(update, context):
    query = update.inline_query.query
    filename, text = query.split("\n", 1)
    filename = filename.strip(" ")
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Update",
            input_message_content=InputTextMessageContent("/update_content " + query),
        )
    ]
    update.inline_query.answer(results)


def update_content(update, context):
    try:
        command, message_data = update.message.text.split(" ", 1)
        filename, text = message_data.split("\n", 1)
        filename = filename.strip(" ")
        if not context.chat_data.get(filename):
            update.reply_text(f"Doc {filename} does not exist")
            return
        context.chat_data[filename] = {
            "text": text,
            "from": update.message.from_user.to_dict(),
        }
        update.message.reply_text(f"Doc {filename} has been updated")
    except Exception as e:
        logging.exception(e)
        update.message.reply_text("An error occured")
