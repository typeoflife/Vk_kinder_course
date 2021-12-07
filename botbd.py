import sqlite3

class BotBD:

    def __init__(self, bd_file):
        """коннект с бд"""
        self.connect = sqlite3.connect(bd_file)
        self.cursor = self.connect.cursor()

    def user_add(self, user_id, candidate_id):
        self.cursor.execute("INSERT INTO 'users' ('user_id', 'candidate_id') VALUES(?, ?)", (user_id, candidate_id))
        return self.connect.commit()

    def candidate_add(self, candidate):
        self.cursor.execute("INSERT INTO 'candidate' ('candidate') VALUES(?)", (candidate,))
        return self.connect.commit()

    def check_candidate(self, candidate):
        result = self.cursor.execute("SELECT candidate FROM candidate WHERE candidate=?", (candidate,))
        return bool(result.fetchall())

    def see_table_info(self, table):
        for value in self.cursor.execute(f"SELECT * FROM {table}"):
            return value

    def see_candidate_id(self, canditate):
        result = self.cursor.execute("SELECT id FROM candidate WHERE candidate=?", (canditate,))
        return result.fetchone()[0]

    def user_exists(self, user):
        result = self.cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user,))
        return bool(result.fetchall())

    def user_delite(self, user):
        self.cursor.execute("DELETE FROM users WHERE user_id=?", (user,))
        return self.connect.commit()

    def candidate_delite(self, candidate):
        self.cursor.execute("DELETE FROM candidate WHERE candidate=?", (candidate,))
        return self.connect.commit()

bot = BotBD("user_ids.db")

# print(bot.see_candidate_id('id377021'))