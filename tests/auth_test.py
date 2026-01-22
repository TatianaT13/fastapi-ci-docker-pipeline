import os
import time
import requests

api_address = os.environ.get("API_ADDRESS", "localhost")
api_port = int(os.environ.get("API_PORT", "8000"))
log_enabled = os.environ.get("LOG", "0") == "1"
log_path = os.environ.get("LOG_PATH", "api_test.log")

def wait_api(timeout_s=60):
    url = f"http://{api_address}:{api_port}/status"
    start = time.time()
    while time.time() - start < timeout_s:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False

def write_log(text):
    if log_enabled:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(text)

def run_case(username, password, expected_code):
    r = requests.get(
        url=f"http://{api_address}:{api_port}/permissions",
        params={"username": username, "password": password},
        timeout=10,
    )
    status_code = r.status_code
    test_status = "SUCCESS" if status_code == expected_code else "FAILURE"

    output = f"""
============================
    Authentication test
============================

request done at "/permissions"
| username="{username}"
| password="{password}"

Expected result = {expected_code};
actual result = {status_code}

==>  {test_status}

"""
    print(output)
    write_log(output)

    if test_status != "SUCCESS":
        raise SystemExit(1)

def main():
    if not wait_api():
        out = """
============================
    Authentication test
============================

API not reachable on /status within timeout

==>  FAILURE

"""
        print(out)
        write_log(out)
        raise SystemExit(1)

    run_case("alice", "wonderland", 200)
    run_case("bob", "builder", 200)
    run_case("clementine", "mandarine", 403)

if __name__ == "__main__":
    main()
