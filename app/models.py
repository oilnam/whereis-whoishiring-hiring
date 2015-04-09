from app import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.UnicodeText)
    country = db.Column(db.UnicodeText)

    def __init__(self, _name, _country):
        self.name = _name
        self.country = _country

    def __repr__(self):
        return '{}'.format(self.name)



class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.UnicodeText)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    hn_id = db.Column(db.Integer)
    location = db.Column(db.Integer, db.ForeignKey('city.id'))

    def __init__(self, _description, _month, _year, _hn_id, _location):
        self.description = _description
        self.month = _month
        self.year = _year
        self.hn_id = _hn_id
        self.location = _location

    def __repr__(self):
        return '{}'.format(self.description)
