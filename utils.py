import requests
import urllib3
import urllib

def get_json(url):
    """
    example url = https://www.youtube.com/watch?v=dBD54EZIrZo

    url 을 받아서 도메인 추출 https://www.youtube.com/
    json file 에서 해당 도메인 이름있는 컬럼 확인
    해당 칼럼의 schema 에 url 이 매칭되는 지 확인
    url_name 추출
    `{url_name}+format=json&url=url` 으로 request 요청, 리턴 값 받아와서 전달함.
    """
    json_url = "https://oembed.com/providers.json"

    data = requests.get(json_url).json()
    domain = extract_domain(url)
    for i in data:
        # print(i["provider_name"])
        if i["provider_name"].lower() == domain:
            base = i["endpoints"][0]["url"]
            endpoint = base + "/?format=json&url=" + url
            return requests.get(endpoint).json()
    else:
        return {"error": "해당 url 은 oEmbed 에 등록된 Provider 가 아닙니다."}


def extract_domain(url):
    return url.split('/')[2].split('.')[1]


# 인스타 api :https://api.instagram.com/oembed/
# facebook 에서 oembed 를 사용하는 게 이제 안되나?


# print(get_endpoint("https://www.instagram.com/p/BUawPlPF_Rx/"))
print(requests.get("https://graph.facebook.com/v10.0/instagram_oembed?format=json&url=https://www.instagram.com/p/BUawPlPF_Rx/&access_token=1233543173748276|910614243ff1caaf7f37b4a7f5f1981d").json())
# token 910614243ff1caaf7f37b4a7f5f1981d
# id 1233543173748276

# print(urllib3.parse_url("https://www.instagram.com/p/BUawPlPF_Rx/"))

# print(urllib.parse.urlparse("https://www.instagram.com/p/BUawPlPF_Rx/").netloc)


"""
            if "schemes" not in endpoint:
                continue
            for scheme in endpoint['schemes']:
                scheme = scheme.replace('?', '\?')

                pattern = scheme.replace('*', r'[^\*&]+?')
                
                if re.findall(pattern, url):
                    base_url = endpoint['url']
                    if ".{format}" in base_url:
                        base = base_url.replace("{format}", "json")
                        endpoint = base + "?url=" + url
                    else:
                        endpoint = base_url + "?format=json&url=" + url
                    print(endpoint)
                    return requests.get(endpoint).json()
        # if domain_name in item["provider_name"].lower(): # domain name 이 정확히 일치하지 않는 경우도 있음
            
        else:
            return {"error": "해당 url 은 oEmbed 에 등록된 Provider 가 아닙니다."}
"""