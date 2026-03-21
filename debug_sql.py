import re

with open('backups/shuwei_data_manager_20260320_235846.sql', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-16-le', errors='ignore')

# Find knowledge_docs section
pattern = r'LOCK TABLES `knowledge_docs` WRITE;(.+?)UNLOCK TABLES'
match = re.search(pattern, content, re.DOTALL)

if match:
    data_section = match.group(1)
    print(f'Data section length: {len(data_section)}')

    # Find INSERT VALUES
    values_pattern = r'INSERT INTO `knowledge_docs` VALUES (.+?);'
    values_match = re.search(values_pattern, data_section, re.DOTALL)

    if values_match:
        values_str = values_match.group(1)
        print(f'VALUES length: {len(values_str)}')
        print(f'First 200 chars: {repr(values_str[:200])}')
        print(f'Last 200 chars: {repr(values_str[-200:])}')

        # Count opening and closing parentheses
        open_count = values_str.count('(')
        close_count = values_str.count(')')
        print(f'\nParentheses: open={open_count}, close={close_count}')

        # Count records by ),(
        record_count = values_str.count('),(')
        print(f'Record separators ),(: {record_count}')
else:
    print('No match found')