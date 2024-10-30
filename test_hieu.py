import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

#Driver
@pytest.fixture
def driver():
    #Chrome driver
    driver = webdriver.Chrome()
    #Edge driver
    #driver = webdriver.Edge()
    driver.maximize_window()
    yield driver
    driver.quit()

##########################################LOGIN/LOG_OUT###############################################

#TC1: Kiểm tra đăng nhập thành công.
# passed in 23.44s
def test_valid_login(driver):
    #Truy cập trang và gửi thông tin đăng nhập
    driver.get("https://ecommerce.tealiumdemo.com/customer/account/login/")
    driver.find_element(By.ID, "email").send_keys("hieu@gmail.com")
    driver.find_element(By.ID, "pass").send_keys("12345678")
    button = driver.find_element(By.ID, "send2")
    #Vì thiết kế của nút login nằm bên dưới màn hình nên phải cuộn màn hình xuống để tìm kiếm nút
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(5)
    #Lấy đường dẫn hiện tai
    current_url = driver.current_url
    # Kiểm tra URL hiện tại
    assert current_url == "https://ecommerce.tealiumdemo.com/customer/account/", f"Expected URL: 'https://ecommerce.tealiumdemo.com/customer/account/', but got: '{current_url}'"

#TC2: Kiểm tra đăng nhập với email và password không đúng.
#Passed in 18.28s
def test_invalid_login(driver):
    driver.get("https://ecommerce.tealiumdemo.com/customer/account/login/")
    #Thông tin đăng nhập sai
    driver.find_element(By.ID, "email").send_keys("hieu@gmail.com")
    driver.find_element(By.ID, "pass").send_keys("123456788999")
    button = driver.find_element(By.ID, "send2")
    #Vì thiết kế của nút login nằm bên dưới màn hình nên phải cuộn màn hình xuống để tìm kiếm nút
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    #Chờ cho đến khi thẻ li có class error-msg chứa thông báo xuất hiện
    li_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "li.error-msg"))
    )
    alert_text = ""
    # Tìm thẻ con đầu tiên có văn bản
    child_element = li_element.find_element(By.XPATH, ".//*[text()]")
    if child_element:
        alert_text =  child_element.text
    print(alert_text)
    #Pass nếu thông báo chính xác
    assert alert_text == "Invalid login or password."

#TC3: Kiểm tra Đăng xuất.
#passed in 30.00s
def test_log_out(driver):
    #Đăng nhập
    driver.get("https://ecommerce.tealiumdemo.com/customer/account/login/")
    driver.find_element(By.ID, "email").send_keys("hieu@gmail.com")
    driver.find_element(By.ID, "pass").send_keys("12345678")
    button = driver.find_element(By.ID, "send2")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(3)
    #Tìm đến vị trí nút User và click
    driver.find_element(By.CSS_SELECTOR, "a.skip-link.skip-account").click()
    #Vì nút Logout nằm trong danh sách các chức năng của User nên phải chờ cho thẻ logout xuất hiện
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@class=' last']/a"))
    )
    logout_link.click()
    #Đợi 10s vì website tốn 1 khoảng thời gian để tải trang chuyển hướng
    time.sleep(10)
    current_url = driver.current_url
    # Kiểm tra URL hiện tại
    assert current_url == "https://ecommerce.tealiumdemo.com/", f"Expected URL: 'https://ecommerce.tealiumdemo.com/', but got: '{current_url}'"

#########################################SEARCH########################################

#TC4: Kiểm tra tìm kiếm với từ khoá tìm kiếm hợp lệ.
#passed in 21.16s
def test_valid_search(driver):
    driver.get("https://ecommerce.tealiumdemo.com")
    #Nhập key tìm kiếm và nhấn nút
    driver.find_element(By.ID, "search").send_keys("Chelsea Tee")
    driver.find_element(By.CSS_SELECTOR, ".button.search-button").click()
    #Đợi tải trang kết quả tìm kiếm
    time.sleep(3)
    #Kiểm tra xem thẻ chứa danh sách kết quả trả về có tồn tại không
    element = driver.find_element(By.CLASS_NAME, "category-products")
    assert element is not None

#TC5: Kiểm tra tìm kiếm với từ khoá tìm kiếm không hợp lệ.
#passed in 17.31s
def test_invalid_search(driver):
    driver.get("https://ecommerce.tealiumdemo.com")
    #Nhập key tìm kiếm và nhấn nút
    driver.find_element(By.ID, "search").send_keys("zyzzz")
    driver.find_element(By.CSS_SELECTOR, ".button.search-button").click()
    p_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.note-msg"))
    )
    # Lấy nội dung văn bản thông báo trong thẻ <p>
    element = p_element.text
    assert element == "Your search returns no results."

