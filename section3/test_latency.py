import time
import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model.pkl"
LATENCY_LIMIT_MS = 500
VALID_LABELS = {"billing", "technical_issue", "feature_request", "complaint", "other"}

TICKETS = [
    "I was charged twice this month and need a refund immediately.",
    "The app crashes every time I try to upload a file.",
    "Could you add a dark mode to the dashboard?",
    "I've been waiting four days for a response and this is unacceptable.",
    "How do I add another user to my account?",
    "My invoice shows a higher amount than my plan price.",
    "I keep getting a 500 error when I open the reports page.",
    "It would be great to have a Slack integration.",
    "Your support team is completely useless and I'm furious.",
    "Where can I find your API documentation?",
    "I was billed after I cancelled my subscription last week.",
    "Notifications stopped working after yesterday's update.",
    "Can you add bulk export to the admin panel?",
    "No one has replied to my three support emails — this is terrible service.",
    "What payment methods do you accept?",
    "There's an unauthorized charge on my account from last Friday.",
    "The password reset link in my email doesn't work.",
    "I'd like a read-only view I can share with external clients.",
    "I'm a long-time customer and I've never been treated this poorly.",
    "Is there a limit to how much storage I get on the basic plan?",
]

model = joblib.load(MODEL_PATH)

print(f"{'ms':>8}  {'label':<20}  ticket")
print("-" * 80)

for ticket in TICKETS:
    t0 = time.perf_counter()
    pred = model.predict([ticket])[0]
    elapsed_ms = (time.perf_counter() - t0) * 1000

    assert pred in VALID_LABELS, f"Unexpected label '{pred}' for: {ticket}"
    assert elapsed_ms < LATENCY_LIMIT_MS, (
        f"Latency {elapsed_ms:.1f}ms exceeds {LATENCY_LIMIT_MS}ms limit\n  ticket: {ticket}"
    )

    print(f"{elapsed_ms:>7.2f}ms  {pred:<20}  {ticket[:55]}")

print("-" * 80)
print(f"All {len(TICKETS)} predictions within {LATENCY_LIMIT_MS}ms limit. Assertions passed.")
