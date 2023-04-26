
import os
import openai
from database import Database
import sqlite3
import re

openai.api_key = os.environ['api_key']

def thread_db(fn):
    def set_up(self, *args, **kwargs):
        con = sqlite3.connect("dedoose_data.db")
        cur = con.cursor()
        con.create_function('regexp', 2, lambda x, y: 1 if re.search(x,y) else 0)
        thread_cur = fn(self, con, cur, *args, **kwargs)
        con.close()
        return thread_cur
    return set_up

class Demographics:
    def __init__(self) -> None:
        self.database = Database()
        self.uuids = self.database.get_user('', True)

    @thread_db
    def update_table(self, con, cur):
        #cur.execute("DROP table IF EXISTS demographics")
        cur.execute("""
            CREATE TABLE demographics AS
            SELECT uuid, interview_name, 'unknown' as sex, 'unknown' as age, 'unknown' as marital_status, 'unknown' as widow, 'unknown' as children, 'unknown' as religion, 'unknown' as ethnicity, 'unknown' as profession
            FROM users;
        """)
        con.commit()

    @thread_db
    def update_data(self, con, cur, column, data, uuid):
        cur.execute("""
            UPDATE demographics
            SET {} = ?
            WHERE uuid = ?
        """.format(column), (data, uuid))
        con.commit()
    
    @thread_db
    def get_data(self, con, cur, column, uuid):
        cur.execute("""
                SELECT {} FROM demographics WHERE uuid = ?
            """.format(column), (uuid, ))
        val = cur.fetchone()
        if val is None:
            raise Exception("No data found for this interview name")
        return val[0]


    def _scrape_data(self, qid):
        data = {}
        for user in self.uuids:
            res = ''
            try:
                res = self.database.get_responses(user, qid)
            except:
                pass   
            data[user] = res
        return data

    def user_details(self):
        demo_q = [768766, 818556, 127515, 737666, 866648, 180654, 511429, 158078, 363930, 868157, 388462, 396790, 946197, 4539, 155061, 147984, 725234, 225300, 812253, 431358, 920510]
        docs = []
        for user in self.uuids[:5]:
            res = ''
            for q in demo_q:
                det = self.database.get_responses(user, q)
                if det:
                    res += det
            if res:
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f'Using {res}, summarize the demographic details in the format "Age:, Marital Status:, Spouse Status:, Children:, Profession:, Literacy:, Religion:, Ethnicity:" using bools, short answers, or None such that is parseable as a dict by json loads',
                temperature=0.1,
                max_tokens=2049,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
                )
                dem_details = response.choices[0].text.strip()
            docs.append(dem_details)
        print(docs)
    
    def res_sex(self):
        for user in self.uuids:
            self.update_data("sex", "female", user)
    
    def is_married(self):
        data = self._scrape_data(818556)
        for key, value in data.items():
            if value:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f'Return True if they are married, and False if they are not {value}',
                    temperature=0.1,
                    max_tokens=10,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                married = response.choices[0].text.strip()
                self.update_data("marital_status", married, key)
            else:
                self.update_data("marital_status", 'NULL', key)
    
    def is_widow(self):
        data = self._scrape_data(127515)
        for key, value in data.items():
            if value:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f'Return True if they are widowed or their spouse is missing/ captured, and False if they are not {value}',
                    temperature=0.1,
                    max_tokens=10,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                widowed = response.choices[0].text.strip()
                self.update_data("widow", widowed, key)
            else:
                self.update_data("widow", 'NULL', key)
    
    def religion(self):
        data = self._scrape_data(812253)
        for key, value in data.items():
            if value:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f'What religion is this person, respond in 1-2 words {value}',
                    temperature=0.1,
                    max_tokens=10,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                religion = response.choices[0].text.strip()
                self.update_data("religion", religion, key)
            else:
                self.update_data("religion", 'NULL', key)
    
    def ethnicity(self):
        data = self._scrape_data(920510)
        for key, value in data.items():
            if value:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f'What ethnicity is this person, respond in 1-2 words {value}',
                    temperature=0.1,
                    max_tokens=10,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                ethnicity = response.choices[0].text.strip()
                self.update_data("ethnicity", ethnicity, key)
            else:
                self.update_data("ethnicity", 'NULL', key)
    
    def age(self):
        data = self._scrape_data(768766)
        for key, value in data.items():
            if value:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f'How old is this person, just return a number or NULL if unclear {value}',
                    temperature=0.1,
                    max_tokens=10,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                age = response.choices[0].text.strip()
                self.update_data("age", age, key)
            else:
                self.update_data("age", 'NULL', key)


if __name__ == '__main__':
    a = Demographics()
    #a.update_table()
    #a.is_married()
    #a.is_widow()
    #a.religion()
    #a.res_sex()
    #a.ethnicity()
    a.age()