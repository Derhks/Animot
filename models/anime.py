from create_table import create_table
from datetime import datetime
from settings import db


class Anime(db.Model):
    __tablename__ = 'anime_posted'

    id = db.Column(db.Integer, primary_key=True)
    canonical_title = db.Column(db.Text, unique=True, nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    rating = db.Column(db.String(10), unique=True, nullable=False)
    image = db.Column(db.String(255), unique=True, nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, canonical_title: str, synopsis: str, rating: str, image: str):
        self.canonical_title = canonical_title
        self.synopsis = synopsis
        self.rating = rating
        self.image = image
        self.published_at = datetime.now()

    def __repr__(self):
        return f'<Anime: {self.canonical_title}>'

    def save(self):
        try:
            db.session.add(
                Anime(
                    canonical_title=self.canonical_title,
                    synopsis=self.synopsis,
                    rating=self.rating,
                    image=self.image
                )
            )

            db.session.commit()
        except Exception as Err:
            if Err:
                create_table()
                db.session.add(
                    Anime(
                        canonical_title=self.canonical_title,
                        synopsis=self.synopsis,
                        rating=self.rating,
                        image=self.image
                    )
                )

                db.session.commit()
