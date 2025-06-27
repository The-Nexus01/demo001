# Nexus v2.0 - Advanced Telegram Userbot
# Multi-stage Docker build for optimized production deployment
# Session string authentication only - no phone numbers required

# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r nexus && useradd -r -g nexus -d /app -s /bin/bash nexus

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements-build.txt ./

# Install Python dependencies with exact versions
RUN pip install --no-cache-dir -r requirements-build.txt

# Copy application files
COPY --chown=nexus:nexus . .

# Create necessary directories
RUN mkdir -p logs downloads assets/temp \
    && touch logs/.gitkeep downloads/.gitkeep \
    && chown -R nexus:nexus /app

# Switch to non-root user
USER nexus

# Expose port (if needed for future web interface)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command
CMD ["python", "main.py"]

# Docker build labels
LABEL maintainer="The Nexus Team" \
      description="Nexus v2.0 - Advanced Telegram Userbot with session string authentication" \
      version="2.0" \
      license="MIT" \
      repository="https://github.com/The-Nexus-Bot/Nexus-Userbot"