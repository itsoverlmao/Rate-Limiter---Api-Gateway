import requests
import time


def test_burst():
    url = "http://127.0.0.1:8000/"
    allowed=0
    blocked=0


    for i in range(15):
        response = requests.get(url)
        if response.status_code == 200:
            allowed += 1
        elif response.status_code == 429:
            blocked += 1
    
    print()
    print(f"Allowed: {allowed}, Blocked: {blocked}")

def test_recovery():
    url = "http://127.0.0.1:8000/"
    for i in range(10):
        response = requests.get(url)
        print(f"Attempt {i+1}: Status Code: {response.status_code}")  
    # Wait for 1 second to allow token bucket to refill
    time.sleep(1)
    response = requests.get(url)
    print(f"Final Attempt: Status Code: {response.status_code}")


if __name__ == "__main__":
    print("Testing burst of requests:")
    test_burst()
    time.sleep(10)  # Wait for 10 seconds to allow token bucket to refill
    print("\nTesting recovery after burst:")
    test_recovery()