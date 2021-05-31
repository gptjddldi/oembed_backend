import urllib
import re

from django.shortcuts import render

import requests

from oembed.forms import URLForm

access_token = "1233543173748276|910614243ff1caaf7f37b4a7f5f1981d"


def get_json(url):
    """
.
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

                pattern = scheme.replace('*', r'[^\*&]+?')  # 패턴 매칭
                # print(pattern)
                if re.findall(pattern, url):  # url 이 매칭되는 패턴이 있다면
                    base_url = endpoint['url']

                    # only instagram (token 인증 해야함)
                    if domain_name == "instagram":
                        return requests.get("https://graph.facebook.com/v10.0/instagram_oembed?"
                                            "format=json&url={}&access_token={}".format(url, access_token)).json()

                    if ".{format}" in base_url:  # vimeo
                        base = base_url.replace("{format}", "json")
                        endpoint = base + "?url=" + url

                    else:
                        endpoint = base_url + "?format=json&url=" + url

                    return requests.get(endpoint).json()
    else:
        return {"error": "해당 url 은 oEmbed 에 등록되어있지 않습니다."}


def extract_domain(url):
    """
    도메인 주소 추출
    """
    url = urllib.parse.urlparse(url).netloc
    return url


def post_renderer(request):
    form = URLForm
    if request.method == 'POST':
        request_url = request.POST.get("url")
        data = get_json(request_url)
        return render(request, 'post/home.html', {'form': form, 'data': data})

    return render(request, 'post/home.html', {'form': form})
