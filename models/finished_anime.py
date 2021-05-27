from datetime import datetime
from settings import db


class FinishedAnime(db.Model):
    __tablename__ = 'animes_viewed'

    id = db.Column(db.Integer, primary_key=True)
    canonical_title = db.Column(db.Text, unique=True, nullable=False)
    finished_at = db.Column(db.DateTime, nullable=False)
    is_published = db.Column(db.Boolean)

    def __init__(self, anime_name: str):
        self.canonical_title = self.get_canonical_title(anime_name)
        self.finished_at = datetime.now()
        self.is_published = False

    def __repr__(self):
        return f'<Anime viewed: {self.canonical_title}>'

    def save(self):
        db.session.add(FinishedAnime(anime_name=self.canonical_title))
        db.session.commit()

    def update(self, published):
        anime_viewed = FinishedAnime.query.filter_by(canonical_title=self.canonical_title).first()
        anime_viewed.is_published = published
        db.session.commit()

    def was_published(self) -> bool:
        anime_viewed = FinishedAnime.query.filter_by(canonical_title=self.canonical_title).first()

        if anime_viewed is None:
            return False

        return anime_viewed.is_published

    @staticmethod
    def get_canonical_title(name: str) -> str:
        words_list = name.lower().split('-')
        canonical_title = ''

        for idx in range(len(words_list)):
            word = words_list[idx]

            if len(word) > 3 or idx == 0:
                new_word = list(word)
                new_word[0] = word[0].upper()
                canonical_title += ''.join(new_word)
            else:
                canonical_title += word

            if idx < len(words_list) - 1:
                canonical_title += ' '

        return canonical_title
