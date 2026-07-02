from sqlite3 import connect
import os
import json


class data_base:

    def __init__(self):

        self.title = "date_base"
        self.path = os.getcwd()
        self.name = "orders.db"
        self.data_path = self.path + "\\" + self.name

        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::base tables

        self.dat = connect(self.data_path)

        self.cursor = self.dat.cursor()

        cmd = """CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT,
            sender_username TEXT,
            sender_chat_id TEXT,
            project_title TEXT,
            project_describtion TEXT,
            suggestion_amount TEXT,
            status_of_process TEXT,
            accept TEXT,
            is_deleted TEXT 


        )"""

        self.cursor.execute(cmd)
        self.dat.commit()

    def add_order(
        self,
        sender_name,
        sender_username,
        sender_chat_id,
        project_title,
        project_describtion,
        suggestion_amount,
    ):

        cmd = """INSERT INTO orders (sender_name, sender_username, sender_chat_id, project_title, project_describtion, suggestion_amount, status_of_process, accept, is_deleted) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        print(sender_chat_id + "hello")

        self.cursor.execute(
            cmd,
            (
                str(sender_name),
                str(sender_username),
                str(sender_chat_id),
                str(project_title),
                str(project_describtion),
                str(suggestion_amount),
                "Not finished",
                "not seen yet",
                "False",
            ),
        )

        self.dat.commit()

        return "oreder added"

    def update_order_item(self, id, column, data):

        cmd = f"""UPDATE orders SET {column}=? WHERE id = ?"""

        self.cursor.execute(cmd, (str(data), int(id)))

        self.dat.commit()

    def delete_order(self, id):

        self.update_order_item(id, "is_deleted", "True")

    def accept_order(self, id):

        self.update_order_item(id, "accept", "True")
        self.update_order_item(id, "status_of_process", "coding")

    def disapprove_order(self, id):

        self.update_order_item(id, "accept", "False")

    def done_order(self, id):

        self.update_order_item(id, "status_of_process", "Done")

    def get_user_order(self, chat_id):

        cmd = """SELECT * FROM orders WHERE sender_chat_id = ? AND is_deleted <> ?"""

        self.cursor.execute(cmd, (str(chat_id), "True"))

        user_orders = self.cursor.fetchall()

        print(user_orders)

        return user_orders

    def get_inline_orders(self):

        cmd = """SELECT * FROM orders WHERE is_deleted <> 'True' AND accept <> 'False' AND accept <> 'True' AND status_of_process <> 'Done'"""

        self.cursor.execute(cmd)

        in_line_orders = self.cursor.fetchall()

        return in_line_orders

    def get_order_by_username(self, username):

        cmd = """SELECT * FROM orders WHERE sender_username = ? AND is_deleted <> 'True'"""

        self.cursor.execute(cmd, (str(username),))

        users_order = self.cursor.fetchall()

        return users_order

    def get_order_by_id(self, id):

        cmd = "SELECT * FROM orders WHERE id = ?"

        self.cursor.execute(cmd, (int(id),))

        return self.cursor.fetchall()[0]

    def get_accepted_orders(self):

        cmd = """SELECT * FROM orders WHERE accept = 'True' AND is_deleted <> 'True'"""

        self.cursor.execute(cmd)

        return self.cursor.fetchall()

    def get_all_users_chat_id(self):

        cmd = """SELECT sender_chat_id FROM orders"""

        self.cursor.execute(cmd)

        return tuple(set(self.cursor.fetchall()))

    def test(self):

        cmd = "SELECT * FROM orders"

        self.cursor.execute(cmd)

        print(self.cursor.fetchall())

a = data_base()

a.test()