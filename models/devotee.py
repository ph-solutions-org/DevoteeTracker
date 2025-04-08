class Devotee:
    """
    Model class representing a devotee.
    """
    
    def __init__(self, id="", name="", phone="", email="", address=""):
        """
        Initialize a devotee.
        
        Args:
            id: Unique identifier for the devotee
            name: Devotee's name
            phone: Devotee's phone number
            email: Devotee's email address
            address: Devotee's physical address
        """
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
    
    @classmethod
    def from_db_row(cls, row):
        """
        Create a Devotee instance from a database row.
        
        Args:
            row: Database row tuple (id, name, phone, email, address, created_at)
            
        Returns:
            Devotee instance
        """
        if not row:
            return None
        
        return cls(
            id=row[0],
            name=row[1],
            phone=row[2] if row[2] else "",
            email=row[3] if row[3] else "",
            address=row[4] if row[4] else ""
        )
    
    def to_dict(self):
        """
        Convert devotee to dictionary.
        
        Returns:
            Dictionary representation of devotee
        """
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }
