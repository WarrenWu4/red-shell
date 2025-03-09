from app import db

class ShellUrl(db.Model):
    __tablename__ = "urls"
    # required parameters
    id= db.Column(db.String(255), primary_key=True, unique=True)
    link = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    # optional parameters
    expires_at = db.Column(db.DateTime, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    auth = db.Column(db.Boolean, nullable=True)

    # specify init method so pyright gets off my ass about it
    def __init__(self, id:str, link:str):
        self.id = id
        self.link = link
