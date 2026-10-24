import yfinance as yf
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_TOKEN = "8896619870:AAFBniky8f033NtnJdB0ax7-ETNkvTXpTEI"
FINNHUB_KEY = "dbdkt69r01qtak1qvbd0dbdkt69r01qtak1qvbdg"

def scan_low():
    stocks=[]
    LIST=["SOFI","NIO","MARA","RIOT","CLSK","SNDL","NOK","BB","AMC","LCID","FUBO","OPEN","CLOV","BBAI","SOUN","JOBY","LUNR","RKLB","ASTS","IONQ","RGTI","QUBT"]
    for sym in LIST:
        try:
            t=yf.Ticker(sym)
            h=t.history(period="1d")
            if h.empty: continue
            price=float(h['Close'].iloc[-1])
            vol=int(h['Volume'].sum())
            if 0.5<=price<=7 and vol>500000:
                ch=float((h['Close'].iloc[-1]-h['Open'].iloc[0])/h['Open'].iloc[0]*100)
                stocks.append(f"${sym} | ${price:.2f} | {ch:+.1f}% | Vol {vol/1e6:.1f}M")
        except: continue
    return stocks

async def start(u,c): await u.message.reply_text("أبو سهم جاهز 🔥 /filter")
async def filt(u,c):
    await u.message.reply_text("⏳ يفحص...")
    s=scan_low()
    msg="🔥 أسهم تحت 7$\n\n"+"\n".join(s[:20]) if s else "السوق مقفل (ويكند)"
    await u.message.reply_text(msg)

def main():
    app=Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("filter",filt))
    app.run_polling()

if __name__=="__main__": main()
