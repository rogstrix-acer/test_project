"""
Sample invoice data for the chatbot.
In a real implementation, this would be extracted from PDF/image files.
"""

from datetime import datetime

# Sample invoice data extracted from invoices
SAMPLE_INVOICES = [
    {
        "vendor": "Amazon",
        "invoice_number": "INV-0012",
        "invoice_date": "2025-08-20",
        "due_date": "2025-09-05",
        "total": 2450.00
    },
    {
        "vendor": "Microsoft", 
        "invoice_number": "INV-0043",
        "invoice_date": "2025-08-25",
        "due_date": "2025-09-10", 
        "total": 3100.00
    },
    {
        "vendor": "Google",
        "invoice_number": "INV-0089",
        "invoice_date": "2025-08-15",
        "due_date": "2025-08-30",
        "total": 1800.00
    }
]

def get_invoices():
    """Return the sample invoice data."""
    return SAMPLE_INVOICES