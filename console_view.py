from database import SessionLocal, LogEntry


def show_in_console():
    db = SessionLocal()
    ip_filter = input("Введите IP для фильтрации (или Enter для всех): ")

    query = db.query(LogEntry)
    if ip_filter:
        query = query.filter(LogEntry.ip == ip_filter)

    logs = query.limit(20).all()
    print(f"{'IP':<15} | {'Date':<20} | {'URL':<30} | {'Status'}")
    print("-" * 75)
    for l in logs:
        print(f"{l.ip:<15} | {str(l.timestamp):<20} | {l.url[:30]:<30} | {l.status}")
    db.close()


if __name__ == "__main__":
    show_in_console()
