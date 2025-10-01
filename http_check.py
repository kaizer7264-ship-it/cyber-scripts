import requests

url = input("Enter website URL (include http:// or https://): ")
try:
    response = requests.get(url)
    print(f"\n[+] Status Code: {response.status_code}")

    # Check if HTTPS is used
    if url.startswith("https://"):
        print("[+] Connection is secure (HTTPS)")
    else:
        print("[-] Connection is not secure (HTTP)")

    # Print common security headers if they exist
    headers = ["Content-Security-Policy", "X-Frame-Options", "Strict-Transport-Security", "X-Content-Type-Options"]
    print("\n[+] Security Headers Found:")
    for h in headers:
        if h in response.headers:
            print(f"   - {h}: {response.headers[h]}")
        else:
            print(f"   - {h}: Missing")

except Exception as e:
    print("[-] Error:", e)
