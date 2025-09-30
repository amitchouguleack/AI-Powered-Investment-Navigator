import openai
import yfinance as yf


def get_stock_summary(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "Name": info.get("longName"),
        "Sector": info.get("sector"),
        "Market Cap": info.get("marketCap"),
        "PE Ratio": info.get("trailingPE"),
        "Dividend Yield": info.get("dividendYield"),
    }


def ask_llm(prompt):
    openai.api_key = "your-openai-key"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are FinPilot, an ethical investment advisor."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
