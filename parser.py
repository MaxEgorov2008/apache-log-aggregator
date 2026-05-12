import re
import glob
import os
import yaml
from datetime import datetime
from database import SessionLocal, LogEntry

# Регулярное выражение для формата Apache Combined
LOG_PATTERN = r'^(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+)\s?(\S+)?\s?(\S+)?" (\d{3}|-) (\d+|-)$'


def parse_logs():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    db = SessionLocal()
    path = os.path.join(config['app']['log_directory'], config['app']['log_mask'])

    for file_path in glob.glob(path):
        try:
            with open(file_path, "r") as f:
                for line in f:
                    match = re.match(LOG_PATTERN, line)
                    if match:
                        data = match.groups()
                        entry = LogEntry(
                            ip=data[0],
                            timestamp=datetime.strptime(data[1], '%d/%b/%Y:%H:%M:%S %z'),
                            method=data[2],
                            url=data[3],
                            status=int(data[5]) if data[5] != '-' else 0,
                            size=int(data[6]) if data[6] != '-' else 0
                        )
                        db.add(entry)
            db.commit()
        except Exception as e:
            print(f"Ошибка при чтении {file_path}: {e}")
    db.close()


if __name__ == "__main__":
    parse_logs()