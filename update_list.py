# update_list.py
import os
import glob
import re
import sys
from bs4 import BeautifulSoup

# --- Installation check for dependencies ---
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Lỗi: Thư viện 'beautifulsoup4' chưa được cài đặt.", file=sys.stderr)
    print("Vui lòng chạy lệnh sau trong terminal của bạn:", file=sys.stderr)
    print("pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

OUTPUT_FILE = "chudiem-list.html"
IGNORED_FILES = ["tool.html", "index.html", "trietgia.html", OUTPUT_FILE]

def extract_poster_info(file_path):
    """Parses an HTML file and extracts poster information if it's a valid poster."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Check for the marker meta tag
        marker = soup.find('meta', attrs={'name': 'xth-poster', 'content': 'true'})
        if not marker:
            return None

        # Extract info
        num_element = soup.select_one('header div.text-right > p.font-sans')
        topic_element = soup.select_one('div.mt-8 > p.text-poster-accent')
        quote_element = soup.find('p', id='quote')


        if not num_element or not topic_element or not quote_element:
            print(f"Cảnh báo: File '{file_path}' trông giống poster nhưng thiếu thông tin cần thiết.")
            return None

        # Extract number as an integer for sorting
        num_text = num_element.get_text(strip=True)
        num_match = re.search(r'\d+', num_text)
        if not num_match:
            return None
        
        poster_num = int(num_match.group(0))
        poster_topic = topic_element.get_text(strip=True)
        
        # Generate a title from the quote
        quote_text = quote_element.get_text(strip=True)[1:] # remove drop cap
        poster_title = ' '.join(quote_text.split()[:5]) + '...'


        return {
            "path": file_path,
            "number": poster_num,
            "number_text": num_text,
            "title": poster_title,
            "topic": poster_topic,
        }
    except Exception as e:
        print(f"Lỗi khi xử lý file '{file_path}': {e}")
        return None

def build_list_item_html(poster):
    """Generates the HTML for a single list item."""
    return f"""
                <!-- Item {poster['number']} -->
                <a href="{poster['path']}" class="list-item block p-6 md:p-8">
                    <div class="flex justify-between items-start">
                        <div>
                            <p class="font-sans text-xs font-bold tracking-[0.2em] uppercase mb-2 text-poster-accent">{poster['number_text']}</p>
                            <h3 class="item-title font-serif text-3xl font-bold text-poster-black">{poster['title']}</h3>
                        </div>
                        <div class="text-right flex-shrink-0 ml-4">
                            <p class="font-sans text-sm font-semibold text-poster-black/70">{poster['topic']}</p>
                        </div>
                    </div>
                </a>"""

def build_html_structure(list_items_html):
    """Builds the final HTML page with the generated list items."""
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Danh sách: Những Chủ Điểm Triết Học Nhỏ</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'poster-bg': '#EAEAEA',
                        'poster-black': '#121212',
                        'poster-accent': '#CC3300',
                    }},
                    fontFamily: {{
                        serif: ['"Playfair Display"', 'serif'],
                        sans: ['"Inter"', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #222; /* Nền tối như viền poster */
        }}
        .list-item {{
            transition: background-color 0.3s ease;
        }}
        .list-item:hover {{
            background-color: #fff;
        }}
        .list-item:hover .item-title {{
            color: #CC3300; /* poster-accent */
        }}
    </style>
</head>
<body class="text-poster-black">
    <div class="max-w-4xl mx-auto my-12 md:my-20 px-4">
        <header class="p-8 pb-4 flex justify-between items-center border-b-2 border-gray-500 mb-10">
            <div class="flex flex-col gap-1">
                 <a href="index.html" class="flex items-center gap-2 text-gray-300 hover:text-white">
                    <img src="xomtriethoc.png" alt="Logo Xóm" class="w-10 h-10 object-contain">
                    <span class="text-xs uppercase tracking-wider font-bold">Xóm Triết học</span>
                 </a>
            </div>
            <div class="flex flex-col gap-1 items-end">
                 <a href="#" class="flex items-center gap-2 text-gray-300">
                    <span class="text-xs uppercase tracking-wider font-bold">Trung tâm Chí Dũng</span>
                    <img src="chidungcenterLogo.png" alt="Logo Chí Dũng" class="w-10 h-10 object-contain">
                 </a>
            </div>
        </header>
        <div class="mb-12 text-center">
            <h1 class="text-5xl md:text-6xl font-black font-sans leading-tight tracking-tighter text-white">
                NHỮNG CHỦ ĐIỂM
            </h1>
            <h2 class="text-5xl md:text-6xl font-serif italic font-normal text-poster-accent -mt-2">
                Triết học nhỏ
            </h2>
        </div>
        <main class="bg-poster-bg shadow-2xl">
            <div class="divide-y divide-gray-300">
                {list_items_html}
                 <div class="p-6 md:p-8">
                     <div class="flex justify-between items-center">
                        <div>
                            <p class="font-sans text-xs font-bold tracking-[0.2em] uppercase mb-2 text-gray-400">Sắp ra mắt</p>
                            <h3 class="font-serif text-3xl font-bold text-gray-400">Chủ đề mới...</h3>
                        </div>
                    </div>
                </div>
            </div>
        </main>
        <footer class="text-center mt-12">
            <a href="index.html" class="text-gray-500 hover:text-gray-400 transition text-sm">← Quay lại trang chủ</a>
        </footer>
    </div>
</body>
</html>"""

def main():
    """Main function to find posters, build, and write the list file."""
    print("Bắt đầu quét các file poster...")
    all_html_files = glob.glob("*.html")
    
    posters = []
    for file_path in all_html_files:
        if file_path in IGNORED_FILES:
            continue
        
        info = extract_poster_info(file_path)
        if info:
            posters.append(info)

    if not posters:
        print("Không tìm thấy poster nào được đánh dấu. Trang danh sách sẽ trống.")
    
    # Sort posters by number
    posters.sort(key=lambda p: p['number'])
    
    print(f"Đã tìm thấy {len(posters)} poster. Đang tạo trang danh sách...")

    # Build the HTML for all list items
    list_items_html = "\n".join([build_list_item_html(p) for p in posters])
    
    # Build the final page
    final_html = build_html_structure(list_items_html)
    
    # Write the file
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"\n✅ Thành công! Đã cập nhật file '{OUTPUT_FILE}'.")
        print("   Hãy mở file đó trên trình duyệt để xem kết quả.")
    except Exception as e:
        print(f"\nLỗi khi ghi file '{OUTPUT_FILE}': {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
