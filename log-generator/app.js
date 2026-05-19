const express = require('express');
const Redis = require('ioredis');

const app = express();
const PORT = 5000;

// Redis connection setup (Container name 'redis-queue' use karenge network me)
const redis = new Redis({
  host: 'redis-queue',
  port: 6379,
  maxRetriesPerRequest: 3
});

redis.on('connect', () => console.log('🎉 Log Generator Redis Queue se connect ho gaya!'));
redis.on('error', (err) => console.error('Redis connection error:', err.message));

// Fake logs generate karne ki repository (Normal vs Threat logs)
const logTemplates = [
  { status: 'INFO', message: 'User login successful from IP 192.168.1.5', label: 'safe' },
  { status: 'INFO', message: 'Database backup completed successfully', label: 'safe' },
  { status: 'WARNING', message: 'Multiple failed login attempts from IP 45.79.10.4', label: 'threat' },
  { status: 'CRITICAL', message: 'SQL Injection detected in login form field', label: 'threat' },
  { status: 'WARNING', message: 'CPU utilization reached 92%', label: 'safe' }
];

// Har 3 second me automatic log generate karke Redis Queue me push karne ka logic
setInterval(async () => {
  const randomLog = logTemplates[Math.floor(Math.random() * logTemplates.length)];
  const logPayload = {
    timestamp: new Date().toISOString(),
    ...randomLog
  };

  try {
    // Redis ki 'logs-queue' list me data push kar rahe hain (LPUSH)
    await redis.lpush('logs-queue', JSON.stringify(logPayload));
    console.log(`[Sent to Queue]: ${logPayload.status} - ${logPayload.message}`);
  } catch (err) {
    console.error('Queue me log push nahi ho paya:', err.message);
  }
}, 3000);

app.get('/status', (req, res) => {
  res.send({ status: 'running', service: 'Log Generator' });
});

app.listen(PORT, () => console.log(`Log Generator running on port ${PORT}`));
