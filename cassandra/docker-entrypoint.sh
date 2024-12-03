#!/bin/bash
set -e

# Iniciar Cassandra usando el entrypoint original en segundo plano
echo "Iniciando Cassandra..."
/usr/local/bin/base-entrypoint.sh cassandra -f &

# Obtener el PID del proceso de Cassandra
CASSANDRA_PID=$!

# Esperar hasta que Cassandra esté listo para aceptar conexiones
echo "Esperando que Cassandra inicie completamente..."
until cqlsh cassandra -e 'DESCRIBE KEYSPACES;' > /dev/null 2>&1; do
  echo "Cassandra no está listo, esperando 10 segundos..."
  sleep 5
done

# Ejecutar el script de inicialización
echo "Cassandra está listo, ejecutando scripts de inicialización..."
cqlsh cassandra -f /db-init/init.cql

echo "Inicialización completada."

# Esperar a que Cassandra continúe ejecutándose en primer plano
wait $CASSANDRA_PID