# simulate_thingspeak_stable.py
import requests
import time
import random

# ==== CONFIGURE THIS ====
WRITE_KEY = 'YPSTQO1DL709XOJO'   # <-- replace this with your ThingSpeak Write API Key
THINGSPEAK_URL = 'https://api.thingspeak.com/update'
BASE_INTERVAL = 16  # ≥15s required by ThingSpeak Free Tier
BINS = [101, 102, 103]
# =========================

WASTE_TYPES = ['general', 'organic', 'recyclable']

def send_update(bin_id, fill_level, waste_type):
    payload = {
        'api_key': WRITE_KEY,
        'field1': fill_level,
        'field2': bin_id,
        'status': waste_type
    }

    try:
        r = requests.post(THINGSPEAK_URL, data=payload, timeout=10)
        if r.status_code == 200 and r.text != '0':
            print(f"✅ Sent: bin={bin_id}, fill={fill_level}%, waste={waste_type}, entry={r.text}")
        else:
            print(f"⚠️  Skipped: Too soon or duplicate (code={r.status_code}, text={r.text})")
    except Exception as e:
        print('❌ Error sending:', e)

def simulate_loop():
    fills = {b: random.randint(0, 50) for b in BINS}
    while True:
        for b in BINS:
            # Rapid fill-up for more action
            fills[b] = min(100, fills[b] + random.randint(10, 25))
            waste_type = random.choice(WASTE_TYPES)

            send_update(b, fills[b], waste_type)

            # Alert condition
            if fills[b] >= 40:
                print(f"🟡 Bin {b} FULL ({fills[b]}%)! Sending alert... 🚮 Emptying now...")
                fills[b] = random.randint(5, 15)

            # Add safe delay + small random jitter
            wait_time = BASE_INTERVAL + random.randint(1, 4)
            print(f"⏳ Waiting {wait_time}s before next bin...")
            time.sleep(wait_time)

if __name__ == '__main__':
    print("🚀 Starting Smart Waste Simulator (Stable Mode)... Press Ctrl+C to stop.\n")
    try:
        simulate_loop()
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user. Goodbye!\n")
