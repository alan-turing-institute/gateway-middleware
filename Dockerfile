FROM base/archlinux:latest
RUN pacman -Sy --noconfirm python python-pip sqlite3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP app.py
RUN sed -i "s/#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/" /etc/locale.gen
RUN locale-gen
ENV LANG=en_US.UTF-8
EXPOSE 8080
RUN rm test.db
RUN python create_and_mint_case_using_stores.py
CMD ["python","app.py"]

