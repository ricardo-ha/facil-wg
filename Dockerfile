FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
#    dpkg \
#    dumb-init \
    iproute2 \
    iptables \
#    iptables-legacy \
    wireguard-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app

ENV DEBUG=Server,WireGuard

CMD ["python", "app.py"] 
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]

# Iamge:
# docker build -t facil-wg .
# Container:
# docker run -d \
#    -p 51820:51820/udp \
#    -p 80:8080 \
#    --cap-add=NET_ADMIN \
#    --cap-add=SYS_MODULE \
#    --name wg \
#    -e PASSWORD="Your password utf-8" \
#    -e HOST="Your public ip or your host domain name (DDNS)" \
#    facil-wg

