FROM python:3.9-slim

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        libxcb-xinerama0-dev \
        libxcb-xinerama0 \
        libxcb-icccm4-dev \
        libxcb-icccm4 \
        libxcb-image0-dev \
        libxcb-image0 \
        libxcb-keysyms1-dev \
        libxcb-keysyms1 \
        libxcb-randr0-dev \
        libxcb-randr0 \
        libxcb-render-util0-dev \
        libxcb-render-util0 \
        libxcb-shape0-dev \
        libxcb-shape0 \
        libxcb-sync-dev \
        libxcb-sync1 \
        libxcb-xfixes0-dev \
        libxcb-xfixes0 \
        libxcb-xkb-dev \
        libxcb-xkb1 \
        libxkbcommon-dev \
        libxkbcommon-x11-0 \
        libxkbcommon0 \
        libxcb-xinerama0 \
        libxcb-xinerama0-dev \
        python3-dev \
        pyqt5-dev \
        pyqt5-dev-tools \
        qtbase5-dev \
        qttools5-dev \
        qttools5-dev-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

