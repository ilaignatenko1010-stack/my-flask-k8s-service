# My Flask K8s Service

В ходе выполнения практического задания был разработан веб-сервис на фреймворке Flask, предоставляющий REST API. Сервис упакован в Docker-контейнер, загружен в публичный реестр Docker Hub, развернут в Яндекс Облаке (доступ через телефон) и в локальном кластере Kubernetes (Minikube). Все исходные коды и манифесты загружены в GitHub.

## 1. СОЗДАНИЕ РЕПОЗИТОРИЯ GITHUB

### Что сделано:

1. Создан публичный репозиторий с именем `my-flask-k8s-service`
2. Репозиторий инициализирован с `README.md` и `.gitignore` (Python)
3. Репозиторий склонирован на локальный компьютер

### Использованные команды:

```bash
git clone https://github.com/<username>/my-flask-k8s-service.git
cd my-flask-k8s-service
```

![](/media/1.png)
![](/media/2.png)

## 2. РАЗРАБОТКА СЕРВИСА FLASK

### Что сделано:

1. Создан файл `app.py` с кодом веб-сервиса
2. Реализованы три endpoint: `/`, `/health`, `/info`
3. Создан `requirements.txt` с зависимостью Flask
4. Файлы загружены в GitHub

### Содержимое `app.py`:

```python
from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "service": "Flask K8s Demo",
        "status": "running",
        "timestamp": datetime.datetime.now().isoformat(),
        "hostname": os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/info')
def info():
    return jsonify({
        "version": "1.0.0",
        "python_version": "3.9",
        "framework": "Flask"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

![](/media/3.png)
![](/media/4.png)

## 3. УПАКОВКА СЕРВИСА В DOCKER

### Что сделано:

- Создан `Dockerfile` для сборки образа
- Выполнена сборка Docker-образа: `docker build -t my-flask-service .`
- Запущен контейнер: `docker run -d -p 5000:5000 --name my-flask-container my-flask-service`
- Проверена работа через браузер `http://localhost:5000`

### Содержимое `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

![](/media/5.png)
![](/media/6.png)
![](/media/7.png)
![](/media/8.png)

## 4. ЗАГРУЗКА ОБРАЗА В DOCKER HUB

### Что сделано:

- Выполнен вход в Docker Hub: `docker login`
- Образ помечен тегом: `docker tag my-flask-service <username>/my-flask-service:latest`
- Образ загружен: `docker push <username>/my-flask-service:latest`
- Проверено наличие образа на сайте Docker Hub

![](/media/9.png)
![](/media/10.png)
![](/media/11.png)
![](/media/12.png)
![](/media/13.png)

## 5. РАЗВЁРТКА В ЯНДЕКС ОБЛАКЕ (через телефон)

### Что сделано:

1. Выполнена регистрация в Yandex Cloud
2. Создана виртуальная машина:
   - Имя: `my-flask-service`
   - Образ: Container Optimized Image
   - Диск: SSD 20 ГБ
   - Ресурсы: 2 vCPU, 2 GB RAM
   - Публичный IP: включен
3. В метаданные (user-data) добавлена конфигурация для запуска Docker-контейнера
4. ВМ запущена, получен публичный IP-адрес
5. С телефона открыт адрес `http://<IP>:5000`

### Конфигурация метаданных (user-data):

```yaml
#cloud-config
runcmd:
  - docker run -d -p 5000:5000 --name my-flask-app <username>/my-flask-service:latest
```
   ![](/media/14.jpg)
   ![](/media/15.jpg)
   ![](/media/16.jpg)

   
## 6. РАЗВЁРТКА В MINIKUBE (KUBERNETES)

### Что сделано:

1. Установлен и запущен Minikube: `minikube start --driver=docker`
2. Созданы три Kubernetes манифеста в папке `k8s/`:
   - `00-namespace.yaml` — создание пространства `my-app`
   - `01-deployment.yaml` — Deployment с 2 репликами
   - `02-service.yaml` — Service типа NodePort (порт 30001)
3. Выполнено применение манифестов: `kubectl apply -f k8s/`
4. Проверена работа сервиса через `minikube service`

![](/media/17.png)
![](/media/18.png)
![](/media/19.png)
![](/media/20.png)

