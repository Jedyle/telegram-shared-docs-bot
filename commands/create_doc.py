import logging


def create_doc(update, context):
    if len(context.args) < 1:
        logging.warning(f"Invalid number of arguments : {update.message.text}")
        update.message.reply_text(
            "Usage: /create_doc <filename_to_save>\n"
            "Exemple : /create_doc List of good bars in Paris"
        )
        return

    _, document = update.message.text.split(" ", 1)
    if context.chat_data.get(document):
        logging.warning(f"Document already exists {document}")
        update.message.reply_text(
            "This document already exists in this chat, use /update_doc to change it."
        )
        return

    context.chat_data[document] = {
        "text": "Empty doc... Please fill!",
        "from": update.message.from_user.to_dict(),
    }
    update.message.reply_text(
        text=f"Empty message has been saved as '{document}'.",
    )
