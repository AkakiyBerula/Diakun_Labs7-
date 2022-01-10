import enum
from .. import db


"""class ContractTypes(enum.Enum):
    one_sided = "Односторонній"
    two_sided = "Двохсторонній"
    many_sided = "Багатосторонній"""

class Contractypes(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, unique = True)
    contract = db.relationship('Contracts', backref='my_backref_types', lazy=True)


class Contracts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    contract_code = db.Column(db.String(10), nullable=False, unique=True)
    organization_name = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.Date(), nullable=False)
    contract_amount = db.Column(db.Float(), nullable=True)
    contract_type = db.Column(db.Integer, db.ForeignKey('contractypes.type_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Сontracts('{self.id}', '{self.organization_name}')"