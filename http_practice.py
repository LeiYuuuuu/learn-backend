import json                  # 标准库：在 JSON 文本和 Python 的 dict/list 之间转换
import urllib.request        # 标准库：发 HTTP 请求，不用 pip 安装任何东西
import urllib.error          # 标准库：里面有 HTTPError，服务器返回 4xx/5xx 时会抛出它

def get(url):                                    # 封装一个函数：对 url 发 GET 请求并打印结果
    try:
        with urllib.request.urlopen(url) as r:   # 发出请求；r 是响应对象，with 结束后自动关闭连接
            print(url)                           # 打印请求的地址，方便对照输出
            print("  状态码:", r.status)          # r.status 就是 HTTP 状态码，成功时是 200
            return json.loads(r.read())          # r.read() 读出响应体（字节），json.loads 把它转成 dict 或 list
    except urllib.error.HTTPError as e:          # 4xx/5xx 会走到这里，而不是正常返回
        print(url)
        print("  状态码:", e.code)                # e.code 是出错时的状态码，比如 404
        return None                              # 失败时返回 None，调用方据此判断

# 1. 路径参数：查一个具体的用户
user = get("https://api.github.com/users/LeiYuuuuu")   # 返回一个 JSON 对象，即 Python dict
if user:                                                # dict 非空时为真
    print("  用户名:", user["login"], "公开仓库数:", user["public_repos"])  # 用键取值，和 dict 用法一样

# 2. 查询参数：只要 3 个仓库
repos = get("https://api.github.com/users/LeiYuuuuu/repos?per_page=3")  # 返回 JSON 数组，即 Python list
if repos:
    for repo in repos:                       # 数组里每一项都是一个 dict
        print("  仓库:", repo["name"])        # 只打印仓库名

# 3. 故意请求一个不存在的资源
get("https://api.github.com/users/no-such-user-zzz999")    # 预期输出 404