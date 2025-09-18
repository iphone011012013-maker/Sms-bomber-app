document.getElementById('smsForm').addEventListener('submit', function(event) {
    event.preventDefault(); // منع إرسال الفورم بالطريقة التقليدية

    const phone = document.getElementById('phone').value;
    const count = document.getElementById('count').value;
    const statusDiv = document.getElementById('status');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');

    // التحقق من صحة الرقم
    if (!phone.startsWith('01') || phone.length !== 11) {
        statusDiv.textContent = '❌ الرقم غير صحيح. يجب أن يبدأ بـ 01 ويكون 11 رقمًا.';
        statusDiv.style.color = '#ff7b7b';
        return;
    }

    // رابط الدالة السحابية (الخاص بمشروعك)
    const apiUrl = '/api/send';
    // تجهيز الواجهة للبدء
    statusDiv.textContent = '⏳ جاري الإرسال... برجاء الانتظار.';
    statusDiv.style.color = '#e0e0e0';
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    loader.style.display = 'block';

    // إرسال الطلب إلى الخادم
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            number: phone,
            sms_count: parseInt(count)
        }),
    })
    .then(response => response.json())
    .then(data => {
        // عرض النتيجة
        statusDiv.textContent = `✅ ${data.message}`;
        statusDiv.style.color = '#75f9a1';
    })
    .catch(error => {
        console.error('Error:', error);
        statusDiv.textContent = '❌ حدث خطأ أثناء الاتصال بالخادم.';
        statusDiv.style.color = '#ff7b7b';
    })
    .finally(() => {
        // إعادة الواجهة لوضعها الطبيعي
        submitBtn.disabled = false;
        btnText.style.display = 'block';
        loader.style.display = 'none';
    });
});
