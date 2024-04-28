import psycopg2
import re
import os
import requests
from bs4 import BeautifulSoup
from psycopg2 import sql
from unidecode import unidecode
from datetime import datetime
from PIL import Image
from io import BytesIO

def init():
    #Link các mục bài báo
    urls = [
            "https://vnexpress.net/the-thao",
            "https://vnexpress.net/kinh-doanh",
            "https://vnexpress.net/thoi-su/chinh-tri",
            "https://vnexpress.net/khoa-hoc",
            "https://vnexpress.net/the-gioi",
            "https://vnexpress.net/giao-duc",
            "https://vnexpress.net/giai-tri",
            "https://vnexpress.net/suc-khoe",
            ]
    #categoryId tương ứng với các mục bài báo
    categoryIds = [
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                   ]
    combined_dict = dict(zip(categoryIds, urls))
    # Thư mục để lưu trữ hình ảnh
    image_folder = "/Users/ThanhNV177/Project/PycharmProjects/XuanThuNews/static/news/images/article"

    # Kết nối đến PostgreSQL
    conn = psycopg2.connect(
        dbname="xuanthudb",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5433"
    )
    numArticles = 20
    return combined_dict, image_folder, conn, numArticles
def convert_to_formatted_time(date_str):
    # Tách chuỗi theo dấu phẩy
    date_parts = date_str.split(", ")
    try:
        # Ghép lại các phần tử cần thiết
        formatted_date_str = f"{date_parts[1]} {date_parts[2].replace(' (GMT+7)', '')}"
        # Chuyển đổi thành đối tượng datetime
        date_obj = datetime.strptime(formatted_date_str, "%d/%m/%Y %H:%M")

        # Định dạng lại ngày thành chuỗi theo định dạng mong muốn
        formatted_time = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time
    except Exception as e:
        return ""

def get_article_content(url):
    # Gửi yêu cầu HTTP để lấy nội dung trang web
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Bỏ nội dung trong thẻ span có class location-stamp
        for span_tag in soup.find_all("span", class_="location-stamp"):
            span_tag.decompose()
        # Lấy tiêu đề
        title_tag = soup.find('h1', class_='title-detail')
        title = title_tag.text.strip() if title_tag else "No Title"
        # Lấy date
        date_tag = soup.find('span', class_='date')
        date = date_tag.text.strip() if title_tag else "No Date"
        published_date = convert_to_formatted_time(date)
        # Lấy mô tả
        description_tag = soup.find('p', class_='description')
        description = description_tag.text.strip() if description_tag else "No Description"

        # Lấy danh sách tất cả các thẻ <p> trong nội dung bài báo
        p_tags = soup.find_all('p', class_='Normal')

        # Cộng nội dung của từng thẻ <p> lại với nhau, mỗi thẻ có xuống hàng
        content = ""
        for p_tag in p_tags:
            if p_tag:
                content += "<p>" + p_tag.text.strip()+ "</p>"

        html_content = "<p>"+ description+ "</p>" + content
        html_content.replace("VnExpress","báo Xuân Thu")

        # Lấy đường link hình ảnh
        image_url = None
        # Lấy nội dung bài báo
        article_content = soup.find('article', class_='fck_detail')
        if article_content:
            image_tag = article_content.find('img')
            if image_tag:
                image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None

        return title, html_content, image_url,published_date
    else:
        print(f"Failed to fetch content. Status code: {response.status_code}")
    return None

def download_image(image_folder, image_url, article_title, target_size_kb=80):
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(image_folder, exist_ok=True)
    if image_url:
        # Tạo đường dẫn đầy đủ cho hình ảnh
        full_image_path = os.path.join(image_folder, f"{article_title}.webp")

        # Tải hình ảnh
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))

            # Lấy tỉ lệ giảm kích thước để đạt được dung lượng mong muốn
            target_size_bytes = target_size_kb * 1024
            current_size_bytes = len(response.content)
            if current_size_bytes > target_size_bytes:
                # Resize ảnh
                new_width = 800
                new_height = int((image.height / image.width) * new_width)
                resized_image = image.resize((new_width, new_height))
            else:
                resized_image = image

            # Chuyển đổi và lưu lại ảnh đã được resize dưới định dạng WebP
            resized_image.save(full_image_path, 'WEBP', quality=85)

