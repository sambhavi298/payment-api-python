# Payment API (Python)

A robust payment gateway integration API built with [FastAPI](https://fastapi.tiangolo.com/) and [Razorpay](https://razorpay.com/). This API handles order creation, payment signature verification, and webhook events.

## Features

- **Create Order**: Generate Razorpay orders with dynamic amounts and currency.
- **Verify Payment**: Securely verify payment signatures on the server side.
- **Webhooks**: Handle asynchronous payment events (e.g., `payment.captured`).
- **Secure**: Uses environment variables for API keys and secrets.

## Project Structure

```
payment-api-python/
├── app/
│   ├── main.py       # Application entry point
│   ├── config.py     # Configuration & Environment loading
│   ├── routes.py     # API Endpoints
│   └── utils.py      # Razorpay client & helpers
├── .env              # Environment variables (git-ignored)
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## Prerequisites

- Python 3.8+
- [Razorpay Account](https://razorpay.com/) (Key ID & Key Secret)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/sambhavi298/payment-api-python.git
    cd payment-api-python
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Razorpay credentials and configuration:

    ```env
    PORT=4000
    RAZORPAY_KEY_ID=your_actual_key_id
    RAZORPAY_KEY_SECRET=your_actual_key_secret
    RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
    ```

## Running the Server

Start the development server with hot-reload:

```bash
uvicorn app.main:app --reload --port 4000
```

The API will be available at `http://localhost:4000`.

## API Endpoints

### 1. Create Order
**POST** `/api/payments/create-order`

Creates a new order in Razorpay.

**Body:**
```json
{
  "amount": 50000,
  "currency": "INR"
}
```
*(Note: Amount is in paise, so 50000 = ₹500.00)*

### 2. Verify Signature
**POST** `/api/payments/verify-signature`

Verifies the payment signature after a successful transaction on the client side.

**Body:**
```json
{
  "razorpay_order_id": "order_...",
  "razorpay_payment_id": "pay_...",
  "razorpay_signature": "signature_string"
}
```

### 3. Webhook
**POST** `/api/payments/webhook`

Receives events from Razorpay (e.g., `payment.captured`). Ensure the `RAZORPAY_WEBHOOK_SECRET` matches your dashboard setting.

## Testing

You can test the endpoints using [Postman](https://www.postman.com/) or the built-in Swagger UI at:
`http://localhost:4000/docs`
