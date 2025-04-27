# WhatsApp Group Chat Analysis Script
# Reads a WhatsApp chat export, counts messages per sender, 
# computes percentages, and flags any user >25% of total.

import re
from collections import defaultdict

# Change this to your actual chat file name/path
CHAT_FILE = "_chat.txt"

# Compile a regex that grabs whatever appears after "] " up to the first colon
pattern = re.compile(r"\] ([^:]+?):")

# Use defaultdict so we can safely do `+= 1` without KeyError
user_counts = defaultdict(int)

# Read & parse
with open(CHAT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            sender = match.group(1).strip()
            user_counts[sender] += 1

if not user_counts:
    print("No messages found (check your file/pattern).")
    exit(0)

# Sort users by message count (descending)
sorted_counts = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)
total_msgs = sum(user_counts.values())

# Display summary
print("\nWhatsApp Group Message Count")
print("-----------------------------")
for user, count in sorted_counts:
    percent = (count / total_msgs) * 100
    print(f"{user}: {count} messages ({percent:.1f}%)")

# Flag any "dominant" users >25% of total
dominant = [u for u, c in sorted_counts if c / total_msgs > 0.25]
if dominant:
    print("\nDominant Users Detected (>25% of total):")
    for u in dominant:
        print(f" - {u}")
