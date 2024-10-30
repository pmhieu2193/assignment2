## Thông tin 
Ngôn ngữ test: python ver 3.8

Website kiểm thử: https://ecommerce.tealiumdemo.com/

Môi trường (IDE): PyCharm

Driver: Chrome, Edge

lib: pytest, requests, selenium

## Installation
Cài đặt driver: driver sẽ tự động được cài đặt sau khi cài các gói thư viện sau.
```bash
pip install selenium
pip install requests
pip install pytest
```
Nếu cài đặt không thành công, hãy làm theo hướng dẫn tại [link](https://knowledge-curiositysoftware-ie.translate.goog/docs/how-to-install-chromedriver-for-web-ui-testing?_x_tr_sl=en&_x_tr_tl=vi&_x_tr_hl=vi&_x_tr_pto=tc) này.

## Thay đổi Driver
Các test case đã được kiểm tra và chạy trên 2 trình duyệt là Chrome và Edge. Để chuyển đổi trình duyệt, hãy sửa biến driver trên hàm driver() ứng với trình duyệt muốn tiến hành kiểm thử:

#cho trình duyệt chrome
driver = webdriver.Chrome()

#cho trình duyệt Edge
driver = webdriver.Edge()

## Chú ý
Các test case đã được thiết kế để không gây ra tình trạng xung đột khi chạy không có thứ tự (vd: muốn kiểm thử test case thanh toán nhưng các sản phẩm trong giỏ hàng đã bị test case xoá sản phẩm xoá sạch dẫn đến lỗi...). Có thể kiểm thử các test case trong bài mà không cần quan tâm module hay thứ tự.

File kiểm thử test_hieu.py, gồm 10 chức năng chính và 15 test case (13 PASS/ 2 FAILDED).

Bên dưới là thông tin cơ bản từng test case ứng với chức năng và ý tưởng thiết kế.

## Chi tiết các Test Case ứng với Chức năng
1. Login/Logout.

TC1 : Kiểm tra đăng nhập thành công.

def test_valid_login(driver):

Tiền điều kiện: Thông tin đăng nhập đã được đăng kí trước đó.

Ý tưởng: Cho hệ thống chờ vài giây sau khi đăng nhập thành công, sau đó kiểm tra đường dẫn hiện tại so sánh với trang trủ.

TC2 : Kiểm tra đăng nhập với email và password không đúng.

def test_invalid_login(driver):

Ý tưởng:  Cho hệ thống chờ vài giây sau khi đăng nhập, sau đó kiểm tra văn bản bên trong thông báo lỗi.

TC3: Kiểm tra Đăng xuất.

def test_log_out(driver):

Tiền điều kiện: Đã đăng nhập.

Ý tưởng: Kiểm tra đường dẫn trang hiện tại sau khi đăng xuất.

2. Search.

TC4: Kiểm tra tìm kiếm với từ khoá tìm kiếm hợp lệ.

def test_valid_search(driver):

Ý tưởng: Sau khi tìm kiếm thành công, hệ thống sẽ trả về 1 thẻ chứa danh sách các kết quả trả về. Kiểm tra thẻ đó có tồn tại hay không.

TC5: Kiểm tra tìm kiếm với từ khoá tìm kiếm không hợp lệ.

def test_valid_search(driver):

Ý tưởng: Sau khi tìm kiếm thất bại, hệ thống sẽ trả về 1 thẻ chứa thông báo "Không có kết quả tìm kiếm". Kiểm tra nội dung thẻ chứa thông báo.

3. Add to Cart.

def test_add_to_cart(driver):

TC6: Kiểm tra thêm sản phẩm vào giỏ hàng.

Ý tưởng: Sau khi thêm sản phẩm vào giỏ hàng thành công, hệ thống hiển thị thông báo văn bản, kiểm tra nội dung thông báo.

4. Cart.

TC7: Kiểm tra truy cập vào giỏ hàng trống.

def test_cart_empty(driver):

Ý tưởng: Khi click vào biểu tượng giỏ hàng khi giỏ hàng trống, hệ thống sẽ gửi thông báo "Giỏ hàng trống", kiểm tra thông báo.

TC8: Kiểm tra truy cập vào giỏ hàng có sẵn sản phẩm.

def test_cart_not_empty(driver):
(truy cập cart bằng biểu tượng.)

Tiền điều kiện: Đăng nhập thành công, giỏ hàng có sẵn sản phẩm.

Ý tưởng: Khi truy cập vào 1 giỏ hành có sẵn sản phẩm, hệ thống sẽ đưa đến trang giỏ hàng, kiểm tra đường dẫn này.

TC9: Kiểm tra xoá tất cả sản phẩm trong giỏ hàng.
def test_remove_all_cart(driver):

(truy cập cart bằng cách thêm sản phẩm.)

Tiền điều kiện: Thực hiện thêm sản phẩm.

Ý tưởng: Sau khi xoá tất cả sản phẩm, kiểm tra thông báo "SHOPPING CART IS EMPTY".

5. Check out. 

TC10: Kiểm tra checkout.

def test_check_out(driver):

tiền điều kiện: Giỏ hàng có sẵn sản phẩm.

Ý tưởng: Sau khi check out thành công, hệ thống hiển thị trang check out để người dùng điền thông tin đơn hàng. Kiểm tra đường dẫn trang này.

6. Change Langue.

TC11: Kiểm tra thay đổi ngôn ngữ.

def test_change_langue(driver):

Ý tưởng: Sau khi thay đổi ngôn ngữ, lấy 1 vùng văn bản động xem nội dung có thay đổi không (ở test case này sử dụng place holder trong ô tìm kiếm), nếu nội không thay đổi tức Fails.

7. Test Link.

TC12: Kiểm tra tính khả dụng tất cả các đường dẫn trên trang.

def test_link(driver):

Ý tưởng: Lấy danh sách tất cả các đường dẫn trên trang, kiểm tra mã phản hồi của từng đường dẫn này. Tạo 1 list, Với mỗi dường dẫn hỏng thêm đường dẫn vào list. Nếu list trên rỗng sau khi kiểm tra hết các đường dẫn, Pass.

8. Test Nav.

TC13: Kiểm tra hiển thị các trang điều hướng.

def test_nav(driver):

Ý tưởng: Lấy tất cả thẻ chứa nội dung là href trang điều hướng (naviagtion, footer,...). Tạo 1 list, mở tất cả các trang này và kiểm tra xem phần header page (Phần đầu trang) có hiển thị hay không. Nếu có trang không mở được thì lưu vào list, list trống trả về Pass.

9. Test Reponsive Layout.

TC14: Kiểm tra ứng dụng thích ứng với các kích thước màn hình khác nhau.

def test_adapt_to_different_screen_sizes(driver):

Ý tưởng: Trang được tính là hiển thị đầy đủ khi hiển thị header page (Phần đầu trang), kiểm tra hiển thị lần lượt các kích thước và lưu các kích thước không hiển thị được vào 1 list. List trống trả về Pass.

10. Wish List.

TC15: Kiểm tra truy cập trang wish list.

def test_access_to_wishlist(driver):

Ý tưởng: Sau khi truy cập wish list, hệ thống sẽ trả về trang này. Kiểm tra đường dẫn.

## FAILD  1
Thông báo của các test case failded trên IDE:

Lỗi TC_11: Nội dung website sau khi thay đổi ngôn ngữ không thay đổi
ID: E1

assert placeholder_text != "Search entire store here..."
E       AssertionError: assert 'Search entire store here...' != 'Search entire store here...'


## FAILD  2
Lỗi TC_12: Những link không phản hồi

ID: E2

assert not list_link, print(list_link)
E       AssertionError: None
E       assert not ['https://ecommerce.tealiumdemo.com/contacts/', 'https://ecommerce.tealiumdemo.com/sale/accessories.html', 'https://ecommerce.tealiumdemo.com/home-decor/decorative-accents.html', 'https://ecommerce.tealiumdemo.com/checkout/cart/', 'https://ecommerce.tealiumdemo.com/women/dresses-skirts.html', 'https://ecommerce.tealiumdemo.com/accessories/jewelry.html', ...]
AssertionError

Bên trên là danh sách những link không phản hồi.

