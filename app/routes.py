from fastapi import APIRouter, Request, Header
from app.utils import razorpay_client, verify_payment_signature, verify_webhook_signature

router = APIRouter(prefix="/api/payments")


@router.post("/create-order")
async def create_order(request: Request):
    body = await request.json()
    amount = body.get("amount")
    currency = body.get("currency", "INR")
    receipt_id = body.get("receiptId", f"rcpt_{id(body)}")

    if not amount or amount <= 0:
        return {"error": "Valid amount required"}

    order = razorpay_client.order.create(
        {
            "amount": amount,      # paise
            "currency": currency,
            "receipt": receipt_id,
        }
    )

    return {
        "success": True,
        "orderId": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "receipt": order["receipt"],
        "keyId": razorpay_client.auth[0]
    }


@router.post("/verify-signature")
async def verify_signature(request: Request):
    body = await request.json()

    order_id = body.get("razorpay_order_id")
    payment_id = body.get("razorpay_payment_id")
    signature = body.get("razorpay_signature")

    valid = verify_payment_signature(order_id, payment_id, signature)

    if not valid:
        return {"success": False, "error": "Invalid signature"}

    # Update DB here

    return {"success": True, "message": "Payment verified"}


@router.post("/webhook")
async def webhook(
    request: Request,
    x_razorpay_signature: str = Header(None)
):
    raw_body = await request.body()

    if not verify_webhook_signature(raw_body, x_razorpay_signature):
        return {"status": "invalid signature"}

    event = await request.json()

    # Process events
    if event["event"] == "payment.captured":
        payment_id = event["payload"]["payment"]["entity"]["id"]
        # update database
        print("Payment captured:", payment_id)

    return {"status": "ok"}
