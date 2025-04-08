import datetime

class Visit:
    """
    Model class representing a devotee's visit.
    """
    
    def __init__(self, id=None, devotee_id="", visit_date=None, selected_item=""):
        """
        Initialize a visit.
        
        Args:
            id: Database ID (can be None for new visits)
            devotee_id: ID of the devotee who visited
            visit_date: Date of the visit (datetime.date)
            selected_item: The randomly selected item
        """
        self.id = id
        self.devotee_id = devotee_id
        
        # Set visit date to today if not provided
        if visit_date is None:
            self.visit_date = datetime.date.today()
        elif isinstance(visit_date, str):
            # Parse ISO date string (YYYY-MM-DD)
            self.visit_date = datetime.date.fromisoformat(visit_date)
        else:
            self.visit_date = visit_date
            
        self.selected_item = selected_item
    
    @classmethod
    def from_db_row(cls, row):
        """
        Create a Visit instance from a database row.
        
        Args:
            row: Database row tuple (id, devotee_id, visit_date, selected_item)
            
        Returns:
            Visit instance
        """
        if not row:
            return None
        
        # Parse date from ISO format if it's a string
        visit_date = row[2]
        if isinstance(visit_date, str):
            visit_date = datetime.date.fromisoformat(visit_date)
        
        return cls(
            id=row[0],
            devotee_id=row[1],
            visit_date=visit_date,
            selected_item=row[3]
        )
    
    def to_dict(self):
        """
        Convert visit to dictionary.
        
        Returns:
            Dictionary representation of visit
        """
        return {
            'id': self.id,
            'devotee_id': self.devotee_id,
            'visit_date': self.visit_date.isoformat(),
            'selected_item': self.selected_item
        }
