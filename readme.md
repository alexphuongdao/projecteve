# Pokemon Center Trading Card Bot

A legitimate automation tool for monitoring and purchasing Pokemon trading cards from the [Pokemon Center website](https://www.pokemoncenter.com/category/trading-card-game).

## Features

- 🔍 **Product Monitoring**: Continuously monitors the Pokemon Center trading card page for product availability
- 🛒 **Automated Checkout**: Option to automatically add products to cart and assist with checkout
- ⚙️ **Configurable**: Customize target products, check intervals, and price limits
- 📊 **Logging**: Detailed logging of all bot activities
- 🎨 **Colored Console Output**: Easy-to-read status updates
- 🔔 **Notifications**: Visual alerts when products become available

## Disclaimer

This bot is designed for **legitimate personal use only** to help you make purchases on the Pokemon Center website. Users are responsible for:
- Complying with Pokemon Center's Terms of Service
- Using the bot ethically and responsibly
- Not engaging in reselling or scalping activities
- Respecting rate limits and not overwhelming the server

## Installation

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- pip (Python package manager)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/alexphuongdao/projecteve.git
cd projecteve
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create your configuration file:
```bash
cp config.example.json config.json
```

4. Edit `config.json` with your preferences and information:
```bash
nano config.json  # or use your preferred text editor
```

## Configuration

The `config.json` file contains all bot settings:

```json
{
  "target_url": "https://www.pokemoncenter.com/category/trading-card-game",
  "check_interval_seconds": 30,
  "target_products": [
    "Booster Box",
    "Elite Trainer Box",
    "Collection Box"
  ],
  "max_price": 200.0,
  "notification_enabled": true,
  "auto_checkout": false,
  "user_info": {
    "email": "your-email@example.com",
    "first_name": "FirstName",
    "last_name": "LastName",
    "address": "123 Main St",
    "city": "City",
    "state": "ST",
    "zip": "12345",
    "phone": "555-555-5555"
  },
  "headless": false,
  "timeout_seconds": 10
}
```

### Configuration Options

- **target_url**: The Pokemon Center category page to monitor
- **check_interval_seconds**: How often to check for product availability (recommended: 30-60 seconds)
- **target_products**: List of product keywords to look for
- **max_price**: Maximum price you're willing to pay (currently informational)
- **notification_enabled**: Enable console notifications when products are found
- **auto_checkout**: Enable automatic checkout (disabled by default for safety)
- **user_info**: Your shipping information (only used if auto_checkout is enabled)
- **headless**: Run browser in headless mode (false = visible browser)
- **timeout_seconds**: Request timeout in seconds

## Usage

### Basic Usage

Run the bot with:

```bash
python pokemon_bot.py
```

The bot will:
1. Start monitoring the configured Pokemon Center page
2. Check for product availability at regular intervals
3. Alert you when target products are found
4. Open a browser window to the product page
5. Allow you to complete the purchase manually

### Advanced Usage

#### Headless Mode

To run the bot without opening a visible browser window, set `"headless": true` in your config:

```json
{
  "headless": true
}
```

#### Auto-Checkout (Use with Caution)

⚠️ **Warning**: Auto-checkout is experimental and disabled by default.

To enable automatic checkout, set `"auto_checkout": true` in your config and ensure your `user_info` is correctly filled out.

## How It Works

1. **Monitoring Phase**:
   - The bot makes HTTP requests to the Pokemon Center trading card page
   - It parses the HTML to find product listings
   - It checks if any products match your target keywords
   - It verifies if products are in stock

2. **Alert Phase**:
   - When a target product is found in stock, the bot alerts you
   - It displays product details (title, price, link)
   - It provides visual and console notifications

3. **Purchase Phase**:
   - The bot opens a Chrome browser to the product page
   - It attempts to click the "Add to Cart" button
   - It keeps the browser open for you to complete checkout manually
   - (Optional) If auto_checkout is enabled, it assists with the checkout process

## Logs

All bot activity is logged to:
- Console output (colored and formatted)
- `bot.log` file (detailed logging for troubleshooting)

## Troubleshooting

### Common Issues

**"Config file not found" error**
- Make sure you've copied `config.example.json` to `config.json`
- Ensure the file is in the same directory as `pokemon_bot.py`

**"Could not find 'Add to Cart' button" warning**
- The website structure may have changed
- The product might be out of stock
- The bot will keep the browser open for manual action

**Chrome driver issues**
- The bot automatically downloads the correct ChromeDriver
- Ensure Google Chrome is installed on your system
- Try updating Chrome to the latest version

**Rate limiting or blocked requests**
- Increase `check_interval_seconds` to be more respectful
- The bot includes user-agent headers to appear as a normal browser
- Avoid running multiple instances simultaneously

## Ethical Considerations

This tool is provided for **personal use only**. Please use it responsibly:

- ✅ Use it to help you make legitimate purchases for your own collection
- ✅ Respect the website's servers by using reasonable check intervals
- ✅ Follow Pokemon Center's Terms of Service
- ❌ Don't use it for bulk purchasing or reselling
- ❌ Don't run multiple instances to gain unfair advantages
- ❌ Don't use it to deprive other collectors of products

## Legal

This software is provided "as is" without warranty of any kind. Users are solely responsible for their use of this software and must comply with all applicable laws and terms of service.

## Contributing

This is a personal project, but suggestions and improvements are welcome. Please open an issue or submit a pull request.

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please open an issue on GitHub.

---

**Remember**: Use this bot ethically and responsibly. Happy collecting! 🎴
