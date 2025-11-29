FROM python:3.11-slim


# Install tesseract system dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
tesseract-ocr \
libtesseract-dev \
poppler-utils \
&& rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# Create a models directory
RUN mkdir /app/models /app/uploads
COPY . /app


EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "1"]