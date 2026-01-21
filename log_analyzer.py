import re
import logging
import pandas as pd
from collections import Counter

LOG_PATTERN = re.compile(
    r'(?P<timestamp>[\d\-:\. ]+) (?P<ip>\d+\.\d+\.\d+\.\d+) (?P<request>[A-Z]+) (?P<code>\d{3})'
)

logging.basicConfig(
    filename="app_logs/execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def analyze_log(file_path):
    total_requests = 0
    error_counter = Counter()
    ip_counter = Counter()
    records = []

    with open(file_path, "r") as file:
        for line_no, line in enumerate(file, start=1):
            try:
                total_requests += 1
                match = LOG_PATTERN.search(line)

                if not match:
                    raise ValueError("Malformed entry")

                data = match.groupdict()
                code = int(data["code"])

                records.append(data)

                if code >= 400:
                    error_counter[code] += 1
                    ip_counter[data["ip"]] += 1

            except Exception as e:
                logging.warning(f"Line {line_no}: {e}")

    logging.info("Log analysis completed")

    summary = {
        "total_requests": total_requests,
        "total_errors": sum(error_counter.values()),
        "error_frequency": dict(error_counter),
        "top_ips": ip_counter.most_common(5)
    }

    return summary, pd.DataFrame(records)
