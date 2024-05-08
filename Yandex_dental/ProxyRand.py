import random

proxy_list = [
'5.254.34.4:3129',
'117.251.103.186:8080',
'27.79.12.81:22552',
'23.152.40.15:3128',
'8.209.114.72:3129'
'200.143.75.194:8080'
]



def return_proxy():
    return random.choice(proxy_list)

