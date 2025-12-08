# create_poster.py
import os
import sys

# --- Installation check for dependencies ---
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Lỗi: Thư viện 'beautifulsoup4' chưa được cài đặt.", file=sys.stderr)
    print("Vui lòng chạy lệnh sau trong terminal của bạn:", file=sys.stderr)
    print("pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

TEMPLATE_FILE = 'chudiemnho.html'

def get_multiline_input(prompt):
    """Gets multiline input from the user."""
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError: # Handles Ctrl+D/Ctrl+Z+Enter in some terminals
            break
    return "\n".join(lines)

def create_poster():
    """
    Creates a new poster HTML file based on a template, with custom content.
    """
    print("--- Công cụ tạo Poster Triết học ---")
    print("Vui lòng cung cấp thông tin cho poster mới.")

    # 1. Check for template file
    if not os.path.exists(TEMPLATE_FILE):
        print(f"\nLỗi: Không tìm thấy file mẫu '{TEMPLATE_FILE}'.", file=sys.stderr)
        print("Vui lòng đảm bảo file đó tồn tại trong cùng thư mục với script này.", file=sys.stderr)
        return

    # 2. Get user input
    new_quote = get_multiline_input("\n▶︎ Nhập câu quote (để xuống dòng, nhấn Enter. Nhấn Enter lần nữa trên dòng trống để kết thúc):")
    new_author = input("▶︎ Nhập tên tác giả/nguồn (ví dụ: 'Plato'): ")
    new_number = input("▶︎ Nhập số thứ tự poster (ví dụ: 'Số 02'): ")
    output_filename = input("▶︎ Nhập tên file output (ví dụ: 'poster_plato.html'): ")

    if not output_filename:
        print("\nLỗi: Tên file output không được để trống.", file=sys.stderr)
        return
        
    if not output_filename.endswith('.html'):
        output_filename += '.html'

    # 3. Read and parse the template
    print("\nĐang xử lý...")
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"Lỗi khi đọc file mẫu: {e}", file=sys.stderr)
        return

    # 4. Find and update the quote
    quote_element = soup.find('p', id='quote')
    if quote_element:
        new_quote_stripped = new_quote.strip()
        if new_quote_stripped:
            first_letter = new_quote_stripped[0]
            rest_of_quote = new_quote_stripped[1:]

            span_tag = soup.new_tag('span', **{'class': 'font-sans font-black text-6xl float-left mr-4 mt-[-12px] text-poster-accent leading-none'})
            span_tag.string = first_letter

            quote_element.clear()
            quote_element.append(span_tag)
            
            # Replace newlines with <br> and parse as HTML
            rest_of_quote_html = rest_of_quote.replace('\n', '<br/>')
            
            # Append the rest of the quote. We need to parse it to handle the <br/> tags.
            # We iterate over a copy of the contents list `list(...)` because appending an
            # element moves it from the source soup, which can corrupt the iteration.
            for element in list(BeautifulSoup(f"<div>{rest_of_quote_html}</div>", 'html.parser').div.contents):
                 quote_element.append(element)

        else:
            quote_element.clear()
            quote_element.string = "Chưa có trích dẫn."
    else:
        print("Cảnh báo: Không tìm thấy element với id='quote' trong file mẫu.", file=sys.stderr)

    # 5. Find and update the author
    author_selector = 'div.mt-8 > p.text-poster-accent'
    author_element = soup.select_one(author_selector)
    if author_element:
        author_element.string = new_author
    else:
        print("Cảnh báo: Không tìm thấy element tác giả trong file mẫu.", file=sys.stderr)

    # 6. Change the poster number
    # <p class="font-sans text-xs font-bold tracking-[0.2em] uppercase mb-1">Số 01</p>
    poster_number_element = soup.select_one('header div.text-right > p.font-sans')
    if poster_number_element:
        poster_number_element.string = new_number
    else:
        print("Cảnh báo: Không tìm thấy element số thứ tự poster.", file=sys.stderr)


    # 7. Write the new HTML file
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Prepend doctype and use prettify with an HTML5 formatter
            # to preserve formatting and structure similar to the original.
            f.write("<!DOCTYPE html>\n")
            f.write(soup.prettify(formatter='html5'))
        print(f"\n✅ Thành công! Đã tạo file '{output_filename}'.")
        print("   Bạn có thể mở file này bằng trình duyệt để xem kết quả.")
    except Exception as e:
        print(f"Lỗi khi ghi file output: {e}", file=sys.stderr)


if __name__ == '__main__':
    create_poster()
