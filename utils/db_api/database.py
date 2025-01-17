import sqlite3


class DataBase:
    def __init__(self, path: str):
        self.path = path

    def __connection(self):
        return sqlite3.connect(self.path)

    def __execute(self, sql: str, fetchone=False, fetchall=False, commit=False):
        conn = self.__connection()
        cursor = conn.cursor()
        data = None
        cursor.execute(sql)

        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        if commit:
            conn.commit()
        conn.close()
        return data

    def add_user(self, telegram_id: int, name: str, age: int, gender: str, roommate_gender: str,
                 smoking: int, number_of_rooms: str, about: str, photo_id: str, how_long: str,
                 location: str, local_location: str, pet: str, budget: str, found: str):
        sql = f"""
        INSERT INTO questionnaires(telegram_id, name, age, gender, roommate_gender, smoking, rooms_number, about,
         photo_id, how_long, location, local_location, pet, budget, found )
        VALUES ({telegram_id}, '{name}', {age}, '{gender}', '{roommate_gender}', {smoking}, '{number_of_rooms}', '{about}',
         '{photo_id}', '{how_long}', '{location}', '{local_location}', '{pet}', '{budget}', '{found}')
        """
        self.__execute(sql, commit=True)

    def questionnaire_in_table(self, telegram_id: int = None, search_id: int = -1, roommate_gender: str = None, user_gender: str = None) -> bool:
        if search_id == -1:
            sql = f"""
            SELECT EXISTS(SELECT telegram_id FROM questionnaires
            WHERE telegram_id = {telegram_id})
            """
            return not self.__execute(sql, fetchone=True, commit=True)[0] == 0
        else:
            return not self.get_next_questionnaire_by_search_id(search_id, roommate_gender, telegram_id, user_gender) is None

    def get_questionnaire_by_user_id(self, telegram_id: int):
        sql = f"""
        SELECT * FROM questionnaires
        WHERE telegram_id = {telegram_id}
        """
        return self.__execute(sql, fetchone=True, commit=True)

    def delete_questionnaire(self, telegram_id: int):
        sql = f"""
            DELETE FROM questionnaires
            WHERE telegram_id = {telegram_id};
        """
        self.__execute(sql, commit=True)

    def change_field(self, field_name: str, field_value: str, telegram_id: int):
        sql = f"""
        UPDATE questionnaires
        SET {field_name} = {field_value}
        WHERE telegram_id = {telegram_id}
        """
        self.__execute(sql, commit=True)

    def get_next_questionnaire_by_search_id(self, search_id: int, roommate_gender: str, ignore_tg_id: int, user_gender: str):
        if roommate_gender == "Неважно":
            sql = f"""
                SELECT * FROM questionnaires
                WHERE ID = (select min(ID) from questionnaires where ID >= {search_id} AND telegram_id != {ignore_tg_id}
                AND telegram_id NOT IN (select liked_id from likes where liker_id = {ignore_tg_id})
                AND roommate_gender IN ('{user_gender}', 'Неважно'))
            """
        else:
            sql = f"""
            SELECT * FROM questionnaires
            WHERE gender = '{roommate_gender}'
            AND ID = (select min(ID) from questionnaires where ID >= {search_id} AND telegram_id != {ignore_tg_id}
            AND telegram_id NOT IN (select liked_id from likes where liker_id = {ignore_tg_id})
            AND roommate_gender IN ('{user_gender}', 'Неважно'))
            """
        return self.__execute(sql, fetchone=True, commit=True)

    def questionnaire_by_search_id(self, search_id: int):
        sql = f"""
        SELECT * FROM questionnaires
        WHERE ID = {search_id}
        """
        return self.__execute(sql, fetchone=True, commit=True)

    def add_reported(self, telegram_id: int):
        sql = f"""
        INSERT OR IGNORE INTO reported(telegram_id)
        VALUES ({telegram_id})
        """
        return self.__execute(sql, commit=True)

    def get_next_reported_que(self):
        sql = f"""
        SELECT * FROM reported
        WHERE ID = (SELECT min(ID) FROM reported)
        """
        return self.__execute(sql, fetchone=True, commit=True)

    def delete_from_reported(self, telegram_id: int):
        sql = f"""
        DELETE FROM reported
        WHERE telegram_id = {telegram_id}
        """
        return self.__execute(sql, commit=True)

    def add_like(self, liker_id: int, liked_id: int):
        sql = f"""
        INSERT OR IGNORE INTO likes
        VALUES ({liker_id}, {liked_id})
        """
        return self.__execute(sql, commit=True)
