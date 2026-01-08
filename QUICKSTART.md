# Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure the Bot

```bash
# Copy the example config
cp config.example.json config.json

# Edit with your preferred editor
nano config.json  # or vim, code, etc.
```

**Minimum required changes in config.json:**
- Set your `target_products` (e.g., "Charizard", "Booster Box")
- Adjust `check_interval_seconds` (recommended: 30-60)
- Keep `auto_checkout: false` for safety (manual checkout)

### Step 3: Run the Bot

```bash
python pokemon_bot.py
```

The bot will:
1. Monitor the Pokemon Center trading card page
2. Alert you when target products are available
3. Open a browser to the product page
4. Let you complete the purchase manually

## Example Configuration

Minimal config.json for monitoring Booster Boxes:

```json
{
  "target_url": "https://www.pokemoncenter.com/category/trading-card-game",
  "check_interval_seconds": 30,
  "target_products": ["Booster Box", "ETB"],
  "auto_checkout": false,
  "headless": false,
  "timeout_seconds": 10
}
```

## Tips

- **First run**: Set `headless: false` to see what the bot does
- **Check interval**: 30-60 seconds is respectful to the server
- **Target products**: Use keywords that appear in product titles
- **Manual checkout**: Safer and recommended for first-time users

## Troubleshooting

**"Config file not found"**
- Make sure you created `config.json` from `config.example.json`

**Dependencies not installed**
- Run: `pip install -r requirements.txt`

**Chrome not found**
- Install Google Chrome browser
- The bot will auto-download the correct driver

## What's Next?

See the full [README.md](readme.md) for:
- Detailed configuration options
- Advanced features
- Troubleshooting guide
- Ethical usage guidelines
