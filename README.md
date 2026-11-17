# transaction preview sdk

ChatPayGuard is an AI‑powered **transaction preview SDK** that lets fintech applications preview every payment before exposing any card details. It generates a concise purchase summary, waits for developer‑approved validation, and only then releases the card number to the payment gateway. Designed for fintech developers who need an extra layer of security and control without sacrificing user experience.

## Problem

Existing tools focus on post‑transaction validation or simple approval flows for merchants and consumers. They do not give developers a way to intercept a payment **before** the card data is sent, leaving a gap in risk mitigation and card security for modern fintech apps.

## Solution

ChatPayGuard provides a lightweight SDK that integrates into your payment stack, previews each transaction, and requires explicit validation via an AI‑driven summary. This pre‑authorization step protects card information, reduces fraud exposure, and gives developers full control over the payment flow.

## Who is it for

- Fintech developers building mobile or web payment experiences  
- Teams integrating payment gateways who need an extra security layer  
- Companies that require strict card security and risk mitigation policies  

## Features

- **AI‑generated transaction summary** – concise description of amount, merchant, and currency.  
- **Explicit validation hook** – pause the flow until the developer approves the preview.  
- **Seamless SDK integration** – works with popular payment gateways and mobile payment SDKs.  
- **Secure handling of card data** – card numbers are never exposed until validation passes.  
- **Health check endpoint** – `/health` for monitoring SDK status.  
- **Demo endpoint** – showcases a full preview‑validate‑pay cycle.  

## Use cases

- **Mobile wallet apps** that want to show users a preview of the purchase before charging the card.  
- **Online marketplaces** needing to verify high‑value transactions prior to payment processing.  
- **Subscription services** that require manual review of the first payment to prevent fraudulent sign‑ups.  
- **Payment gateway integrations** where developers must comply with strict PCI‑DSS requirements.  

## Installation and configuration

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

For Docker users:

```bash
docker build -t app .
docker run -p 8000:8000 app
```

The API exposes two endpoints:

- `GET /health` – returns service status.  
- `POST /demo` – demonstrates a transaction preview, validation, and finalization flow.  

## Usage examples

```python
import chatpayguard

# Initialize the SDK with your API key
sdk = chatpayguard.SDK(api_key="YOUR_API_KEY")

# Create a transaction preview
preview = sdk.preview_transaction(
    amount=49.99,
    currency="USD",
    merchant="Acme Store",
    card_last4="1234"
)

print(preview.summary)
# => "Purchase of $49.99 at Acme Store. Card ending in 1234."

# Wait for developer approval (could be a UI button, webhook, etc.)
if sdk.validate_preview(preview.id, approved=True):
    # Proceed with payment
    payment = sdk.process_payment(preview.id)
    print("Payment successful:", payment.id)
else:
    print("Transaction rejected by developer.")
```

## Limitations

- The SDK does not replace full PCI‑DSS compliance; developers must still follow all required security standards.  
- Real‑time AI generation may add a small latency (typically <200 ms).  
- Currently supports only REST‑based payment gateways; native SDKs for specific platforms are planned for future releases.  

## Next steps

- Extend language support for non‑English transaction summaries.  
- Add webhook callbacks for asynchronous validation workflows.  
- Provide deeper analytics on preview acceptance rates and risk patterns.
