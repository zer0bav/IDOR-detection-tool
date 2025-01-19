# IDOR Detection Tool

This tool is designed to test for **Insecure Direct Object References (IDOR)** vulnerabilities in web applications. It performs automated scans over a range of resource IDs, using provided authorization tokens and configurable headers. The tool can also check for sensitive information in HTTP responses.

## Features
- **Asynchronous Requests**: Fast scanning using `aiohttp`.
- **Header Manipulation**: Dynamically modify headers during runtime.
- **Keyword Detection**: Searches responses for sensitive data (e.g., `admin`, `username`, `email`).
- **Proxy Support**: Allows integration with tools like Burp Suite.
- **Configurable ID Range**: Test specific resource ID ranges.

---

## Prerequisites
- Python 3.7+
- Required Libraries:
  - `aiohttp`
  - `requests`
  - `argparse`
  - `urllib3`
  - `asyncio`
  - `re`

To install the required libraries, run:
```bash
pip install -r requirements.txt
```

---

## Usage
### Basic Command Structure
```bash
python idor_detection_tool.py -u <URL> -t <TOKEN> -r <START_ID> <END_ID> [OPTIONS]
```

### Arguments
| Argument                  | Description                                       | Required | Default |
|---------------------------|---------------------------------------------------|----------|---------|
| `-u`, `--url`            | The base URL to test (e.g., `https://example.com/resources/`). | Yes      | None    |
| `-t`, `--token`          | Authorization token for requests.                | No       | None    |
| `-r`, `--range`          | Range of resource IDs to test (start, end).       | No       | 1-100   |
| `-p`, `--proxy`          | Proxy URL for routing requests.                  | No       | None    |
| `-k`, `--keywords`       | List of keywords to search for in responses.      | No       | `admin`, `username`, `email` |
| `--manipulate-headers`   | Enable interactive header manipulation.           | No       | Disabled |

### Example Commands

#### Basic Usage
Scan the URL `https://example.com/resource/` for IDs 1 through 50:
```bash
python idor_detection_tool.py -u https://example.com/resource/ -r 1 50
```

#### Adding an Authorization Token
Add a Bearer token for requests:
```bash
python ıdordet.py -u https://example.com/resource/ -r 1 50 -t YOUR_TOKEN
```

#### Using a Proxy
Route requests through a proxy (e.g., Burp Suite):
```bash
python ıdordet.py -u https://example.com/resource/ -p http://127.0.0.1:8080
```

#### Enabling Header Manipulation
Enable interactive header modification:
```bash
python ıdordet.py -u https://example.com/resource/ --manipulate-headers
```

---

## How It Works
1. **Header Setup**: The tool uses a default `Authorization` header. When `--manipulate-headers` is enabled, you can add or modify headers dynamically.
2. **Resource Scanning**: The tool iterates over the specified ID range and sends asynchronous GET requests to the target URL.
3. **Response Validation**:
   - If the HTTP status code is `200`, it checks the response body for sensitive keywords.
   - Logs potential IDOR vulnerabilities and snippets of the response.

---

## Sample Output
### No Issues Found
```plaintext
[INFO] Starting IDOR detection...
[-] ID 1 is accessible but no sensitive data found.
[-] ID 2 is accessible but no sensitive data found.
```

### Potential IDOR Detected
```plaintext
[INFO] Starting IDOR detection...
[+] Potential IDOR detected at https://example.com/resource/5
Response result: {"admin": true, "username": "test_user"}
```

### Errors or Restrictions
```plaintext
[!] ID 6 returned status: 403
```

---

## Limitations
- Relies on user-provided keywords for sensitive data detection.
- Cannot automatically exploit detected vulnerabilities; manual verification is required.
- Limited to GET requests; does not support POST, PUT, or DELETE methods.

---

## Disclaimer
This tool is for **educational purposes only**. Unauthorized use against systems without permission may violate laws and regulations. Use responsibly!

