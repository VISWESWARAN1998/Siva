# SWAMI KARUPPASWAMI THUNNAI

class FirewallSymptom:
    cloudflare_symptom ={
        "title" : "Direct IP access not allowed | Cloudflare",
        "status_code": 403,
        "soup_text": ["Cloudflare", "Ray ID:"]
    }
    cloudfront_symptom = {
        "title": "ERROR: The request could not be satisfied",
        "status_code": 403,
        "soup_text": ["cloudfront", "Request ID:"]
    }