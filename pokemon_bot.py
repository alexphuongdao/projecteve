#!/usr/bin/env python3
"""
Pokemon Center Trading Card Bot
A legitimate automation tool for monitoring and purchasing trading cards
from the Pokemon Center website.
"""

import json
import time
import sys
import logging
from datetime import datetime
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style, init

# Initialize colorama for colored console output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class PokemonCenterBot:
    """Bot for monitoring and purchasing Pokemon trading cards."""
    
    def __init__(self, config_path: str = 'config.json'):
        """
        Initialize the bot with configuration.
        
        Args:
            config_path: Path to the configuration JSON file
        """
        self.config = self._load_config(config_path)
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"{Fore.GREEN}Configuration loaded successfully")
            return config
        except FileNotFoundError:
            logger.error(f"{Fore.RED}Config file not found: {config_path}")
            logger.info(f"{Fore.YELLOW}Please copy config.example.json to config.json and update with your details")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"{Fore.RED}Invalid JSON in config file: {e}")
            sys.exit(1)
    
    def _init_driver(self):
        """Initialize Selenium WebDriver."""
        if self.driver is None:
            logger.info(f"{Fore.CYAN}Initializing Chrome WebDriver...")
            chrome_options = Options()
            
            if self.config.get('headless', False):
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info(f"{Fore.GREEN}WebDriver initialized successfully")
            except Exception as e:
                logger.error(f"{Fore.RED}Failed to initialize WebDriver: {e}")
                raise
    
    def check_product_availability(self) -> List[Dict]:
        """
        Check for available products on the Pokemon Center website.
        
        Returns:
            List of available products with details
        """
        available_products = []
        target_url = self.config['target_url']
        
        try:
            logger.info(f"{Fore.CYAN}Checking product availability at {target_url}")
            response = self.session.get(target_url, timeout=self.config.get('timeout_seconds', 10))
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Look for product cards/items (adjust selectors based on actual site structure)
            products = soup.find_all(['div', 'article'], class_=lambda x: x and any(
                term in str(x).lower() for term in ['product', 'item', 'card']
            ))
            
            for product in products:
                try:
                    # Extract product information
                    title_elem = product.find(['h2', 'h3', 'h4', 'a'], class_=lambda x: x and 'title' in str(x).lower())
                    if not title_elem:
                        title_elem = product.find('a')
                    
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown Product"
                    
                    # Check if it matches target products
                    is_target = any(target.lower() in title.lower() 
                                  for target in self.config.get('target_products', []))
                    
                    # Look for price
                    price_elem = product.find(['span', 'div'], class_=lambda x: x and 'price' in str(x).lower())
                    price_text = price_elem.get_text(strip=True) if price_elem else "N/A"
                    
                    # Look for availability/stock status
                    stock_elem = product.find(['button', 'span', 'div'], 
                                             string=lambda x: x and any(
                                                 term in str(x).lower() 
                                                 for term in ['add to cart', 'in stock', 'available']
                                             ))
                    
                    in_stock = stock_elem is not None
                    
                    # Get product link
                    link_elem = product.find('a', href=True)
                    link = link_elem['href'] if link_elem else None
                    if link and not link.startswith('http'):
                        link = f"https://www.pokemoncenter.com{link}"
                    
                    if is_target and in_stock:
                        product_info = {
                            'title': title,
                            'price': price_text,
                            'link': link,
                            'in_stock': in_stock
                        }
                        available_products.append(product_info)
                        logger.info(f"{Fore.GREEN}✓ Found available product: {title}")
                
                except Exception as e:
                    logger.debug(f"Error parsing product: {e}")
                    continue
            
            if not available_products:
                logger.info(f"{Fore.YELLOW}No target products currently in stock")
            
        except requests.RequestException as e:
            logger.error(f"{Fore.RED}Error fetching product page: {e}")
        
        return available_products
    
    def attempt_checkout(self, product_url: str):
        """
        Attempt to add product to cart and checkout.
        
        Args:
            product_url: URL of the product to purchase
        """
        if not self.config.get('auto_checkout', False):
            logger.info(f"{Fore.YELLOW}Auto-checkout is disabled. Opening browser for manual checkout...")
        
        try:
            self._init_driver()
            
            logger.info(f"{Fore.CYAN}Navigating to product page: {product_url}")
            self.driver.get(product_url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Try to find and click "Add to Cart" button
            try:
                add_to_cart_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, 
                        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to bag')]"
                    ))
                )
                
                if add_to_cart_button.is_enabled():
                    logger.info(f"{Fore.GREEN}Found 'Add to Cart' button, clicking...")
                    add_to_cart_button.click()
                    time.sleep(2)
                    
                    logger.info(f"{Fore.GREEN}✓ Product added to cart!")
                    
                    if self.config.get('auto_checkout', False):
                        self._complete_checkout()
                    else:
                        logger.info(f"{Fore.YELLOW}Please complete checkout manually in the browser")
                        logger.info(f"{Fore.YELLOW}Press Ctrl+C to stop the bot when done")
                        # Keep browser open
                        while True:
                            time.sleep(1)
                else:
                    logger.warning(f"{Fore.YELLOW}Add to Cart button is disabled")
                    
            except TimeoutException:
                logger.warning(f"{Fore.YELLOW}Could not find 'Add to Cart' button")
                logger.info(f"{Fore.YELLOW}Browser will remain open for manual action")
                while True:
                    time.sleep(1)
                    
        except Exception as e:
            logger.error(f"{Fore.RED}Error during checkout attempt: {e}")
    
    def _complete_checkout(self):
        """Complete the checkout process (only if auto_checkout is enabled)."""
        logger.info(f"{Fore.CYAN}Attempting to complete checkout...")
        
        try:
            # Navigate to cart
            cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//a[contains(@href, 'cart') or contains(@class, 'cart')]"))
            )
            cart_button.click()
            time.sleep(2)
            
            # Click checkout button
            checkout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'checkout')]"))
            )
            checkout_button.click()
            time.sleep(3)
            
            # Fill in shipping information
            user_info = self.config.get('user_info', {})
            
            # This is a template - actual implementation would need site-specific selectors
            logger.info(f"{Fore.YELLOW}Checkout form opened - automatic form filling requires site-specific implementation")
            logger.info(f"{Fore.YELLOW}Please complete checkout manually")
            
            # Keep browser open for manual completion
            while True:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"{Fore.RED}Error during checkout: {e}")
            logger.info(f"{Fore.YELLOW}Browser will remain open for manual completion")
            while True:
                time.sleep(1)
    
    def monitor_and_purchase(self):
        """Main loop to monitor products and attempt purchase when available."""
        logger.info(f"{Fore.CYAN}{'='*60}")
        logger.info(f"{Fore.CYAN}Pokemon Center Trading Card Bot Started")
        logger.info(f"{Fore.CYAN}{'='*60}")
        logger.info(f"{Fore.CYAN}Target URL: {self.config['target_url']}")
        logger.info(f"{Fore.CYAN}Target Products: {', '.join(self.config.get('target_products', []))}")
        logger.info(f"{Fore.CYAN}Check Interval: {self.config['check_interval_seconds']} seconds")
        logger.info(f"{Fore.CYAN}{'='*60}\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                logger.info(f"{Fore.BLUE}[Iteration {iteration}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Check for available products
                available = self.check_product_availability()
                
                if available:
                    logger.info(f"{Fore.GREEN}{'='*60}")
                    logger.info(f"{Fore.GREEN}PRODUCT(S) AVAILABLE!")
                    logger.info(f"{Fore.GREEN}{'='*60}")
                    
                    for product in available:
                        logger.info(f"{Fore.GREEN}Title: {product['title']}")
                        logger.info(f"{Fore.GREEN}Price: {product['price']}")
                        logger.info(f"{Fore.GREEN}Link: {product['link']}")
                        logger.info(f"{Fore.GREEN}{'-'*60}")
                        
                        if self.config.get('notification_enabled', True):
                            print(f"\n{Fore.YELLOW}{'*'*60}")
                            print(f"{Fore.YELLOW}🚨 ALERT: Product Available! 🚨")
                            print(f"{Fore.YELLOW}{'*'*60}\n")
                        
                        # Attempt checkout with first available product
                        if product['link']:
                            self.attempt_checkout(product['link'])
                            # After first successful attempt, exit
                            return
                else:
                    logger.info(f"{Fore.CYAN}Waiting {self.config['check_interval_seconds']} seconds before next check...")
                
                # Wait before next check
                time.sleep(self.config['check_interval_seconds'])
                
        except KeyboardInterrupt:
            logger.info(f"\n{Fore.YELLOW}Bot stopped by user")
        except Exception as e:
            logger.error(f"{Fore.RED}Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            logger.info(f"{Fore.CYAN}Closing browser...")
            self.driver.quit()
        logger.info(f"{Fore.CYAN}Bot shutdown complete")


def main():
    """Main entry point for the bot."""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("=" * 60)
    print("  Pokemon Center Trading Card Bot")
    print("  Automated Product Monitoring & Purchase Assistant")
    print("=" * 60)
    print(f"{Style.RESET_ALL}\n")
    
    # Check if config exists
    import os
    if not os.path.exists('config.json'):
        print(f"{Fore.RED}Error: config.json not found!")
        print(f"{Fore.YELLOW}Please copy config.example.json to config.json and update with your details")
        print(f"{Fore.YELLOW}Example: cp config.example.json config.json")
        sys.exit(1)
    
    # Create and run bot
    bot = PokemonCenterBot('config.json')
    bot.monitor_and_purchase()


if __name__ == '__main__':
    main()
