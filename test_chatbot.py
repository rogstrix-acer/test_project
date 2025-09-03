"""
Test script to demonstrate the chatbot functionality.
"""

from chatbot import InvoiceChatbot


def test_chatbot():
    """Test the chatbot with sample queries."""
    bot = InvoiceChatbot()
    
    test_queries = [
        "How many invoices are due in the next 7 days?",
        "What is the total value of the invoice from Amazon?",
        "List all vendors with invoices > $2,000",
        "Show me all invoices",
        "What invoices are overdue?",
        "How many invoices are due in the next 30 days?"
    ]
    
    print("🧪 Testing Invoice Chatbot")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQ: {query}")
        response = bot.process_query(query)
        print(f"A: {response}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")


if __name__ == "__main__":
    test_chatbot()