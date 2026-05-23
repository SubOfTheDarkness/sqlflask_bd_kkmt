from app import create_app
from waitress import serve

app = create_app()

if __name__ == '__main__':
    print("🚀 Сервер запущен: http://127.0.0.1:5000")
    
    # Для разработки используй встроенный сервер Flask
    # Для продакшена закомментируй строку ниже и раскомментируй waitress
    # app.run(debug=True, host='127.0.0.1', port=5000)
    
    # Продакшен-сервер (раскомментируй когда будешь готов):
    serve(app, host='127.0.0.1', port=5000)