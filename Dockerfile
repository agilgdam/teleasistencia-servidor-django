FROM python:3.9

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requerimientos.txt requerimientos.txt
RUN pip install --no-cache-dir -r requerimientos.txt

COPY . app-tla
WORKDIR /app-tla/teleasistencia

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver_plus", "0.0.0.0:8000"]
