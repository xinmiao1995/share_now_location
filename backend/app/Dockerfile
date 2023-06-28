FROM osgeo/gdal:ubuntu-small-latest

WORKDIR /app/

RUN apt-get update
RUN apt-get install -y python3 python3-pip

RUN pip install python-multipart fastapi uvicorn geopandas

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]