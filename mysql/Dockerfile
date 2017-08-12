FROM mysql:5.7

ADD dump.sql /docker-entrypoint-initdb.d

EXPOSE 3306
CMD ["mysqld"]
