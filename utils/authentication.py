class Authentication:
    """
    Handles authentication for admin access.
    """
    
    def __init__(self, db):
        """
        Initialize the authentication system.
        
        Args:
            db: DatabaseHandler instance
        """
        self.db = db
    
    def verify_credentials(self, username, password):
        """
        Verify admin credentials.
        
        Args:
            username: Admin username
            password: Admin password
            
        Returns:
            Boolean indicating whether credentials are valid
        """
        return self.db.verify_admin(username, password)
    
    def change_password(self, username, old_password, new_password):
        """
        Change admin password.
        
        Args:
            username: Admin username
            old_password: Current password
            new_password: New password
            
        Returns:
            Boolean indicating success
        """
        # Verify current credentials
        if not self.verify_credentials(username, old_password):
            return False
        
        # Update password in database
        try:
            self.db.cursor.execute(
                "UPDATE admins SET password = ? WHERE username = ?",
                (new_password, username)
            )
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
