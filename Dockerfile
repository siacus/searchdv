# Use the official Python 3.10 image
#FROM python:3.10
FROM quay.io/fedora/python-310

# Set the working directory
# WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . . 

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app with Uvicorn
# CMD ["uvicorn", "searchdv:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
CMD uvicorn searchdv:app --host 0.0.0.0 --port 8000
#
# docker tag searchdv smiacus/searchdv
# docker push smiacus/searchdv