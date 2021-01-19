from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contacts(db.Model):
    """Defines the structure for a contact (number).

        Args:
           db.Model: object for manipulating the database.

        Returns:
            A requested number.

        Raises:
            Abort: If the user is not authenticated.
    """


    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(20))
    monthyPrice = db.Column(db.Float(precision=2))
    setupPrice = db.Column(db.Float())
    currency = db.Column(db.String(4))

    def __init__(self, value, monthyPrice, setupPrice, currency):
        self.value = value
        self.monthyPrice = round(monthyPrice, 2)
        self.setupPrice = round(setupPrice, 2)
        self.currency = currency

    def to_dict(self, columns=[]):

        """Converts the object's structure to a dictionary.

           Args:
              columns: structure columns.

           Returns:
              Contact in dictionary format.
        """

        if not columns:
            return {"id": self.id, "value": self.value, "monthyPrice": self.monthyPrice, "setupPrice": self.setupPrice, "currency" : self.currency}
        else:
            return {col: getattr(self, col) for col in columns}