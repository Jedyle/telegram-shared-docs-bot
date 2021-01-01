import logging
from service import doc_list_markup, validate_action_on_single_doc


DELETE_DOC = "DELETE_DOC"


def list_docs_for_deletion(update, context):
    docs = list(context.chat_data.keys())

    update.message.reply_text(
        "Select a document to delete",
        reply_markup=doc_list_markup(
            docs,
            callback_data_func=lambda doc: f"{DELETE_DOC} {doc}",
            doc_name_func=lambda doc: f"DELETE '{doc}'",
        ),
    )


def delete_doc(update, context):
    query = update.callback_query
    query.answer()

    doc_name = validate_action_on_single_doc(update, context, DELETE_DOC)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=context.chat_data.pop(doc_name)["text"]
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="This document was deleted successfully."
    )
    query.answer()
