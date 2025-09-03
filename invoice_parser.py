"""
Invoice parsing and query functions.
"""

from datetime import datetime, timedelta
from dateutil.parser import parse
from invoice_data import get_invoices


class InvoiceParser:
    def __init__(self):
        self.invoices = get_invoices()
    
    def get_invoices_due_in_days(self, days=7):
        """Get invoices due within the specified number of days."""
        today = datetime.now().date()
        target_date = today + timedelta(days=days)
        
        due_invoices = []
        for invoice in self.invoices:
            due_date = parse(invoice['due_date']).date()
            if today <= due_date <= target_date:
                due_invoices.append(invoice)
        
        return due_invoices
    
    def get_invoice_by_vendor(self, vendor_name):
        """Get invoice by vendor name (case insensitive)."""
        for invoice in self.invoices:
            if invoice['vendor'].lower() == vendor_name.lower():
                return invoice
        return None
    
    def get_invoices_above_amount(self, amount):
        """Get invoices with total above specified amount."""
        return [inv for inv in self.invoices if inv['total'] > amount]
    
    def get_overdue_invoices(self):
        """Get invoices that are overdue."""
        today = datetime.now().date()
        overdue = []
        
        for invoice in self.invoices:
            due_date = parse(invoice['due_date']).date()
            if due_date < today:
                overdue.append(invoice)
        
        return overdue
    
    def format_currency(self, amount):
        """Format amount as currency."""
        return f"${amount:,.2f}"
    
    def format_date(self, date_str):
        """Format date string for display."""
        date_obj = parse(date_str)
        return date_obj.strftime("%b %d, %Y")