##########################ADD TO CART###########################################

#TC6: Kiểm tra thêm sản phẩm vào giỏ hàng.
#passed in 18.10s
def test_add_to_cart(driver):
    #Vào trang chi tiết 1 sản phẩm tên là Blue Horizons Bracelets
    driver.get("https://ecommerce.tealiumdemo.com/blue-horizons-bracelets.html")
    #Nhấn thêm vào giỏ.
    buttons = driver.find_elements(By.CLASS_NAME, "btn-cart")
    buttons[1].click()
    #Chờ cho đến khi thẻ thông báo xuất hiện
    span_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//li[@class='success-msg']//span"))
    )
    # Lấy nội dung văn bản trong <span>
    mgs = span_element.text
    print(mgs)
    assert mgs =="Blue Horizons Bracelets was added to your shopping cart."

##################################CART###########################################

#TC7: Kiểm tra truy cập vào giỏ hàng trống.
#passed in 14.85s
def test_cart_empty(driver):
    driver.get("https://ecommerce.tealiumdemo.com")
    driver.find_element(By.CLASS_NAME, "skip-cart").click()
    empty_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.empty"))
    )
    mgs = empty_message.text
    print(mgs)
    assert mgs == "You have no items in your shopping cart."

#TC8: Kiểm tra truy cập vào giỏ hàng có sẵn sản phẩm.
#passed in 24.50s
def test_cart_not_empty(driver):
    #Đăng nhập tài khoản có sẵn sp trong giỏ (sản phẩm từ test case trên)
    driver.get("https://ecommerce.tealiumdemo.com/customer/account/login/")
    driver.find_element(By.ID, "email").send_keys("hieu@gmail.com")
    driver.find_element(By.ID, "pass").send_keys("12345678")
    button = driver.find_element(By.ID, "send2")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(5)
    #Chờ nút xem giỏ hàng xuất hiện và nhấn nút
    driver.find_element(By.CLASS_NAME, "skip-cart").click()
    a_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.cart-link"))
    )
    a_element.click()
    time.sleep(5)
    current_url = driver.current_url
    # Kiểm tra URL hiện tại
    assert current_url == "https://ecommerce.tealiumdemo.com/checkout/cart/"

#TC9: Kiểm tra xoá tất cả sản phẩm trong giỏ hàng.
#passed in 28.37s
def test_remove_all_cart(driver):
    #Thực hiện pre condition
    driver.get("https://ecommerce.tealiumdemo.com/blue-horizons-bracelets.html")
    buttons = driver.find_elements(By.CLASS_NAME, "btn-cart")
    buttons[1].click()
    time.sleep(3)
    # Nếu hàm lỗi hãy thêm hàm dưới để kéo xuống vị trí nút empty
    # driver.execute_script("arguments[0].scrollIntoView();", button)
    #Bấm nút empty
    btn_empty = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button2.btn-empty"))
    )
    btn_empty.click()
    h1_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='page-title']/h1"))
    )
    h1_text = h1_element.text
    print(f"current text: {h1_text}")
    # Kiểm tra URL hiện tại
    assert h1_text == "SHOPPING CART IS EMPTY"

############################CHECK OUT########################################

#TC10: Kiểm tra checkout.
#passed in 27.41s
def test_check_out(driver):
    # Thực hiện thêm sản phẩm vào giỏ
    driver.get("https://ecommerce.tealiumdemo.com/blue-horizons-bracelets.html")
    buttons = driver.find_elements(By.CLASS_NAME, "btn-cart")
    buttons[1].click()
    time.sleep(3)
    #Nhấn vào biểu tượng user
    driver.find_element(By.CLASS_NAME, "skip-cart").click()
    #Chờ nút check out xuất hiện
    a_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.checkout-button"))
    )
    a_element.click()
    time.sleep(5)
    current_url = driver.current_url
    assert current_url == "https://ecommerce.tealiumdemo.com/checkout/onepage/"

############################CHANGE LANGUAGE########################

#TC11: Kiểm tra thay đổi ngôn ngữ.
#failed in 12.96s
def test_change_langue(driver):
    driver.get("https://ecommerce.tealiumdemo.com")
    #Đợi select box đổi ngôn ngữ hiển thị
    select_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "select-language"))
    )
    # Tạo đối tượng Select
    select = Select(select_element)
    # Chọn giá trị thứ hai (Chọn ngôn ngữ thứ 2)
    select.select_by_index(1)
    input_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "search"))
    )
    # Lấy giá trị của thuộc tính placeholder
    placeholder_text = input_element.get_attribute("placeholder")
    print(f"current text: {placeholder_text}")
    assert placeholder_text != "Search entire store here..."

#########################TEST LINK#############################

