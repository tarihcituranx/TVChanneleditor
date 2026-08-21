import glob
import re

for file in glob.glob('templates/base*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the select block
    select_match = re.search(r'(<select id="lang-selector"[^>]*>)(.*?)(</select>)', content, re.DOTALL)
    if select_match:
        start_tag = select_match.group(1)
        options_block = select_match.group(2)
        end_tag = select_match.group(3)
        
        # Extract individual options
        options = re.findall(r'<option[^>]*>.*?</option>', options_block)
        
        # Sort options alphabetically by the value attribute
        options.sort(key=lambda x: re.search(r'value="(.*?)"', x).group(1))
        
        # Reconstruct the block
        sorted_options = "\n                    ".join(options)
        new_block = f"{start_tag}\n                    {sorted_options}\n                {end_tag}"
        
        content = content.replace(select_match.group(0), new_block)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Language dropdowns sorted!")
