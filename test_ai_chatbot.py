"""
Test script for the AI-enhanced chatbot.
"""

from chatbot_simple import SimpleLLMChatbot


def test_ai_chatbot():
    """Test the AI chatbot with various query types."""
    bot = SimpleLLMChatbot()
    
    # Test queries - mix of rule-based and natural language
    test_queries = [
        # Rule-based queries (should work fast)
        "How many invoices are due in the next 7 days?",
        "What is the total value of the invoice from Amazon?",
        "List all vendors with invoices above $2,000",
        "Show me all invoices",
        
        # Natural language queries (will use AI model)
        "Which vendor has the highest invoice?",
        "What's Microsoft's invoice number?",
        "Who owes the most money?",
        "Which company has the earliest due date?",
        "What invoices are from tech companies?",
    ]
    
    print("🧪 Testing AI-Enhanced Invoice Chatbot")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Q: {query}")
        response = bot.process_query(query)
        print(f"   A: {response}")
        
        # Add separator for readability
        if i == 4:
            print("\n" + "─" * 40 + " AI Model Queries " + "─" * 40)
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")
    print("\nNote: Natural language queries use the local AI model.")
    print("Rule-based queries are processed faster without AI.")


if __name__ == "__main__":
    test_ai_chatbot()