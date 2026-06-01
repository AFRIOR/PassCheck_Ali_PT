FROM python:3.13-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

EXPOSE 5000

CMD ["python", "server.py"]