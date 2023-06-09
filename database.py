import sqlite3
import re
import random

def thread_db(fn):
    def set_up(self, *args, **kwargs):
        con = sqlite3.connect("dedoose_data.db")
        cur = con.cursor()
        con.create_function('regexp', 2, lambda x, y: 1 if re.search(x,y) else 0)
        thread_cur = fn(self, con, cur, *args, **kwargs)
        con.close()
        return thread_cur
    return set_up

class Database:
    def __init__(self) -> None:
        pass
    
    @thread_db
    def create_table(self, con, cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uuid integer PRIMARY KEY,
                interview_name text UNIQUE,
                audio_name text UNIQUE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id integer PRIMARY KEY,
                question_name text,
                question text,
                section text
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                response_id integer PRIMARY KEY,
                uuid integer,
                question_id integer,
                raw_response text,
                response text
            );
        """)
        con.commit()
    
    @thread_db
    def add_users(self, con, cur, interview_name):
        uuid = random.randint(1, 2**20)
        cur.execute("""
            INSERT INTO users (uuid, interview_name)
                VALUES (?, ?)
        """, [uuid, interview_name])
        con.commit()
    
    @thread_db
    def add_questions(self, con, cur, question_name, question, section):
        question_id = random.randint(1, 2**20)
        cur.execute("""
            INSERT INTO questions (question_id, question_name, question, section)
                VALUES (?, ?, ?, ?)
        """, [question_id, question_name, question, section])
        con.commit()

    @thread_db
    def get_user(self, con, cur, interview_name, all=False):
        if all:
            cur.execute("""
                SELECT uuid FROM users
            """)
            vals = cur.fetchall()
            if vals is None:
                raise Exception("No interviews found")
            return [val[0] for val in vals]
        else:
            cur.execute("""
                SELECT uuid FROM users WHERE interview_name = ?
            """, [interview_name])
            val = cur.fetchone()
            if val is None:
                raise Exception("No interviews found for this interview name")
            return val[0]

    @thread_db
    def get_question_id(self, con, cur, question_name, all=False):
        if all:
            cur.execute("""
                SELECT question_id FROM questions
            """)
            vals = cur.fetchall()
            if vals is None:
                raise Exception("No questions")
            return [val[0] for val in vals]
        else:
            cur.execute("""
                SELECT question_id FROM questions WHERE question_name = ?
            """, [question_name])
            val = cur.fetchone()
            if val is None:
                raise Exception("No questions found for this question name")
            return val[0]

    @thread_db
    def get_question(self, con, cur, question_id):
        cur.execute("""
                SELECT question FROM questions WHERE question_id = ?
            """, [question_id])
        val = cur.fetchone()
        if val is None:
            raise Exception("No questions found for this question id")
        return val[0]

    @thread_db
    def get_sections(self, con, cur):
        sections = []
        cur.execute('SELECT DISTINCT section FROM questions')
        results = cur.fetchall()
        for row in results:
            sections.append(row[0])
        return sections

    @thread_db
    def get_section_questions(self, con, cur, section):
        questions = []
        cur.execute("""
            SELECT question_id FROM questions WHERE section = ?
        """, [section])
        val = cur.fetchall()
        if val:
            for q in val:
                questions.append(q[0])
        return questions
    
    @thread_db
    def add_raw_responses(self, con, cur, interview_name, question_name, raw_response):
        response_id = random.randint(1, 2**50)
        uuid = self.get_user(interview_name)
        question_id = self.get_question_id(question_name)
        cur.execute("""
            INSERT INTO responses (response_id, uuid, question_id, raw_response)
                VALUES (?, ?, ?, ?)
        """, [response_id, uuid, question_id, raw_response])
        #cur.execute("""
            #UPDATE users SET audio_name = ? WHERE uuid = ?
        #""", [audio_name, uuid])
        con.commit()
    
    @thread_db
    def add_normalized_responses(self, con, cur, response, uuid, question_id):
        print(response, uuid, question_id)
        cur.execute("""
            UPDATE responses SET response = ? WHERE uuid = ? and question_id = ?
        """, [response, uuid, question_id])
        con.commit()
    
    @thread_db
    def get_raw_responses(self, con, cur, uuid, question_id):
        cur.execute("""
            SELECT raw_response FROM responses WHERE uuid = ? AND question_id = ?
        """, [uuid, question_id])
        val = cur.fetchone()
        if val is None:
            return 0
            #raise Exception("No questions found for this question name")
        return val[0]

    @thread_db
    def get_responses(self, con, cur, uuid, question_id):
        cur.execute("""
            SELECT response FROM responses WHERE uuid = ? AND question_id = ?
        """, [uuid, question_id])
        val = cur.fetchone()
        if val is None:
            return False
        return val[0]
    
    @thread_db
    def delete_table(self, con, cur):
        cur.execute("DROP table IF EXISTS users")
        cur.execute("DROP table IF EXISTS questions")
        cur.execute("DROP table IF EXISTS responses")
        con.commit()
    
    #@thread_db
    def delete_user(self, con, cur, interview_name):
        uuid = self.get_user(interview_name)
        cur.execute("""
                    DELETE FROM users WHERE (interview_name = ?)
                """, [interview_name])
        cur.execute("""
                    DELETE FROM responses WHERE (uuid = ?)
                """, [uuid])
        con.commit()

    
    
    


