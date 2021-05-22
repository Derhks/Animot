from datetime import datetime
from settings import db


class FinishedAnime(db.Model):
    __tablename__ = 'animes_viewed'

    id = db.Column(db.Integer, primary_key=True)
    canonical_title = db.Column(db.Text, unique=True, nullable=False)
    finished_at = db.Column(db.DateTime, nullable=False)
    is_published = db.Column(db.Boolean)

    def __init__(self, canonical_title: str):
        self.canonical_title = canonical_title
        self.finished_at = datetime.now()
        self.is_published = False

    def __repr__(self):
        return f'<Anime viewed: {self.canonical_title}>'

    def save(self):
        db.session.add(FinishedAnime(canonical_title=self.canonical_title))
        db.session.commit()

    def update(self, published):
        anime_viewed = FinishedAnime.query.filter_by(canonical_title=self.canonical_title).first()
        anime_viewed.is_published = published
        db.session.commit()
