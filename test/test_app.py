def test_index():
    assert True  # Thay thế bằng các kiểm tra thực tế cho ứng dụng của bạn

def test_devices_route(client):
    response = client.get('/devices')
    assert response.status_code == 200