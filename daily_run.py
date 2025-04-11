import json
import requests
import os
import time
from colorama import Fore, Style, init
import random
init(autoreset=True)  # Initialize colorama for colored console output

# Global Headers
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "x-api-key": "03ad7ea4-2b75"
}
PROXY_FILE = "proxy.txt" 
def load_proxies():
    proxies = []
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    proxies.append(line)
    return proxies

# Global proxy list
PROXIES = load_proxies()

# Function to get a random proxy
def get_random_proxy():
    all_proxies = load_proxies()
    if not all_proxies:
        return None
    chosen = random.choice(all_proxies)
    return {
        "http": chosen,
        "https": chosen
    }

def load_tokens_from_file(file_path):
    """Load tokens from token.txt file"""
    tokens = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                token = line.strip()
                if token:
                    tokens.append(token)
        
        print(f"{Fore.GREEN}📁 Loaded {len(tokens)} tokens from {file_path}{Fore.RESET}")
        return tokens
    except FileNotFoundError:
        print(f"{Fore.RED}❌{Fore.RESET} File {file_path} not found")
        return []

def check_user_info(token):
    """Check user information"""
    url = "https://event.goldstation.io/api-v2/user/info"
    headers = HEADERS.copy()
    headers["authorization"] = f"Bearer {token}"
    
    max_retries = 10
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        if not proxy:
            print(f"{Fore.RED}❌ No proxies available. Please add proxies to proxy.txt")
            return False
        
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
            result = response.json()
            
            if result.get("success"):
                data = result.get("data", {})
                address = data.get("address", "Unknown")
                user_level = data.get("userLevel", 0)
                accumulated_power = data.get("accumulatedPower", 0)
                today_click_power = data.get("todayClickPower", 0)
                power_per_sec = data.get("powerPerSec", 0)
                refferal_code = data.get("userReferralCode", "Unknown")
                
                print(f"{Fore.CYAN}📌 User Information: {Fore.RESET}")
                print(f"{Fore.YELLOW}     🔗 Address: {address}{Fore.RESET}")
                print(f"{Fore.GREEN}     💎 Level: {user_level}{Fore.RESET}")
                print(f"{Fore.YELLOW+Style.BRIGHT}     🪙 Gold: {accumulated_power}{Fore.RESET}")
                print(f"{Fore.CYAN}     🔋 Power: {today_click_power}{Fore.RESET}")
                print(f"{Fore.GREEN+Style.BRIGHT}     ⚡ Speed: {power_per_sec}{Fore.RESET}")
                print(f"{Fore.CYAN}     🌟 Referral Code: {refferal_code}{Fore.RESET}")
                
                return True
            else:
                print(f"{Fore.RED}🚫 Failed to get user info: {result.get('message', 'Unknown error')}")
                if attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                    time.sleep(2)
                    continue
                return False
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            print(f"{Fore.YELLOW}⚠️ Proxy connection failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            print(f"{Fore.RED}❌ All proxy attempts failed")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            return False

def check_referral(token):
    """Check referral information"""
    url = "https://event.goldstation.io/api-v2/user/referral"
    headers = HEADERS.copy()
    headers["authorization"] = f"Bearer {token}"
    
    max_retries = 10
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        if not proxy:
            print(f"{Fore.RED}❌ No proxies available. Please add proxies to proxy.txt")
            return False
        
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
            result = response.json()
            
            if result.get("success"):
                data = result.get("data", {})
                referral_history = data.get("referralHistory", [])
                
                print(f"{Fore.CYAN}📌 Referral Information:")
                if referral_history:
                    print(f"{Fore.GREEN}     👥 Total Referrals: {len(referral_history)}")
                else:
                    print(f"{Fore.YELLOW}     👥 No referrals yet")
                
                return True
            else:
                print(f"{Fore.RED}🚫 Failed to get referral info: {result.get('message', 'Unknown error')}")
                if attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                    time.sleep(2)
                    continue
                return False
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            print(f"{Fore.YELLOW}⚠️ Proxy connection failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            print(f"{Fore.RED}❌ All proxy attempts failed")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            return False

def check_daily_status(token):
    """Check daily check-in status"""
    url = "https://event.goldstation.io/api-v2/user/daily"
  
    headers = HEADERS.copy()
    headers["authorization"] = f"Bearer {token}"
    
    max_retries = 10
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        if not proxy:
            print(f"{Fore.RED}❌ No proxies available. Please add proxies to proxy.txt")
            return False
        
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                data = result.get("data", {})
                continuous_days = data.get("continuousDays", 0)
                total_days = data.get("totalDays", 0)
                today_checked = data.get("todayChecked", False)
                
                print(f"{Fore.CYAN}📌 Daily Check-in Status:")
                print(f"{Fore.CYAN}     📅 Continuous Days: {Fore.YELLOW+Style.BRIGHT}{continuous_days} / {total_days}{Fore.RESET}")
                print(f"{Fore.CYAN}     ❤️ Today Checked: {Fore.YELLOW+Style.BRIGHT}{today_checked}{Fore.RESET}")
                
                return today_checked
            else:
                print(f"{Fore.RED}🚫 Failed to get daily status: {result.get('message', 'Unknown error')}")
                return False
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            print(f"{Fore.YELLOW}⚠️ Proxy connection failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            print(f"{Fore.RED}❌ All proxy attempts failed")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            return False    

def perform_daily_checkin(token):
    """Perform daily check-in"""
    url = "https://event.goldstation.io/api-v2/user/daily"
  
    headers = HEADERS.copy()
    headers["authorization"] = f"Bearer {token}"
    
    max_retries = 10
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        if not proxy:
            print(f"{Fore.RED}❌ No proxies available. Please add proxies to proxy.txt")
            return False
        
        try:
            response = requests.post(url, headers=headers, proxies=proxy, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                print(f"{Fore.GREEN}❤️ Daily check-in completed")
                return True
            else:
                print(f"{Fore.RED}🚫 Daily check-in failed: {result.get('message', 'Unknown error')}")
                return False
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            print(f"{Fore.YELLOW}⚠️ Proxy connection failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            print(f"{Fore.RED}❌ All proxy attempts failed")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            return False    

def mine(token, click_power=20000):
    """Perform mining action"""
    url = "https://event.goldstation.io/api-v2/user/click"
     
    headers = HEADERS.copy()
    headers["authorization"] = f"Bearer {token}"
    
    data = {"clickPower": click_power}
    
    max_retries = 10
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        if not proxy:
            print(f"{Fore.RED}❌ No proxies available. Please add proxies to proxy.txt")
            return False
        
        try:
            response = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                data = result.get("data", {})
                daily_max = data.get("dailyMax", 0)
                current = data.get("current", 0)
                remaining = data.get("remaining", 0)
                
                print(f"{Fore.GREEN}     ⛏️ Mining successful")
                print(f"{Fore.CYAN}     💡 Daily Max: {Fore.GREEN}{daily_max}{Fore.RESET}")
                print(f"{Fore.CYAN}     💡 Current: {Fore.GREEN}{current}{Fore.RESET}")
        
                
                return remaining > 0
            else:
                print(f"{Fore.RED}🚫 Mining failed: {result.get('message', 'Unknown error')}")
                return False
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            print(f"{Fore.YELLOW}⚠️ Proxy connection failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            print(f"{Fore.RED}❌ All proxy attempts failed")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            return False    

def upgrade_level(token):
    """Upgrade user level"""
    url = "https://event.goldstation.io/api-v2/user/levelup"
   
    headers = HEADERS.copy()
    headers["authorization"] = f"Bearer {token}"
    max_retries = 10
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        if not proxy:
            print(f"{Fore.RED}❌ No proxies available. Please add proxies to proxy.txt")
            return False
        
        try:
            response = requests.post(url, headers=headers, proxies=proxy, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                print(f"{Fore.GREEN}✨ Level upgrade successful")
                return True, result
            else:
                message = result.get('message', 'Unknown error')
                print(f"{Fore.YELLOW}🚨 Level upgrade: {message}")
                return False, result
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            print(f"{Fore.YELLOW}⚠️ Proxy connection failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            print(f"{Fore.RED}❌ All proxy attempts failed")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}🔄 Retrying with a different proxy... Attempt {attempt + 2}/{max_retries}")
                time.sleep(2)
                continue
            return False   

def print_welcome_message():
    print(Fore.WHITE + r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "DAILY RUN GOLDSTATION")
    print(Fore.YELLOW + Style.BRIGHT + "Join @sirkel_testnet / @ghalibie_sharing \n\n")
    
    
def clear_cmd():
    # Check if the operating system is Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        
def main():
    print_welcome_message()
    
    # Load tokens from token.txt
    tokens = load_tokens_from_file('token.txt')
    
    if not tokens:
        print(f"{Fore.RED}❌{Fore.RESET} No tokens found in token.txt")
        return
    
    # Process each token
    for i, token in enumerate(tokens, start=1):
        print(f"\n{Fore.CYAN}{'='*50}{Fore.RESET}")
        print(f"{Fore.YELLOW+Style.BRIGHT}➤ Processing {Fore.MAGENTA}{i}{Fore.RESET}/{Fore.GREEN}{len(tokens)}{Fore.RESET}")
        print(f"{Fore.CYAN}{'='*50}{Fore.RESET}\n")
        
        # Check user info
        if not check_user_info(token):
            print(f"{Fore.RED}❌{Fore.RESET} Failed to get user info, skipping token")
            continue
            
        # Check referral
        if not check_referral(token):
            print(f"{Fore.RED}❌{Fore.RESET} Failed to get referral info, skipping token")
            continue
        
        # Check daily status
        today_checked = check_daily_status(token)
        time.sleep(2)
        # Perform daily check-in if not already checked
        if not today_checked:
            print(f"{Fore.BLUE}INFO{Fore.RESET} Performing daily check-in...")
            perform_daily_checkin(token)
        
        # Mine until no more clicks available
        print(f"{Fore.BLUE+Style.BRIGHT}⚒️ Starting mining...")
        can_mine = True
        while can_mine:
            can_mine = mine(token)
            if can_mine:
                time.sleep(2)  # Small delay between mining actions
        
        # Try to upgrade level
        print(f"{Fore.BLUE+Style.BRIGHT}📌 Attempting to upgrade level {Fore.RESET}")
        can_upgrade = True
        while can_upgrade:
            success, result = upgrade_level(token)
          
            can_upgrade = success
            if can_upgrade:
                # After successful upgrade, try mining again
                # print(f"[ {Fore.BLUE}INFO{Fore.RESET} ] Level upgraded, mining again...")
                can_mine = True
                while can_mine:
                    can_mine = mine(token)
                    if can_mine:
                        time.sleep(2)  # Small delay between mining actions
            else:
                # If upgrade failed, check if it's because of not enough power
                if "Not enough power to level up" in result.get('message', ''):
                    break
        
        print(f"\n{Fore.CYAN}{'='*50}{Fore.RESET}\n")
        time.sleep(3)  # Delay between tokens

if __name__ == "__main__":
    main() 