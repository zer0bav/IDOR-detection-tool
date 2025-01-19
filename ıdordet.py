import requests
import argparse
from urllib.parse import urljoin
import asyncio
from aiohttp import ClientSession
import re

def validate_response(response_text, keywords):
    """check sens info in response"""
    for keyword in keywords:
        if re.search(keyword, response_text, re.IGNORECASE):
            return True
    return False

async def async_request(url, headers, session):
    """async GET req."""
    try:
        async with session.get(url, headers=headers) as response:
            response_text = await response.text()
            return response.status, response_text
    except Exception as e:
        return None, str(e)

def main():
    parser = argparse.ArgumentParser(description="IDOR Detection Tool")
    parser.add_argument("-u", "--url", required=True, help="url test")
    parser.add_argument("-t", "--token", required=False, help="token")
    parser.add_argument("-r", "--range", type=int, nargs=2, help="ID range to test (start end)")
    parser.add_argument("-p", "--proxy", help="proxy URL (ex., http://127.0.0.1:8080)")
    parser.add_argument("-k", "--keywords", nargs='+', default=["admin", "username", "email"],
                        help="keywords to search in responses")
    parser.add_argument("--manipulate-headers", action="store_true", help="enable header manipulation")                    
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    headers = {"Authorization": f"Bearer {args.token}"}
    if args.proxy:
        proxy = {"http": args.proxy, "https": args.proxy}
    else:
        proxy = None
    id_range = args.range or (1, 100)
    if args.manipulate_headers:
        print("[INFO] header manipulation enabled.")
        while True:
            print("\nCurrent Headers:")
            for key, value in headers.items():
                print(f"{key}: {value}")

            key = input("input header key to modify (press [Enter] to continue): ")
            if not key:
                break

            value = input(f"enter new value for header '{key}': ")
            if value:
                headers[key] = value
                print(f"[INFO] header '{key}' updated to '{value}'")
            else:
                print(f"[INFO] header '{key}' not updated.")


    async def test_idor():
        tasks = []
        async with ClientSession() as session:
            for resource_id in range(id_range[0], id_range[1] + 1):
                target_url = urljoin(base_url, str(resource_id))
                tasks.append(async_request(target_url, headers, session))

            responses = await asyncio.gather(*tasks)

            for i, (status, response_text) in enumerate(responses):
                resource_id = id_range[0] + i
                if status == 200:
                    if validate_response(response_text, args.keywords):
                        print(f"[+] potential IDOR detected at {base_url}/{resource_id}")
                        print(f"response result: {response_text[:200]}\n")
                    else:
                        print(f"[-] ID {resource_id} is accessible but no sensitive data found.")
                else:
                    print(f"[!] ID {resource_id} returned status: {status}")

    print("[INFO] starting IDOR detection...")
    asyncio.run(test_idor())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[INFO] Exiting...")