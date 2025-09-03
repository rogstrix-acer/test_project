# Invoice Chatbot

A simple chatbot that can read invoices and answer basic questions about them.

## Features

- Parse invoice data from sample invoices
- Answer questions about due dates, totals, and vendors
- CLI interface for interactive queries

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the chatbot:
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