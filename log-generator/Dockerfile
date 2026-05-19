# ==========================================
# STAGE 1: Build Stage (Dependencies)
# ==========================================
FROM --platform=linux/amd64 node:20-slim AS builder

WORKDIR /usr/src/app

# Layer Caching: Pehle package files copy karke dependencies install karo
COPY package*.json ./
RUN npm install --production

# Pura source code copy karo
COPY . .

# ==========================================
# STAGE 2: Final Runtime Stage (Lightweight)
# ==========================================
FROM --platform=linux/amd64 node:20-alpine AS runner

WORKDIR /usr/src/app

# Builder stage se sirf node_modules aur code utha kar laao
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app ./

EXPOSE 5000

# Security Best Practice: Non-root user use karo
USER node

CMD ["npm", "start"]
