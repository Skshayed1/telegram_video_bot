# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make static folder accessible
RUN mkdir -p /app/static

# Expose default port (optional)
EXPOSE 8080

# Start the bot
CMD ["python", "bot.py"]
