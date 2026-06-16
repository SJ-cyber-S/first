import yfinance as yf
import pandas as pd

# 1. Define a list of Indian listed stocks to check (NSE format requires adding '.NS')
# You can add or replace any tickers you like in this list!
tickers = [
    "TATASTEEL.NS", "SBIN.NS", "ONGC.NS", "COALINDIA.NS", "IOC.NS", 
    "HDFCBANK.NS", "INFY.NS", "ITC.NS", "RELIANCE.NS", "GAIL.NS",
    "NTPC.NS", "BHEL.NS", "NMDC.NS", "SAIL.NS", "PFC.NS", "RECLTD.NS"
]

print("Scanning Indian stocks for Book Value comparisons...\n")
results = []

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract Current Price and Book Value per share
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        book_value = info.get('bookValue')
        
        if current_price and book_value:
            # Calculate the price-to-book ratio
            pb_ratio = current_price / book_value
            
            # Calculate the differences you requested
            diff_rupees = current_price - book_value
            pct_difference = ((current_price - book_value) / book_value) * 100
            
            results.append({
                "Stock": ticker.replace(".NS", ""),
                "Current Price (₹)": round(current_price, 2),
                "Book Value/Share (₹)": round(book_value, 2),
                "P/B Ratio": round(pb_ratio, 2),
                "Diff From BV (₹)": round(diff_rupees, 2),
                "Deviation (%)": round(pct_difference, 2)
            })
    except Exception as e:
        print(f"Could not fetch data for {ticker}: {e}")

# 2. Convert to DataFrame and sort it
df = pd.DataFrame(results)

# Filter stocks trading reasonably near Book Value (e.g., P/B ratio between 0.5 and 1.5)
# A Deviation (%) near 0% means it is trading exactly at book value.
# Negative deviation means it is trading BELOW book value (discounted value).
df_sorted = df.sort_values(by="P/B Ratio")

# 3. Display the final output beautifully
print(df_sorted.to_string(index=False))
