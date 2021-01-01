import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    InlineQueryHandler,
    CommandHandler,
    PicklePersistence,
    CallbackQueryHandler,
)
from commands.retrieve_doc import GET_DOC, list_docs_to_retrieve, retrieve_doc
from commands.create_doc import create_doc
from commands.update_doc import (
    UPDATE_DOC,
    list_docs_to_update,
    update_doc,
    update_inline,
    update_content,
)
from commands.delete_doc import DELETE_DOC, list_docs_for_deletion, delete_doc

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def help_text(update, context):
    help_message = """/help - Get a help message
/list_docs - List all docs (and show one)
/create_doc - Create new empty doc
/update_doc - Update an existing doc's content
/delete_doc - Delete a doc
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)


def main():
    updater = Updater(
        TELEGRAM_BOT_TOKEN,
        persistence=PicklePersistence("drive_data"),
        use_context=True,
    )
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_text))
    dispatcher.add_handler(CommandHandler("create_doc", create_doc))

    dispatcher.add_handler(CommandHandler("list_docs", list_docs_to_retrieve))
    dispatcher.add_handler(
        CallbackQueryHandler(
            retrieve_doc, pattern=rf"^{GET_DOC} \S.+", pass_chat_data=True
        )
    )

    dispatcher.add_handler(CommandHandler("delete_doc", list_docs_for_deletion))
    dispatcher.add_handler(
        CallbackQueryHandler(
            delete_doc, pattern=rf"^{DELETE_DOC} \S.+", pass_chat_data=True
        )
    )

    dispatcher.add_handler(CommandHandler("update_doc", list_docs_to_update))
    dispatcher.add_handler(
        CallbackQueryHandler(
            update_doc, pattern=rf"^{UPDATE_DOC} \S.+", pass_chat_data=True
        )
    )

    dispatcher.add_handler(CommandHandler("update_content", update_content))

    dispatcher.add_handler(InlineQueryHandler(update_inline))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
