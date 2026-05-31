import requests

def fetch_frontend_code(target_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 KHTML, like Gecko Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        response.encoding = 'utf-8'
        
        print("网页前端源代码抓取成功：\n")
        print(response.text)
        
    except requests.exceptions.RequestException as error:
        print(f"网络通信握手失败或发生异常：{error}")

if __name__ == "__main__":
    target_website = "https://www.hzau.edu.cn/"
    fetch_frontend_code(target_website)

# Create your tests here.
