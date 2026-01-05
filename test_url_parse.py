import re

url = 'https://shopee.ph/Outdoor-Portable-Camping-Tent-2Person-Waterproof-Hiking-Shelter-i.25316261.2935397050'
print('URL:', url)

# Try different patterns
patterns = [
    r'\.i\.(\d+)\.(\d+)',  # Original
    r'-i\.(\d+)\.(\d+)',   # With hyphen
    r'i\.(\d+)\.(\d+)',    # Without leading dot/hyphen
]

for pattern in patterns:
    match = re.search(pattern, url)
    if match:
        print(f'Pattern "{pattern}" MATCH: {match.groups()}')
    else:
        print(f'Pattern "{pattern}" no match')
