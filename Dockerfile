FROM python

RUN mkdir -p /app

COPY ./fwatchdog /usr/bin
RUN chmod +x /usr/bin/fwatchdog

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY index.py .
COPY function function

# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
ENV fprocess="python3 index.py"
# Set to true to see request in function logs
ENV combine_output='false'
ENV write_debug="false"
ENV write_timeout=0
ENV read_timeout=0
ENV exec_timeout=0

EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1
CMD [ "fwatchdog" ]