def slugify(name):
    # Chuyển đổi chuỗi thành chữ thường và loại bỏ dấu
    name = unidecode(name.lower())

    # Loại bỏ các ký tự không phải chữ cái hoặc số và thay thế khoảng trắng bằng dấu gạch ngang
    slug = re.sub(r'[^\w\s-]', '', name)

    # Loại bỏ các dấu gạch ngang liên tiếp và dấu gạch ngang ở đầu và cuối chuỗi
    slug = '-'.join(filter(None, slug.split('-')))
    # Thay thế khoảng trắng bằng dấu gạch ngang
    slug = slug.replace(' ', '-')
    return slug

def getArtcalDataInfors(url,categoryId,image_folder,numArticles):
    # Lấy danh sách các bài báo
    article_links = []
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    articles = soup.select("p.description a")
    for article in articles:
        if 'box_comment_vne' not in article["href"]:
            article_links.append(article["href"] )

    # Tạo insert data
    insertData = []

    i = 1
    for article_url in article_links[:numArticles]:
        try:
            title, content, image_url, public_date = get_article_content(article_url)
            if image_url is None or content == 'No Content':
                print(f'title:{title} imageUrl:{image_url} link:{article_url}')
                continue
            slug = slugify(title)
            if i == 1 and categoryId in (3,5,7,8,9):
                special = True
            else:
                special = False
            # public_date = get_current_time()
            image = "news/images/article/" + slug + ".webp"
            status = "published"
            ordering = i
            i += 1
            # Dữ liệu mẫu, bạn có thể thay đổi tùy theo nhu cầu
            articleInfor = (title, slug, special, public_date, content, image, categoryId, status, ordering)
            insertData.append(articleInfor)

            # Tải hình ảnh và lưu vào thư mục images
            download_image(image_folder, image_url, slug)
        except Exception as e:
            print(f'title:{title} imageUrl:{image_url} link:{article_url}')
            continue
    # Hàm sắp xếp insertData theo trường public_date giảm dần
    return sorted(insertData, key=lambda x: x[3], reverse=True)

def UpdateArticleDataInfos(conn,insertData):

    # Tạo một đối tượng cursor để thực hiện các truy vấn SQL
    cur = conn.cursor()

    try:
        # Sử dụng câu truy vấn INSERT ... ON CONFLICT để kiểm tra trùng lặp trên cột 'name' và 'slug'
        insert_query = sql.SQL("""
            INSERT INTO public.news_article ("name", slug, special, publish_date, content, image, category_id, status, ordering)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name, slug) DO NOTHING
        """)

        # Insert Article Datas
        cur.executemany(insert_query, insertData)

        # Update special với bài báo mới nhất của mỗi category
        update_query = sql.SQL("""
                    UPDATE news_article
                    SET special = CASE WHEN news_article.publish_date = max_dates.max_publish_date THEN True ELSE False END
                    FROM (
                        SELECT category_id, MAX(publish_date) AS max_publish_date
                        FROM news_article
                        GROUP BY category_id
                    ) AS max_dates
                    WHERE news_article.category_id = max_dates.category_id
                """)

        # Thực hiện truy vấn UPDATE
        cur.execute(update_query)
        conn.commit()

    finally:
        # Đóng kết nối
        cur.close()
        conn.close()

if __name__ == "__main__":

    combined_dict, image_folder,conn, numArticles = init()
    insertData = []
    for categoryId, url in combined_dict.items():
        insertData.extend(getArtcalDataInfors(url,categoryId,image_folder,numArticles))
    if len(insertData) > 0:
        UpdateArticleDataInfos(conn,insertData)
