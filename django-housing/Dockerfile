FROM python:3.11-slim  

WORKDIR /usr/src/django-housing

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer les dépendances système nécessaires à Pillow et PostgreSQL
RUN apt-get update && apt-get install -y \
    curl\
    build-essential \
    python3-dev \
    gcc \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    zlib1g-dev \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install wait-for-it
RUN curl -LO https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x wait-for-it.sh \
    && mv wait-for-it.sh /usr/local/bin/wait-for-it


    
# Mise à jour de pip, setuptools et wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copie et installation des dépendances Python
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# RUN pip install Pillow==10.2.0 

# Copie du script d'entrée et configuration
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/django-housing/entrypoint.sh && chmod +x /usr/src/django-housing/entrypoint.sh

# Copier le reste de l'application
COPY . .

# Configuration de l'entrée
ENTRYPOINT [ "/usr/src/django-housing/entrypoint.sh" ]
