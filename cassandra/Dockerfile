# Etapa 1: Usar la imagen oficial de Cassandra como base
FROM cassandra:4.1.7 AS base

# Etapa 2: Crear la imagen personalizada
FROM base

# Crear el directorio para los scripts de inicialización
RUN mkdir -p /db-init

# Copiar el script de inicialización desde el contexto de construcción
COPY db-init/init.cql /db-init/init.cql

# Copiar el script de entrypoint personalizado
COPY cassandra/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Copiar el entrypoint original a una nueva ubicación
COPY --from=base /usr/local/bin/docker-entrypoint.sh /usr/local/bin/base-entrypoint.sh

# Hacer ejecutable el script de entrypoint personalizado
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Establecer el nuevo entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]

# Comando por defecto
CMD ["cassandra", "-f"]