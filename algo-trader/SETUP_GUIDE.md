# Setup Guide - Zerodha API Integration

## Step 1: Get Zerodha API Access

### Create Kite Connect App

1. Go to [Kite Connect](https://developers.kite.trade/)
2. Sign up or log in with your Zerodha account
3. Click "Create New App"
4. Fill in details:
   - **App Name**: Your app name (e.g., "AlgoTrader")
   - **Redirect URL**: `http://127.0.0.1:5000` (for local development)
   - **Description**: Brief description
5. Submit and note down:
   - **API Key**
   - **API Secret**

### Generate Access Token

You have two options:

#### Option A: Manual Login Flow (Recommended for Testing)

```python
from kiteconnect import KiteConnect

api_key = "your_api_key"
api_secret = "your_api_secret"

kite = KiteConnect(api_key=api_key)

# Step 1: Get login URL
login_url = kite.login_url()
print(f"Visit this URL and login: {login_url}")

# After login, you'll be redirected to: http://127.0.0.1:5000/?request_token=XXXXX
request_token = input("Enter the request_token from URL: ")

# Step 2: Generate access token
data = kite.generate_session(request_token, api_secret=api_secret)
access_token = data["access_token"]

print(f"Access Token: {access_token}")
# Save this token in .env file
```

Run this script once, copy the access token to `.env`

#### Option B: Automated (Advanced)

Use `selenium` to automate the login flow. See `scripts/get_token.py` (create if needed).

## Step 2: Configure .env

```bash
cp .env.example .env
```

Edit `.env`:

```
KITE_API_KEY=your_api_key_here
KITE_API_SECRET=your_api_secret_here
KITE_ACCESS_TOKEN=your_access_token_here
```

## Step 3: Verify Connection

Test your setup:

```python
from modules.zerodha_client import ZerodhaClient

client = ZerodhaClient()
instruments = client.get_instruments('NSE')
print(f"Connected! Found {len(instruments)} instruments")
```

## Important Notes

### Access Token Validity

- **Daily token**: Valid for ~24 hours, needs refresh daily
- **Solution**: Run the token generation script each morning before trading

### Rate Limits

- **Historical data**: 3 requests/second
- **Quotes**: No strict limit but be reasonable
- **Orders**: 10 requests/second per API key

### Trading Hours

- **Market open**: 9:15 AM IST
- **Market close**: 3:30 PM IST
- **Pre-market**: 9:00 AM - 9:15 AM

### Intraday (MIS) Requirements

- Requires sufficient margin
- All positions auto-squared off at 3:20 PM
- Cannot carry forward overnight

## Troubleshooting

### "Token is invalid or has expired"

→ Regenerate access token using the login flow

### "Insufficient funds"

→ Ensure you have enough margin for MIS orders

### "403 Forbidden"

→ Check if API key is correct and app is active

### Rate limit errors

→ Add delays between API calls (`time.sleep(0.5)`)

## Security Best Practices

1. **Never commit .env** to git (already in .gitignore)
2. **Use read-only tokens** if available (for screener/backtesting)
3. **Start with small amounts** in live mode
4. **Monitor logs** regularly
5. **Set capital limits** in config.py

## Next: Run Your First Backtest

Once setup is complete:

```bash
python main.py screener
python main.py backtest --symbol RELIANCE --days 30
```

See README.md for full usage guide.
