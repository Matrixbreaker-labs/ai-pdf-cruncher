import os
import pandas as pd
from google import genai

# ১. ইনভয়েস ডাটা সিন্থেসিস লেয়ার (SCM Invoice Synthesis Layer)
def extract_invoice_data_via_ai(raw_invoice_text):
    """গুগল জেমিনি এপিআই ব্যবহার করে অগোছালো লজিস্টিকস ইনভয়েস থেকে ডাটা ফিল্টার করার মেকানিズム।"""
    client = genai.Client()
    
    prompt = f"""
    You are an advanced Supply Chain & Logistics AI. Analyze the following raw, unstructured invoice text.
    Extract the key SCM metrics and format them exactly as a clean, pipe-separated text string like this:
    Vendor Name | Invoice Date | Total Amount USD | Container Number | Port of Discharge

    Ensure no extra words, greetings, or markdown explanations. Just return the pipe-separated string.
    
    Raw Invoice Data:
    {raw_invoice_text}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text.strip()

# ২. ডাটা স্ট্রাকচারিং ও এক্সেল এক্সপোর্ট নোড (Structured Export Node)
def process_scm_pipeline(raw_data_stream):
    print("[*] Initializing Silicon Processing Unit...")
    extracted_string = extract_invoice_data_via_ai(raw_data_stream)
    
    # পাইপ সেপারেটেড স্ট্রিংকে লিস্টে রূপান্তর করা
    data_fields = [field.strip() for field in extracted_string.split('|')]
    
    # এক্সেল ফাইল বা ডেটাফ্রেম তৈরি
    columns = ["Vendor Name", "Invoice Date", "Total Amount (USD)", "Container Number", "Port of Discharge"]
    df = pd.DataFrame([data_fields], columns=columns)
    
    # এক্সেল ফাইল জেনারেট করা
    output_filename = "scm_structured_invoice.xlsx"
    df.to_excel(output_filename, index=False)
    print(f"[+] Output compiled successfully. File locked as: {output_filename}")

if __name__ == "__main__":
    # টেস্ট করার জন্য একটি অগোছালো লজিস্টিকস ইনভয়েসের র ডেটা
    sample_raw_invoice = """
    INVOICE #INV-2026-9901
    Date: October 22, 2026
    From: Maersk Logistics International (Global Shipping Hub)
    To: Apex Retail Bangladesh SCM
    Billable Items:
    Freight Charges for 40ft High Cube Container: $4,500.00
    Terminal Handling Fees: $350.00
    Container ID: MRSK8890214
    Discharge Destination: Port of Chittagong, Bangladesh
    Total Due: $4,850.00 USD
    Please settle via bank wire transfer within 14 days.
    """
    
    process_scm_pipeline(sample_raw_invoice)
