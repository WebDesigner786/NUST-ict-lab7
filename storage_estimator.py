import math

class StorageEstimator:
    """Utility class to estimate data storage requirements."""

    # Multipliers relative to Bytes (Decimal / Base-10)
    UNITS = {
        'B': 1,
        'KB': 1000,
        'MB': 1000**2,
        'GB': 1000**3,
        'TB': 1000**4,
        'PB': 1000**5
    }

    @staticmethod
    def format_bytes(size_in_bytes: float) -> str:
        """Converts raw bytes into a human-readable string format."""
        if size_in_bytes <= 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        i = int(math.floor(math.log(size_in_bytes, 1000)))
        i = min(i, len(units) - 1)
        
        scaled_size = size_in_bytes / (1000 ** i)
        return f"{scaled_size:.2f} {units[i]}"

    @classmethod
    def estimate_media(cls, num_items: int, avg_size_mb: float, redundancy_factor: float = 1.0) -> float:
        """Estimates storage for files/media given count and average size in MB."""
        total_bytes = num_items * (avg_size_mb * cls.UNITS['MB']) * redundancy_factor
        return total_bytes

    @classmethod
    def estimate_database_records(cls, num_records: int, bytes_per_record: int, index_overhead_pct: float = 20.0) -> float:
        """Estimates storage for DB records accounting for index overhead."""
        base_bytes = num_records * bytes_per_record
        total_bytes = base_bytes * (1 + (index_overhead_pct / 100.0))
        return total_bytes

    @classmethod
    def estimate_video_stream(cls, duration_hours: float, bitrate_mbps: float) -> float:
        """Estimates video storage based on streaming duration and bitrate (in Mbps)."""
        # Mbps -> Megabits per second; 8 bits = 1 byte
        bytes_per_second = (bitrate_mbps * 1_000_000) / 8
        total_seconds = duration_hours * 3600
        return bytes_per_second * total_seconds

    @classmethod
    def estimate_daily_logs(cls, daily_active_users: int, logs_per_user_per_day: int, avg_log_bytes: int, retention_days: int) -> float:
        """Estimates storage needed for logging over a retention period."""
        daily_bytes = daily_active_users * logs_per_user_per_day * avg_log_bytes
        return daily_bytes * retention_days

def convert_to_gb(size_in_mb):
    """Converts storage size from Megabytes to Gigabytes."""
    return size_in_mb / 1024

# Example usage within your storage estimator:
if __name__ == "__main__":
    # Assuming your program calculates storage in MB or KB
    estimated_mb = 4239  # Example value
    estimated_gb = convert_to_gb(estimated_mb)
    
    print(f"ESTIMATED STORAGE REQUIRED: {estimated_gb:.2f} GB")

def run_interactive_menu():
    estimator = StorageEstimator()
    
    print("=" * 50)
    print("        DATA STORAGE REQUIREMENT ESTIMATOR        ")
    print("=" * 50)
    print("Select an estimation scenario:")
    print("1. Media / File Storage (Photos, Videos, PDFs)")
    print("2. Database Table / Records")
    print("3. Video Recording / Streaming")
    print("4. Application Logs / User Event Tracking")
    print("=" * 50)

    choice = input("Enter choice (1-4): ").strip()

    if choice == '1':
        count = int(input("Number of files: "))
        avg_mb = float(input("Average file size in MB: "))
        backup = float(input("Redundancy/Backup multiplier (e.g., 1.0 for none, 2.0 for 1 backup copy): ") or "1.0")
        
        total_bytes = estimator.estimate_media(count, avg_mb, backup)
        
    elif choice == '2':
        records = int(input("Expected total records/rows: "))
        avg_bytes = int(input("Estimated size per row in Bytes: "))
        overhead = float(input("Index/Metadata overhead % (default 20%): ") or "20")
        
        total_bytes = estimator.estimate_database_records(records, avg_bytes, overhead)
        
    elif choice == '3':
        hours = float(input("Video duration in hours: "))
        bitrate = float(input("Video bitrate in Mbps (e.g., 5 for 1080p, 25 for 4K): "))
        
        total_bytes = estimator.estimate_video_stream(hours, bitrate)
        
    elif choice == '4':
        dau = int(input("Daily Active Users (DAU): "))
        logs_per_user = int(input("Average log events per user/day: "))
        log_size = int(input("Average size per log entry in Bytes (e.g., 200-500 B): "))
        retention = int(input("Retention period in days: "))
        
        total_bytes = estimator.estimate_daily_logs(dau, logs_per_user, log_size, retention)
        
    else:
        print("Invalid option selected.")
        return

    print("\n" + "-" * 50)
    print(f"ESTIMATED STORAGE REQUIRED: {estimator.format_bytes(total_bytes)}")
    print("-" * 50)


if __name__ == "__main__":
    run_interactive_menu()