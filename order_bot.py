from bale import *
from data_base import data_base


def main():

    token = "717060369:f4VhHYuTd-026HQjB_AdAn1w2-McPI4hdko"

    data_manager = data_base()

    bot = Bot(token=token)

    admins = ["681691196", "5403313784", "890318846"]

    orders_dict = {}

    @bot.event
    async def on_message(message: Message):

        chat_id = str(message.chat_id)
        content = str(message.content)

        # print(chat_id)

        if chat_id in admins:

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

                        markups = InlineKeyboardMarkup()
                        markups.add(
                            InlineKeyboardButton(
                                text="پذیرش پروژه✅",
                                callback_data=f"accept_order:{order[0]},{order[3]}",
                            )
                        )
                        markups.add(
                            InlineKeyboardButton(
                                text="رد کردن پروژه❌",
                                callback_data=f"disapprove_order:{order[0]},{order[3]}",
                            ),
                            row=2,
                        )

                        await bot.send_message(
                            text=text, chat_id=chat_id, components=markups
                        )
                else:

                    await bot.send_message(chat_id=chat_id, text="سفارشی یافت نشد⚠️🫡")

            elif content == "/accepted_orders":

                accepted_orders = data_manager.get_accepted_orders()

                print(accepted_orders, "hello")

                nones = [[], {}, (), "", None, (())]

                if accepted_orders not in nones:

                    for order in accepted_orders:

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

                        markups = InlineKeyboardMarkup()
                        markups.add(
                            InlineKeyboardButton(
                                text="رد کردن پروژه❌",
                                callback_data=f"disapprove_order:{order[0]},{order[3]}",
                            ),
                            row=2,
                        )

                        markups.add(
                            InlineKeyboardButton(
                                text="تحویل پروژه🫡",
                                callback_data=f"done:{order[0]},{order[3]}",
                            )
                        )

                        await bot.send_message(
                            text=text, chat_id=chat_id, components=markups
                        )
                else:

                    await bot.send_message(chat_id=chat_id, text="سفارشی یافت نشد⚠️🫡")

            elif "/send_all:" in content:

                msg = content.replace("/send_all:", "")

                users = data_manager.get_all_users_chat_id()

                for i in users:

                    print(i)

                    await bot.send_message(text=msg, chat_id=str(i[0]))

                await message.reply(text=f"✅ sended to {len(users)} users.")

        else:

            if chat_id in orders_dict.keys():

                markup2 = InlineKeyboardMarkup()
                markup2.add(
                    InlineKeyboardButton(text="انصراف❌", callback_data="exit_ordering")
                )

                if orders_dict[chat_id]["step"] == "name":

                    orders_dict[chat_id]["step"] = "title"
                    orders_dict[chat_id]["datas"].append(content)
                    orders_dict[chat_id]["datas"].append(
                        str(message.from_user.username)
                    )
                    orders_dict[chat_id]["datas"].append(chat_id)

                    await message.reply(
                        text="عنوان پروژه را وارد کنید📫:", components=markup2
                    )

                elif orders_dict[chat_id]["step"] == "title":

                    orders_dict[chat_id]["step"] = "describtion"
                    orders_dict[chat_id]["datas"].append(content)

                    await message.reply(
                        text="لطفا توضیحات پروژه خود را بگویید🗞️📜:", components=markup2
                    )

                elif orders_dict[chat_id]["step"] == "describtion":

                    orders_dict[chat_id]["step"] = "amount"
                    orders_dict[chat_id]["datas"].append(content)

                    await message.reply(
                        text="لطفا بودجه یا مبلغ پیشنهادی خود برای پروژه را وارد کنید💰💵:",
                        components=markup2,
                    )

                elif orders_dict[chat_id]["step"] == "amount":

                    orders_dict[chat_id]["datas"].append(content)

                    datas = orders_dict[chat_id]["datas"]

                    print(datas)

                    data_manager.add_order(
                        datas[0], datas[1], datas[2], datas[3], datas[4], datas[5]
                    )

                    orders_dict.pop(chat_id)

                    await message.reply(
                        text="سفارش شما ثبت شد در صورت موافقت تیم برای پروژه یا عدم موافقت وضعیت براش شما ارسال خواهد شد👍✅💬"
                    )

                    markup = InlineKeyboardMarkup()
                    markup.add(
                        InlineKeyboardButton(
                            text="شفارش های شما📝⏰", callback_data=f"user_orders"
                        ),
                        row=1,
                    )
                    markup.add(
                        InlineKeyboardButton(
                            text="ثبت سفارش🖌️⚙️", callback_data="add_order"
                        ),
                        row=2,
                    )
                    markup.add(
                        InlineKeyboardButton(text="راهنما🔍", callback_data="hint"),
                        row=3,
                    )
                    markup.add(
                        InlineKeyboardButton(text="پشتیبانی🛡️", callback_data="support")
                    )

                    text = """سلام به بازوی ثبت سفارش خوش آمدید👋👋 
شما با استفاده از این بازو میتونید سفارش های خودتون رو به تیم برنامه نویسی Binary secrets برسونید.💬
این تیم تجربه زیادی در ساخت ربات های بله و تلگرام، هوش مصنوعی ، توسعه وب ، اپلیکیشن های دسکتاپ ، وب اسکرپینگ و .... داره 
✅شما میتونید با گزینه های زیر پروژه خودتون رو همراه با اطلاعات و بودجه یا قیمت پیشنهادی خودتون برای تیم ارسال کنید و در صورت موافقت ربات شما رو به تیم وصل کرده و بعد از پیش پرداخت تیم ما پروژه شما رو اونوطوری که میخواید انجام میده و حتی شما رو بهتر کردن پروژه مشاوره و پشتیبانی میکنه
ایده های خود را به واقعیت تبدیل کنید ««Binary secrets »»"""

                    await bot.send_message(
                        chat_id=message.chat_id, text=text, components=markup
                    )

                    order = datas

                    text = (
                        "سفارش جدید از راه رسید🤩💡💵:" + "\n"
                        "اطلاعات سفارش💬:"
                        + "\n" * 2
                        + f"✅ عنوان: {order[3]}"
                        + "\n"
                        + f"✅ توضیحات: {order[4]}"
                        + "\n" * 2
                        + f"✅ مبلغ پیشنهادی: {order[5]}"
                        + "\n"
                        + f"نام فرستنده💬: {order[0]}"
                        + "\n"
                        + f"نام کاربری فرستنده📝: @{order[1]}"
                        + "\n"
                        + f"چت آیدی فرستنده💬⏰: {order[2]}"
                        + "\n" * 2
                        + "برای پذیرش یا رد سفارش از طریق صندوق سفارشات اقدام کنید"
                    )

                    await bot.send_message(chat_id="5403313784", text=text)

            elif content == "/start":

                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton(
                        text="شفارش های شما📝⏰", callback_data=f"user_orders"
                    ),
                    row=1,
                )
                markup.add(
                    InlineKeyboardButton(text="ثبت سفارش🖌️⚙️", callback_data="add_order"),
                    row=2,
                )
                markup.add(
                    InlineKeyboardButton(text="راهنما🔍", callback_data="hint"), row=3
                )
                markup.add(
                    InlineKeyboardButton(text="پشتیبانی🛡️", callback_data="support")
                )

                text = """سلام به بازوی ثبت سفارش خوش آمدید👋👋 
شما با استفاده از این بازو میتونید سفارش های خودتون رو به تیم برنامه نویسی Binary secrets برسونید.💬
این تیم تجربه زیادی در ساخت ربات های بله و تلگرام، هوش مصنوعی ، توسعه وب ، اپلیکیشن های دسکتاپ ، وب اسکرپینگ و .... داره 
✅شما میتونید با گزینه های زیر پروژه خودتون رو همراه با اطلاعات و بودجه یا قیمت پیشنهادی خودتون برای تیم ارسال کنید و در صورت موافقت ربات شما رو به تیم وصل کرده و بعد از پیش پرداخت تیم ما پروژه شما رو اونوطوری که میخواید انجام میده و حتی شما رو بهتر کردن پروژه مشاوره و پشتیبانی میکنه
ایده های خود را به واقعیت تبدیل کنید ««Binary secrets »»"""

                await bot.send_message(
                    chat_id=message.chat_id, text=text, components=markup
                )

    @bot.event
    async def on_callback(callback: CallbackQuery):

        content = callback.data

        chat_id = str(callback.message.chat_id)

        if callback.data == "add_order":

            orders_dict[chat_id] = {"step": "name", "datas": []}

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(text="انصراف❌", callback_data="exit_ordering")
            )

            # text = """لطفا عنوان پروژه را وارد کنید💬:"""
            text = """لطفا نام خود را وارد کنید📝⚔️"""

            await bot.send_message(chat_id=chat_id, text=text, components=markup)

        elif callback.data == "exit_ordering":

            del orders_dict[chat_id]

            await bot.send_message(chat_id=chat_id, text="فرایند ثبت لغو شد⚠️❌")

        elif content == "user_orders":

            orders = data_manager.get_user_order(str(callback.message.chat_id))

            print(orders)

            print(str(callback.message.chat_id))

            nones = [[], {}, (), "", None, (())]

            if orders not in nones:

                for order in orders:

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
                    )

                    markups = InlineKeyboardMarkup()
                    markups.add(
                        InlineKeyboardButton(
                            text="حذف❌", callback_data=f"delete_order:{order[0]}"
                        )
                    )

                    await bot.send_message(
                        text=text, chat_id=chat_id, components=markups
                    )
            else:

                await bot.send_message(chat_id=chat_id, text="سفارشی یافت نشد⚠️🫡")

        elif "delete_order:" in content:

            pid = content.replace("delete_order:", "")

            data_manager.delete_order(pid)

            await bot.send_message(
                chat_id=chat_id, text="❌سفارش شما با این آیدی حذف شد:" + pid
            )

        elif "accept_order:" in content:

            base = content.replace("accept_order:", "").split(",")

            pid = base[0]

            chat_id2 = base[1]

            order_data = data_manager.get_order_by_id(pid)

            if order_data[9] == "True":

                await callback.message.reply(text="سفارش حذف شده است❌❌")
            else:

                data_manager.accept_order(pid)

                text = (
                    "سفارش شما با اطلاعات زیر پذیرفته شد✅👍"
                    + "\n" * 2
                    + f"✅ آیدی: {order_data[0]}"
                    + "\n"
                    + f"✅ عنوان: {order_data[4]}"
                    + "\n"
                    + f"✅ توضیحات: {order_data[5]}"
                    + "\n" * 2
                    + f"✅ مبلغ پیشنهادی: {order_data[6]}"
                    + "\n"
                    + f"✅ وضعیت پیشرفت: {order_data[7]}"
                    + "\n"
                    + f"✅ وضعیت توافق: {order_data[8]}"
                    + "\n" * 2
                    + "برای مطلع شدن از وضعیت پروژه و دادن اطلاعات بیشتر درمورد پروژه به آیدی زیر پیام بدید:"
                    + "@hfjsjahb9"
                    + "\n"
                    + "@parshanm89"
                )

                await bot.send_message(text=text, chat_id=chat_id2)

                text = (
                    "توجه به همه اعضای گروه🔊🔊 یک پروژه گرفته شد با مشخصات زیر:"
                    + "\n" * 2
                    + f"✅ آیدی: {order_data[0]}"
                    + "\n"
                    + f"✅ عنوان: {order_data[4]}"
                    + "\n"
                    + f"✅ توضیحات: {order_data[5]}"
                    + "\n" * 2
                    + f"✅ مبلغ پیشنهادی: {order_data[6]}"
                    + "\n"
                    + f"✅ وضعیت پیشرفت: {order_data[7]}"
                    + "\n"
                    + f"✅ وضعیت توافق: {order_data[8]}"
                )

                await bot.send_message(text=text, chat_id=admins[1])

        elif "done:" in content:

            base = content.replace("done:", "").split(",")

            pid = base[0]

            chat_id2 = base[1]

            order_data = data_manager.get_order_by_id(pid)

            if order_data[9] == "True":

                await callback.message.reply(text="سفارش حذف شده است❌❌")
            else:

                data_manager.done_order(pid)

                text = (
                    "سفارش شما انجام شد🫡🤩"
                    + "\n" * 2
                    + f"✅ آیدی: {order_data[0]}"
                    + "\n"
                    + f"✅ عنوان: {order_data[4]}"
                    + "\n"
                    + f"✅ توضیحات: {order_data[5]}"
                    + "\n" * 2
                    + f"✅ مبلغ پیشنهادی: {order_data[6]}"
                    + "\n"
                    + f"✅ وضعیت پیشرفت: Done"
                    + "\n"
                    + f"✅ وضعیت توافق: {order_data[8]}"
                    + "\n" * 2
                    + "@hfjsjahb9"
                    + "\n"
                    + "@parshanm89"
                )

                await bot.send_message(text=text, chat_id=chat_id2)

                await bot.send_message(
                    chat_id=admins[1],
                    text="سفارش به سلامتی انجام شد حالا پول زور وگیرین⚔️",
                )

        elif "disapprove_order:" in content:

            base = content.replace("disapprove_order:", "").split(",")

            pid = base[0]

            chat_id2 = base[1]

            order_data = data_manager.get_order_by_id(pid)

            if order_data[9] == "True":

                await callback.message.reply(text="سفارش حذف شده است❌❌")
            else:

                data_manager.disapprove_order(pid)

                text = (
                    "متاسفانه سفارش شما با اطلاعات زیر توسط تیم رد شد❌❌:"
                    + "\n" * 2
                    + f"✅ آیدی: {order_data[0]}"
                    + "\n"
                    + f"✅ عنوان: {order_data[4]}"
                    + "\n"
                    + f"✅ توضیحات: {order_data[5]}"
                    + "\n" * 2
                    + f"✅ مبلغ پیشنهادی: {order_data[6]}"
                    + "\n"
                    + f"✅ وضعیت پیشرفت: {order_data[7]}"
                    + "\n"
                    + f"✅ وضعیت توافق: {order_data[8]}"
                    + "\n" * 2
                )

                await bot.send_message(text=text, chat_id=chat_id2)

                text = (
                    "شما سفارش با مشخصات زیر را رد کردید❌🫡"
                    + "\n" * 2
                    + f"✅ آیدی: {order_data[0]}"
                    + "\n"
                    + f"✅ عنوان: {order_data[4]}"
                    + "\n"
                    + f"✅ توضیحات: {order_data[5]}"
                    + "\n" * 2
                    + f"✅ مبلغ پیشنهادی: {order_data[6]}"
                    + "\n"
                    + f"✅ وضعیت پیشرفت: {order_data[7]}"
                    + "\n"
                    + f"✅ وضعیت توافق: {order_data[8]}"
                )

                await bot.send_message(text=text, chat_id=admins[1])

        elif content == "hint":

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    text="شفارش های شما📝⏰", callback_data=f"user_orders"
                ),
                row=1,
            )
            markup.add(
                InlineKeyboardButton(text="ثبت سفارش🖌️⚙️", callback_data="add_order"),
                row=2,
            )
            markup.add(
                InlineKeyboardButton(text="راهنما🔍", callback_data="hint"), row=3
            )
            markup.add(InlineKeyboardButton(text="پشتیبانی🛡️", callback_data="support"))

            text = """سلام به بازوی ثبت سفارش خوش آمدید👋👋 
شما با استفاده از این بازو میتونید سفارش های خودتون رو به تیم برنامه نویسی Binary secrets برسونید.💬
این تیم تجربه زیادی در ساخت ربات های بله و تلگرام، هوش مصنوعی ، توسعه وب ، اپلیکیشن های دسکتاپ ، وب اسکرپینگ و .... داره 
✅شما میتونید با گزینه های زیر پروژه خودتون رو همراه با اطلاعات و بودجه یا قیمت پیشنهادی خودتون برای تیم ارسال کنید و در صورت موافقت ربات شما رو به تیم وصل کرده و بعد از پیش پرداخت تیم ما پروژه شما رو اونوطوری که میخواید انجام میده و حتی شما رو بهتر کردن پروژه مشاوره و پشتیبانی میکنه
ایده های خود را به واقعیت تبدیل کنید ««Binary secrets »»"""

            await bot.send_message(
                chat_id=callback.message.chat_id, text=text, components=markup
            )

        elif content == "support":

            text = """✳️برای گرفتن ارتباط با پشتیبانی تیم ««Binary secrets»» به یکی از آیدی های زیر پیام دهید:💬🤖
@hfjsjahb9
@parshanm89"""

            await bot.send_message(chat_id=chat_id, text=text)

    bot.run()


main()
