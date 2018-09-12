FROM base/archlinux:latest

# Install a bunch of extra packages
RUN pacman -Sy --noconfirm python python-pip

# Set up a UTF 8 locale
RUN sed -i "s/#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/" /etc/locale.gen
RUN locale-gen
ENV LANG=en_US.UTF-8

# Copy over the code to run
ADD . /app
WORKDIR /app

# Now install the python requirements
RUN pip install -r requirements.txt

# Set up the application state
ENV FLASK_APP app.py

# Configure the run command
# python is invoked in development
# gunicorn is invoked in production 
# (via docker-compose.production.yml)
CMD ["python","app.py"]