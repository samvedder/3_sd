-- Crear un keyspace
CREATE KEYSPACE IF NOT EXISTS test_keyspace WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': '1'
} AND durable_writes = true;

-- Usar el keyspace recién creado
USE test_keyspace;

-- Crear una tabla
CREATE TABLE IF NOT EXISTS alerts (
  uuid text PRIMARY KEY,
  country text,
  city text,
  reliability int,
  type text,
  speed int,
  subtype text,
  street text,
  id text,
  ncomments int,
  inscale boolean,
  confidence int,
  roadtype int,
  location_x double,
  location_y double,
  pubmillis bigint
);