FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

# Verify it works
RUN uv --version

# Copy pyproject.toml
COPY pyproject.toml .
# COPY uv.lock .  # <-- only if you want reproducibility (optional but recommended)

# Install deps
RUN uv sync

# Copy the rest of your Dagster project
COPY . .

EXPOSE 8080

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use entrypoint to run db migrate + start api-server
CMD ["/entrypoint.sh"]
