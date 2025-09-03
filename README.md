# Invoice Chatbot

A smart chatbot that can read invoices and answer questions using both rule-based logic and local AI models.

## Features

- Parse invoice data from sample invoices
- Answer questions about due dates, totals, and vendors
- CLI interface for interactive queries
- **Local AI model** for natural language understanding (no external API needed!)
- Fallback to rule-based responses for reliability

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the chatbot (with local AI):
```bash
python chatbot_simple.py
```

3. Or run the basic version:
```bash
python chatbot.py
```

## Sample Queries

- "How many invoices are due in the next 7 days?"
- "What is the total value of the invoice from Amazon?"
- "List all vendors with invoices > $2,000"
- "Show me all invoices"
- "What invoices are overdue?"

## Sample Data

The chatbot uses 3 sample invoices:
- Amazon: $2,450.00 (due Sept 5, 2025)
- Microsoft: $3,100.00 (due Sept 10, 2025)
- Google: $1,800.00 (due Aug 30, 2025)

## Exit

Type 'quit', 'exit', or 'bye' to exit the chatbot.
## T
wo Versions Available

### 1. `chatbot_simple.py` (Recommended)
- Uses DistilBERT Q&A model (lightweight, fast)
- Better natural language understanding
- Works offline after initial model download
- Handles queries like "Which vendor has the highest invoice?"

### 2. `chatbot.py` (Advanced)
- Uses DialoGPT for conversational AI
- More resource intensive
- Better for complex conversations

## Model Information

The chatbot automatically downloads and uses:
- **DistilBERT-base-cased** (~250MB) for question answering
- **DialoGPT-small** (~350MB) for conversational responses

Models are cached locally after first download.

## Enhanced Query Examples

With the local AI model, you can ask more natural questions:
- "Which company owes the most money?"
- "What's the invoice number for Microsoft?"
- "Who has invoices due this month?"
- "Which vendor has the earliest due date?"