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

class UrlHit(db.Model):
    __tablename__ = "url_hits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url_id = db.Column(db.String(255), db.ForeignKey("urls.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    ip_addr = db.Column(db.String(255), nullable=False)
    device_type = db.Column(db.String(255), nullable=False)
    browser_type = db.Column(db.String(255), nullable=False)
    qrcode = db.Column(db.Boolean, nullable=False)

    def __init__(self, url_id, ip_addr, device_type, browser_type, qrcode):
        self.url_id = url_id
        self.ip_addr = ip_addr
        self.device_type = device_type
        self.browser_type = browser_type
        self.qrcode = qrcode

