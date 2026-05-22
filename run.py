from app import create_app

# استدعاء الـ Factory وبناء التطبيق
app = create_app()

if __name__ == '__main__':
    # تشغيل السيرفر بنفس الإعدادات بتاعتك
    app.run(host='0.0.0.0', port=5000, debug=False)