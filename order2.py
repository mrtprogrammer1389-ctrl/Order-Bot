from data_base import data_base
from balethon import Client
from balethon.objects import (
    callback_query,
    Message,
    InlineKeyboard,
    InlineKeyboardButton,
)
from balethon.conditions import is_joined


def main_program():

    bot = Client(token="857605699:75p7HaW_EOCThH0Jk83GMGseKA3TSrsXyz0")

    data_manager = data_base()

    admins = ["5403313784"]

    @bot.on_message(condition=is_joined(admins[0]))
    async def handel_admins(message: Message):

        content = str(message.text)

        chat_id = str(message.chat.id)

        if content == "/inline_orders":

            inline_orders = data_manager.get_inline_orders()

            nones = [[], {}, (), "", None, (())]

            if inline_orders not in nones:

                for order in inline_orders:

                    text = (
                        "اطلاعات سفارش💬:"
                        + "\n" * 2
                        + f"✅ آیدی: {order[0]}"
                        + "\n"
                        + f"✅ عنوان: {order[4]}"
                        + "\n"
                        + f"✅ توضیحات: {order[5]}"
                        + "\n" * 2
                        + f"✅ مبلغ پیشنهادی: {order[6]}"
                        + "\n"
                        + f"✅ وضعیت پیشرفت: {order[7]}"
                        + "\n"
                        + f"✅ وضعیت توافق: {order[8]}"
                        + "\n"
                        + f"نام فرستنده💬: {order[1]}"
                        + "\n"
                        + f"نام کاربری فرستنده📝: @{order[2]}"
                        + "\n"
                        + f"چت آیدی فرستنده💬⏰: {order[3]}"
                    )

                    global markup

                    markup = InlineKeyboard(
                        [
                            [
                                InlineKeyboardButton(
                                    text="پذیرش پروژه✅",
                                    callback_data=f"accept_order:{order[0]}",
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="رد کردن پروژه❌",
                                    callback_data=f"disapprove_order:{order[0]}",
                                )
                            ],
                        ]
                    )

                    await bot.send_message(
                        chat_id=str(chat_id), text=text, reply_markup=markup
                    )
            else:

                await bot.send_message(chat_id=chat_id, text="سفارشی یافت نشد⚠️🫡")

    @bot.on_callback_query(condition=is_joined(admins[0]))
    async def admin_callbacks(callback_query):

        callback_data = str(callback_query.data)

        order_id = callback_data.replace("accept_order:", "")

        if "accept_order:" in callback_data:

            order_id = callback_data.replace("accept_order:", "")

            data_manager.accept_order(order_id)

        else:

            order_id = callback_data.replace("disapprove_order:", "")

            data_manager.disapprove_order(order_id)

    bot.run()


main_program()
