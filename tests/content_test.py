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

def get_score(version, sentence):
    r = requests.get(
        url=f"http://{api_address}:{api_port}/{version}/sentiment",
        params={"username": "alice", "password": "wonderland", "sentence": sentence},
        timeout=10,
    )
    if r.status_code != 200:
        return r.status_code, None
    data = r.json()
    score = data.get("score", None)
    return r.status_code, score

def check_sign(score, expected_sign):
    if score is None:
        return False
    if expected_sign == "positive":
        return score > 0
    return score < 0

def run_tests():
    cases = [
        ("life is beautiful", "positive"),
        ("that sucks", "negative"),
    ]
    versions = ["v1", "v2"]

    for version in versions:
        for sentence, expected_sign in cases:
            status_code, score = get_score(version, sentence)
            ok = (status_code == 200) and check_sign(score, expected_sign)
            test_status = "SUCCESS" if ok else "FAILURE"

            output = f"""
============================
    Content test
============================

request done at "/{version}/sentiment"
| username="alice"
| password="wonderland"
| sentence="{sentence}"

Expected result = 200 and score {expected_sign};
actual result = {status_code} and score = {score}

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
    Content test
============================

API not reachable on /status within timeout

==>  FAILURE

"""
        print(out)
        write_log(out)
        raise SystemExit(1)

    run_tests()

if __name__ == "__main__":
    main()
