"""
Invoice Chatbot - CLI interface for querying invoice data.
"""

import re
from invoice_parser import InvoiceParser
from llm_handler import LocalLLMHandler


class InvoiceChatbot:
    def __init__(self):
        self.parser = InvoiceParser()
        self.llm_handler = LocalLLMHandler()
        self.running = True
    
    def process_query(self, query):
        """Process user query and return appropriate response."""
        query_lower = query.lower()
        
        # Check for exit commands
        if any(word in query_lower for word in ['quit', 'exit', 'bye']):
            self.running = False
            return "Goodbye! Thanks for using the Invoice Chatbot."
        
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
        if 'list' in query_lower and 'vendors' in query_lower and '>' in query:
            amount_match = re.search(r'>\s*\$?(\d+(?:,\d{3})*)', query)
            if amount_match:
                amount = float(amount_match.group(1).replace(',', ''))
                return self.handle_vendors_above_amount(amount)
        
        # Overdue invoices
        if 'overdue' in query_lower:
            return self.handle_overdue_invoices()
        
        # If no rule-based match, try LLM
        if self.llm_handler.is_available():
            return self.llm_handler.generate_response(query)
        
        # Help or unknown query
        return self.show_help()
    
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
    
    def handle_overdue_invoices(self):
        """Handle queries about overdue invoices."""
        overdue = self.parser.get_overdue_invoices()
        
        if not overdue:
            return "No invoices are overdue."
        
        response = f"{len(overdue)} overdue invoice{'s' if len(overdue) != 1 else ''}:\n"
        for inv in overdue:
            response += f"- {inv['vendor']}, due {self.parser.format_date(inv['due_date'])}, {self.parser.format_currency(inv['total'])}\n"
        
        return response.strip()
    
    def show_all_invoices(self):
        """Show all invoices."""
        response = "All invoices:\n"
        for inv in self.parser.invoices:
            response += f"- {inv['vendor']}: {inv['invoice_number']}, due {self.parser.format_date(inv['due_date'])}, {self.parser.format_currency(inv['total'])}\n"
        return response.strip()
    
    def show_help(self):
        """Show help message with example queries."""
        return """I can help you with invoice queries! Try asking:

• "How many invoices are due in the next 7 days?"
• "What is the total value of the invoice from Amazon?"
• "List all vendors with invoices > $2,000"
• "Show me all invoices"
• "What invoices are overdue?"

Type 'quit', 'exit', or 'bye' to exit."""
    
    def run(self):
        """Run the chatbot CLI."""
        print("🤖 Invoice Chatbot")
        print("=" * 50)
        
        # Show LLM status
        if self.llm_handler.is_available():
            print("✅ Local AI model loaded - I can handle natural language queries!")
        else:
            print("⚠️ Local AI model not available - using rule-based responses only")
        
        print("Ask me about your invoices! Type 'help' for examples.\n")
        
        while self.running:
            try:
                query = input("You: ").strip()
                if not query:
                    continue
                
                response = self.process_query(query)
                print(f"Bot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! Thanks for using the Invoice Chatbot.")
                break
            except Exception as e:
                print(f"Bot: Sorry, I encountered an error: {e}\n")


if __name__ == "__main__":
    chatbot = InvoiceChatbot()
    chatbot.run()