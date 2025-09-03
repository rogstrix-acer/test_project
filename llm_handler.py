"""
Local LLM handler using Hugging Face transformers.
"""

import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from invoice_data import get_invoices


class LocalLLMHandler:
    def __init__(self, model_name="microsoft/DialoGPT-small"):
        """Initialize the local LLM handler."""
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.invoices = get_invoices()
        self.load_model()
    
    def load_model(self):
        """Load the local model."""
        try:
            print(f"Loading local model: {self.model_name}...")
            
            # Use a lightweight text generation model
            self.pipeline = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                tokenizer="microsoft/DialoGPT-small",
                device=0 if torch.cuda.is_available() else -1,
                max_length=200,
                do_sample=True,
                temperature=0.7
            )
            
            print("✅ Local model loaded successfully!")
            
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
            print("Falling back to rule-based responses only.")
            self.pipeline = None
    
    def create_context_prompt(self, query):
        """Create a context-aware prompt with invoice data."""
        invoice_context = "Available invoice data:\n"
        for inv in self.invoices:
            invoice_context += f"- {inv['vendor']}: Invoice #{inv['invoice_number']}, "
            invoice_context += f"Date: {inv['invoice_date']}, Due: {inv['due_date']}, "
            invoice_context += f"Total: ${inv['total']:.2f}\n"
        
        prompt = f"""You are an invoice assistant. Based on the following invoice data, answer the user's question concisely.

{invoice_context}

User question: {query}
Assistant: """
        
        return prompt
    
    def generate_response(self, query):
        """Generate response using the local LLM."""
        if not self.pipeline:
            return "I'm sorry, the local AI model is not available. Please try a more specific query."
        
        try:
            prompt = self.create_context_prompt(query)
            
            # Generate response
            response = self.pipeline(
                prompt,
                max_new_tokens=100,
                num_return_sequences=1,
                pad_token_id=self.pipeline.tokenizer.eos_token_id
            )
            
            # Extract the generated text after the prompt
            generated_text = response[0]['generated_text']
            assistant_response = generated_text.split("Assistant: ")[-1].strip()
            
            # Clean up the response
            assistant_response = assistant_response.split('\n')[0]  # Take first line
            
            return assistant_response if assistant_response else "I'm not sure how to answer that question."
            
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I encountered an error processing your question. Please try rephrasing it."
    
    def is_available(self):
        """Check if the LLM is available."""
        return self.pipeline is not None