# Use Python 3.12 Debian-based image (NOT Alpine - Alpine lacks pkg_resources/setuptools by default)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        musl-dev \
        ffmpeg \
        aria2 \
        make \
        g++ \
        cmake \
        wget \
        unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Build and install mp4decrypt from Bento4
RUN wget -q https://github.com/axiomatic-systems/Bento4/archive/v1.6.0-639.zip && \
    unzip v1.6.0-639.zip && \
    cd Bento4-1.6.0-639 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j$(nproc) && \
    cp mp4decrypt /usr/local/bin/ && \
    cd ../.. && \
    rm -rf Bento4-1.6.0-639 v1.6.0-639.zip

# Copy all files
COPY . .

# Install Python dependencies (setuptools first to ensure pkg_resources is available)
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r sainibots.txt \
    && pip install -U yt-dlp \
    && pip install --no-cache-dir m3u8 aiofiles aiohttp

# ── aria2c config for max speed ──────────────────────────────────────────────
RUN mkdir -p /root/.aria2 && echo "\
max-connection-per-server=16\n\
min-split-size=1M\n\
split=16\n\
max-concurrent-downloads=32\n\
file-allocation=none\n\
retry-wait=2\n\
max-tries=5\n\
timeout=30\n\
connect-timeout=10\n\
" > /root/.aria2/aria2.conf

ENV COOKIES_FILE_PATH="/app/modules/youtube_cookies.txt"

# Run gunicorn (web server for Render port detection) + bot in parallel
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} app:app & python3 modules/main.py"]
