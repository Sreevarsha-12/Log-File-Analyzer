import random
from datetime import datetime, timedelta

ERROR_CODES = [200, 200, 200, 404, 500, 403]
REQUESTS = ["GET", "POST", "PUT", "DELETE"]
IPS = [f"192.168.1.{i}" for i in range(1, 60)]

def generate_logs(file_path, lines=50000):
    start_time = datetime.now()

    with open(file_path, "w") as f:
        for _ in range(lines):
            if random.randint(1, 20) == 5:
                f.write("CORRUPTED LOG ENTRY\n")
                continue

            timestamp = start_time + timedelta(seconds=random.randint(1, 100000))
            ip = random.choice(IPS)
            req = random.choice(REQUESTS)
            code = random.choice(ERROR_CODES)

            f.write(f"{timestamp} {ip} {req} {code}\n")

if __name__ == "__main__":
    generate_logs("logs/server.log")
