import urllib
import re

from django.shortcuts import render

import requests

from oembed.forms import URLForm

access_token = "1233543173748276|910614243ff1caaf7f37b4a7f5f1981d"


def get_json(url):
    """
    example url = https://www.youtube.com/watch?v=dBD54EZIrZo

    url 을 받아서 도메인 추출 https://www.youtube.com/
    json file 에서 해당 도메인 이름있는 컬럼 확인
    해당 칼럼의 schema 에 url 이 매칭되는 지 확인
    url_name 추출
    `{url_name}+format=json&url=url` 으로 request 요청, 리턴 값 받아와서 전달함.
    """

    domain = extract_domain(url)
    if "www" in domain:
        domain = domain.replace("www.", "")
    domain_name = domain.split('.')[0]

    json_url = "https://oembed.com/providers.json"
    json_data = requests.get(json_url).json()

    for item in json_data:

        for endpoint in item["endpoints"]:

            if "schemes" not in endpoint:
                continue
            for scheme in endpoint['schemes']:
                scheme = scheme.replace('?', '\?')

                pattern = scheme.replace('*', r'[^\*&]+?')
                # print(pattern)
                if re.findall(pattern, url):
                    base_url = endpoint['url']

                    # only instagram
                    if domain_name == "instagram":
                        return requests.get("https://graph.facebook.com/v10.0/instagram_oembed?"
                                            "format=json&maxwidth=640&maxheight=480&url={}&access_token={}"
                                            .format(url, access_token)).json()

                    if ".{format}" in base_url:
                        base = base_url.replace("{format}", "json")
                        endpoint = base + "?maxwidth=640&maxheight=480&url=" + url
                    else:
                        endpoint = base_url + "?format=json&maxwidth=640&maxheight=480&url=" + url

                    return requests.get(endpoint).json()
    else:
        return {"error": "해당 url 은 oEmbed 에 등록되어있지 않습니다."}


def extract_domain(url):
    url = urllib.parse.urlparse(url).netloc
    return url


def post_renderer(request):
    # context = dict()
    # context['form'] = URLForm
    form = URLForm
    if request.method == 'POST':
        request_url = request.POST.get("url")
        data = get_json(request_url)
        print(data)
        return render(request, 'post/home.html', {'form': form, 'data': data})

    return render(request, 'post/home.html', {'form': form})
