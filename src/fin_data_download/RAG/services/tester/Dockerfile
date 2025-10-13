FROM curlimages/curl:8.10.1
WORKDIR /app
COPY services/tester/run.sh ./run.sh
RUN chmod +x run.sh
CMD ["./run.sh"]
