FROM relaysh/core:latest-python
RUN pip --no-cache-dir install sendgrid
COPY "./step.py" "/step.py"
ENTRYPOINT []
CMD ["python3", "/step.py"]

LABEL "org.opencontainers.image.title"="Send email with SendGrid"
LABEL "org.opencontainers.image.description"="This step allows you to sd an email using the SendGrid API"
LABEL "sh.relay.sdk.version"="v1"