#TC12: Kiểm tra tính khả dụng tất cả các đường dẫn trên trang.
#failed in 66.78s
#Tạo 1 list chứa các link hỏng, nếu list rỗng trả về pass.
def test_link(driver):
    home_page = "https://ecommerce.tealiumdemo.com"
    driver.get(home_page)
    # Tìm tất cả các thẻ <a>
    l = driver.find_elements(By.TAG_NAME, "a")
    # Sử dụng set để lưu các href khác nhau
    links = set(link.get_attribute("href") for link in l)
    list_link = []
    for link in links:
        # Không cần gọi get_attribute ở đây, vì link đã là chuỗi
        url = link
        print(f"Checking: {url}")
        # Kiểm tra nếu URL là None hoặc rỗng
        if url is None or url == "":
            print("URL is either not configured for anchor tag or it is empty")
            continue
        # Kiểm tra nếu URL không bắt đầu bằng home_page
        if not url.startswith(home_page):
            print(f"URL belongs to another domain, skipping it: {url}")
            continue
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code >= 400:
                print(f"code: {response.status_code}")
                print(f"{url} is a broken link")
                list_link.append(url)
            else:
                print(f"{url} is a valid link")
        except requests.exceptions.RequestException as e:
            print(f"Error checking {url}: {e}")
    assert not list_link, print(list_link)

###################################NAV####################################

#TC13: Kiểm tra hiển thị các trang điều hướng.
#passed in 87.07s
def test_nav(driver):
    # Mở trang web
    test_url = "https://ecommerce.tealiumdemo.com"
    driver.get(test_url)
    # Lấy tất cả các thẻ <a> có class "level1" (Tất cả các đường dẫn điều hướng như nav, footer ...)
    links = driver.find_elements(By.CSS_SELECTOR, "a.level1")
    # Lưu tất cả các href vào danh sách
    hrefs = set(link.get_attribute("href") for link in links)
    # In ra danh sách các href
    print("Danh sách các liên kết:")
    for href in hrefs:
        print(href)
    #Tạo đường dẫn chứa link không thể mở được (hay hiển thị không đầy đủ)
    list_link = []
    # Mở lần lượt từng trang từ các href
    for href in hrefs:
        driver.get(href)  # Mở liên kết
        # Chờ cho tiêu đề xuất hiện để đảm bảo trang đã tải xong
        try:
            header = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, "header"))  # Thay đổi theo phần tử tương ứng
            )
            print(f"Đã mở trang: {href}")
        except Exception as e:
            print(f"Lỗi khi mở trang: {href}, Lỗi: {str(e)}")
            list_link.append(href)
        finally:
            pass
    assert not list_link

############################REPONSIVE RESIZE############################

#TC14: Kiểm tra ứng dụng thích ứng với các kích thước màn hình khác nhau
#passed in 19.82s
#Tạo list chứa các kích thước mở không thành công, list rỗng trả về pass
def test_adapt_to_different_screen_sizes(driver):
    #Mở trang chủ
    test_url = "https://ecommerce.tealiumdemo.com"
    driver.get(test_url)
    # Danh sách các kích thước màn hình để kiểm tra
    screen_sizes = {
        "Desktop": (1280, 800),
        "Tablet": (768, 1024),
        "Mobile": (375, 667)
    }
    List = []
    for device, (width, height) in screen_sizes.items():
        #Thay đổi kích thước cửa sổ
        driver.set_window_size(width, height)
        # Kiểm tra các yếu tố trên trang
        try:
            # Chờ cho một phần tử cụ thể xuất hiện (header của page)
            header = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, "header"))
            )
            if not header.is_displayed():
                List.append(device)
        except Exception as e:
            List.append(device)
    assert not List, print(List)

##############################WISH LIST##########################################

#TC15: Kiểm tra truy cập trang wish list.
#passed in 31.94s
def test_access_to_wishlist(driver):
    #LOGIN
    driver.get("https://ecommerce.tealiumdemo.com/customer/account/login/")
    driver.find_element(By.ID, "email").send_keys("hieu@gmail.com")
    driver.find_element(By.ID, "pass").send_keys("12345678")
    button = driver.find_element(By.ID, "send2")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(3)
    #Truy cập logo user và chờ nút wish list xuất hiện
    driver.find_element(By.CSS_SELECTOR, "a.skip-link.skip-account").click()
    wishlist_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@title, 'My Wishlist')]"))
    )
    wishlist_link.click()
    time.sleep(10)
    current_url = driver.current_url
    # Kiểm tra URL hiện tại
    assert current_url == "https://ecommerce.tealiumdemo.com/wishlist/", f"Expected URL: 'https://ecommerce.tealiumdemo.com/wishlist/', but got: '{current_url}'"
