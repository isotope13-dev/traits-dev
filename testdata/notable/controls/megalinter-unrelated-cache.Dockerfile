FROM alpine:3.24
RUN curl -fsSL https://example.org/linter.zip -o /tmp/linter.zip
RUN unzip /tmp/linter.zip -d /usr/bin
RUN chmod +x /usr/bin/linter && rm -f /tmp/linter.zip

# An unrelated cache setting must not join the earlier /tmp locations.
ENV MYPY_CACHE_DIR=/tmp/.mypy_cache
