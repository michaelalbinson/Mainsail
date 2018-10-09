import sqlite3


class Database:
    def __init__(self):
        self.valid_account_types = ['facebook', 'google+', 'instagram', 'linkedin', 'reddit', 'tumblr', 'twitter']
        self.connection = sqlite3.connect("../db/core.db")

    # SCHEMA METHODS
    def generate_schema(self):
        self.connection.executescript("""
        CREATE TABLE IF NOT EXISTS post (
            post_hash VARCHAR(100) NOT NULL,
            post_text VARCHAR(1000) NOT NULL,
            acct_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY,
            nickname VARCHAR(100) DEFAULT NULL,
            username VARCHAR(100) DEFAULT NULL,
            password VARCHAR(100) DEFAULT NULL,
            oauth_token VARCHAR(100) DEFAULT NULL,
            type VARCHAR(50) NOT NULL
        );""")

    # WARNING: this will delete the existing schema... deleting everything in the current schema. Using this is not
    # recommended
    def clear_schema(self):
        self.connection.executescript("""
            DROP TABLE IF EXISTS account;
            DROP TABLE IF EXISTS post;
        """)

    def refresh_schema(self):
        self.clear_schema()
        self.generate_schema()

    # ACCOUNT METHODS
    def add_account(self, nickname=None, username=None, password=None, oauth_token=None, account_type="u"):
        if account_type is "u" or account_type not in self.valid_account_types:
            return

        self.connection.execute("INSERT INTO account (nickname, username, password, oauth_token, type) VALUES",
                                (nickname, username, password, oauth_token, account_type))

    def remove_account(self, account_type="", account_id=""):
        if not account_type or account_id:
            return

        self.connection.execute("DELETE FROM account WHERE id=?", (account_id, ))
        self.delete_all_account_posts(account_id)

    def get_account_by_id(self, acct_id):
        return self.connection.execute("SELECT type, nickname, id FROM account WHERE id=?", (acct_id, ))

    def get_accounts_by_type(self, acct_type):
        if acct_type not in self.valid_account_types:
            return

        return self.connection.execute("SELECT type, nickname, id FROM account WHERE type=?", (acct_type, ))

    def dump_all_accounts(self):
        return self.connection.executescript("SELECT type, nickname, id FROM account")

    # POST METHODS
    def add_post_record(self, post_hash, post_text, timestamp, account_id):
        return self.connection.execute("INSERT INTO post (post_hash, post_text, timestamp, acct_id) VALUES",
                                       (post_hash, post_text, timestamp, account_id, account_id))

    def get_post_record_by_hash(self, post_hash):
        pass

    def get_post_by_time(self, start_time=None, end_time=None):
        pass

    def delete_post_record(self, post_hash):
        return self.connection.execute("DELETE FROM post WHERE post_hash=?", (post_hash, ))

    def delete_all_account_posts(self, account_id):
        return self.connection.execute("DELETE FROM post WHERE acct_id=?", (account_id, ))

    def dump_all_posts(self):
        return self.connection.executescript("SELECT post_text, post_hash, id FROM account")

    def dump_all_account_posts(self, acct_id):
        return self.connection.execute("SELECT post_text, post_hash, id FROM post WHERE acct_id=?", (acct_id, ))


db = Database()
