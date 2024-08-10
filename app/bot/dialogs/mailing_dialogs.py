from aiogram_dialog import Dialog, Window


mailing_dialog = Dialog(
    Window(
        Const("Введите сообщение"),
        TextInput(
            id="letter",
            on_success=Next(),
            filter=F.text.len() >= 10
        ),
        state=LetterStatesGroup.LETTER,
    ),
    Window(
        DynamicMedia("photo", when="photo"),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=8,
        ),
        Format("<blockquote>{letter}</blockquote>"),
        Button(Const("📷Прикрепить скриншот"), id="photo", on_click=sent_photo),
        Button(Const("📨Отправить"), id="send", on_click=confirm_letter),
        Cancel(Const("❌Отменить")),
        state=LetterStatesGroup.SEND,
    ),
    Window(
        Const('Отправьте скриншот'),
        DynamicMedia("photo", when="photo"),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=8,
        ),
        Button(
            Format("🗑️ Delete photo #{media_number}"),
            id="del",
            on_click=on_delete_photo,
            when="media_count",
        ),
        MessageInput(on_input_photo, content_types=[ContentType.PHOTO]),
        Back(Const("⬅️ Назад"), when="photo"),
        state=LetterStatesGroup.SCREEN,
    ),
    getter=get_letter,
)
