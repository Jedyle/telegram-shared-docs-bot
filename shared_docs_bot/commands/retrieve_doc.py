from shared_docs_bot.service import doc_list_markup, validate_action_on_single_doc


GET_DOC = "GET_DOC"


def list_docs_to_retrieve(update, context):
    docs = list(context.chat_data.keys())

    update.message.reply_text(
        "Select a document to open" if docs else "No document to display.",
        reply_markup=doc_list_markup(
            docs, callback_data_func=lambda doc: f"{GET_DOC} {doc}"
        ),
    )


def retrieve_doc(update, context):
    query = update.callback_query

    doc_name = validate_action_on_single_doc(update, context, GET_DOC)
    if not doc_name:
        return

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=context.chat_data[doc_name]["text"]
    )
    query.answer()
