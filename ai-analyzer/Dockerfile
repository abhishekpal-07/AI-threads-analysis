# ==========================================
# STAGE 1: Build Dependencies
# ==========================================
FROM --platform=linux/amd64 python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .

# Global folder ke bajaye user directory me packages install karna for clean copying
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# STAGE 2: Final Slim Runtime
# ==========================================
FROM --platform=linux/amd64 python:3.9-slim AS runner

WORKDIR /app

# Builder stage se python installed packages local directory me copy karna
COPY --from=builder /root/.local /root/.local
COPY . .

# Path set karo taaki python un installed dependencies को dhoond sake
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

# Script running command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
