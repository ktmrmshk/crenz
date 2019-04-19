FROM python:3.6-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl screen vim wget git \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/* \
      && python3 -m pip install requests flask dnspython gunicorn \
      && git clone https://github.com/ktmrmshk/crenz.git

ENV PYTHONPATH /crenz

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000","crenz.crenz_web:app"]
