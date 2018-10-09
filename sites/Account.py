from abc import abstractmethod
from app.Database import db


class Account:
    def __init__(self, username="", password="", oauth="", acct_type="", nickname="", acct_id=""):
        self.username = username
        self.password = password
        self.oauth_token = oauth
        self.acct_type = acct_type
        self.nickname = nickname
        self.acct_id = acct_id

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def create_post(self, text):
        pass

    @abstractmethod
    def delete_post(self, post_hash):
        pass

    def record_post(self, post_hash, text):
        db.add_post_record(post_hash, self.acct_id, text)

    def get_acct_posts(self):
        self.get_acct_posts()
