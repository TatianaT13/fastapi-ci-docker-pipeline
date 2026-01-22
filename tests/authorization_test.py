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

def call_sentiment(version, username, password, sentence):
    endpoint = f"/{version}/sentiment"
    r = requests.get(
        url=f"http://{api_address}:{api_port}{endpoint}",
        params={"username": username, "password": password, "sentence": sentence},
        timeout=10,
    )
    return r.status_code

def run_matrix():
    tests = [
        ("bob", "builder", "v1", 200),
        ("bob", "builder", "v2", 403),
        ("alice", "wonderland", "v1", 200),
        ("alice", "wonderland", "v2", 200),
    ]

    sentence = "life is beautiful"

    for username, password, version, expected_code in tests:
        status_code = call_sentiment(version, username, password, sentence)
        test_status = "SUCCESS" if status_code == expected_code else "FAILURE"

        output = f"""
============================
    Authorization test
============================

request done at "/{version}/sentiment"
| username="{username}"
| password="{password}"
| sentence="{sentence}"

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
    Authorization test
============================

API not reachable on /status within timeout

==>  FAILURE

"""
        print(out)
        write_log(out)
        raise SystemExit(1)

    run_matrix()

if __name__ == "__main__":
    main()
