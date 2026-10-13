"""Write data.json with delayed quotes (price, day change, day %) only."""
import json, datetime
from zoneinfo import ZoneInfo
import yfinance as yf
ET = ZoneInfo("America/New_York")
SYMS = ["TSLA", "NVDA", "SMH", "AMD", "XLK", "NQ=F"]
out = {"generated_et": datetime.datetime.now(ET).strftime("%Y-%m-%d %H:%M ET"), "quotes": {}}
for s in SYMS:
    try:
        h = yf.Ticker(s).history(period="5d", interval="1d")
        if len(h) < 2:
            raise ValueError("insufficient history")
        last, prev = float(h["Close"].iloc[-1]), float(h["Close"].iloc[-2])
        ts = h.index[-1].tz_convert(ET) if h.index[-1].tzinfo else h.index[-1]
        out["quotes"][s] = {"price": round(last, 2), "change": round(last - prev, 2),
                            "change_pct": round(100 * (last - prev) / prev, 2),
                            "asof_et": ts.strftime("%Y-%m-%d") + " close"}
    except Exception as e:
        out["quotes"][s] = {"price": None, "error": str(e)[:200]}
with open("data.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
