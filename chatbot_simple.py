"""
Lightweight version using a smaller, faster model for better performance.
"""

import re
import json
from transformers import pipeline
from invoice_parser import InvoiceParser


class SimpleLLMChatbot:
    def __init__(self):
        self.parser = InvoiceParser()
        self.running = True
        self.qa_pipeline = None
        self.load_qa_model()
    
    def load_qa_model(self):
        """Load a lightweight Q&A model."""
        try:
            print("Loading lightweight Q&A model...")
            # Use DistilBERT for question answering - much smaller and faster
            self.qa_pipeline = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad",
                tokenizer="distilbert-base-cased-distilled-squad"
            )
            print("✅ Q&A model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Could not load Q&A model: {e}")
            self.qa_pipeline = None
    
    def create_invoice_context(self):
        """Create a text context from invoice data."""
        context = "Invoice Information: "
        for inv in self.parser.invoices:
            context += f"Vendor {inv['vendor']} has invoice number {inv['invoice_number']} "
            context += f"dated {inv['invoice_date']} with due date {inv['due_date']} "
            context += f"for total amount ${inv['total']:.2f}. "
        return context
    
    def process_query(self, query):
        """Process user query with rule-based + LLM fallback."""
        query_lower = query.lower()
        
        # Check for exit commands
        if any(word in query_lower for word in ['quit', 'exit', 'bye']):
            self.running = False
            return "Goodbye! Thanks for using the Invoice Chatbot."
        
        # Try rule-based processing first (faster)
        rule_response = self.try_rule_based(query)
        if rule_response:
            return rule_response
        
        # Fallback to Q&A model
        if self.qa_pipeline:
            return self.try_qa_model(query)
        
        return self.show_help()
    
    def try_rule_based(self, query):
        """Try rule-based processing first."""
        query_lower = query.lower()
        
        # Show all invoices
        if 'show' in query_lower and 'all' in query_lower:
            return self.show_all_invoices()
        
        # Due in next X days
        if 'due' in query_lower and ('next' in query_lower or 'days' in query_lower):
            days_match = re.search(r'(\d+)\s*days?', query_lower)
            days = int(days_match.group(1)) if days_match else 7
            return self.handle_due_invoices(days)
        
        # Total value from specific vendor
        if 'total' in query_lower and 'from' in query_lower:
            vendor_match = re.search(r'from\s+(\w+)', query_lower)
            if vendor_match:
                vendor = vendor_match.group(1)
                return self.handle_vendor_total(vendor)
        
        # List vendors above amount
        if 'list' in query_lower and 'vendors' in query_lower and ('>' in query or 'above' in query_lower):
            amount_match = re.search(r'(?:>|above)\s*\$?(\d+(?:,\d{3})*)', query)
            if amount_match:
                amount = float(amount_match.group(1).replace(',', ''))
                return self.handle_vendors_above_amount(amount)
        
        return None  # No rule-based match
    
    def try_qa_model(self, query):
        """Try Q&A model for natural language queries."""
        try:
            context = self.create_invoice_context()
            result = self.qa_pipeline(question=query, context=context)
            
            # If confidence is reasonable, return the answer
            if result['score'] > 0.1:
                return f"{result['answer']} (confidence: {result['score']:.2f})"
            else:
                return "I'm not confident about that answer. Try asking more specifically about vendors, dates, or amounts."
                
        except Exception as e:
            return f"Error processing with AI model: {e}"
    
    def handle_due_invoices(self, days=7):
        """Handle queries about invoices due in X days."""
        due_invoices = self.parser.get_invoices_due_in_days(days)
        
        if not due_invoices:
            return f"No invoices are due in the next {days} days."
        
        count = len(due_invoices)
        response = f"{count} invoice{'s' if count != 1 else ''} due in the next {days} days:\n"
        
        for inv in due_invoices:
            response += f"- {inv['vendor']}, due {self.parser.format_date(inv['due_date'])}, {self.parser.format_currency(inv['total'])}\n"
        
        return response.strip()
    
    def handle_vendor_total(self, vendor):
        """Handle queries about total from specific vendor."""
        invoice = self.parser.get_invoice_by_vendor(vendor)
        
        if not invoice:
            return f"No invoice found from {vendor}."
        
        return f"Total value of invoice from {invoice['vendor']}: {self.parser.format_currency(invoice['total'])}"
    
    def handle_vendors_above_amount(self, amount):
        """Handle queries about vendors with invoices above amount."""
        invoices = self.parser.get_invoices_above_amount(amount)
        
        if not invoices:
            return f"No vendors have invoices above {self.parser.format_currency(amount)}."
        
        response = f"Vendors with invoices > {self.parser.format_currency(amount)}:\n"
        for inv in invoices:
            response += f"- {inv['vendor']} ({self.parser.format_currency(inv['total'])})\n"
        
        return response.strip()
    
    def show_all_invoices(self):
        """Show all invoices."""
        response = "All invoices:\n"
        for inv in self.parser.invoices:
            response += f"- {inv['vendor']}: {inv['invoice_number']}, due {self.parser.format_date(inv['due_date'])}, {self.parser.format_currency(inv['total'])}\n"
        return response.strip()
    
    def show_help(self):
        """Show help message."""
        return """I can help you with invoice queries! Try asking:

• "How many invoices are due in the next 7 days?"
• "What is the total value of the invoice from Amazon?"
• "Lis