from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    access_count = db.Column(db.Integer, default=0)

    def serialize(self, include_stats=False):
        data = {
            "id": self.id,
            "url": self.url,
            "shortCode": self.short_code,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
        }
        if include_stats:
            data["accessCount"] = self.access_count
        return data
