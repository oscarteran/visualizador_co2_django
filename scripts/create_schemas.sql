-- Script SQL para crear esquemas y configurar PostGIS
-- Ejecutar este script después de crear la base de datos

-- Crear esquema para datos de CO2
CREATE SCHEMA IF NOT EXISTS co2_data;

-- Crear esquema para datos geográficos
CREATE SCHEMA IF NOT EXISTS geo_data;

-- Crear esquema para datos procesados
CREATE SCHEMA IF NOT EXISTS processed_data;

-- Habilitar extensión PostGIS (si no está habilitada)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Crear tabla principal de mediciones de CO2
CREATE TABLE IF NOT EXISTS co2_data.measurements (
    id SERIAL PRIMARY KEY,
    utm_x DOUBLE PRECISION NOT NULL,
    utm_y DOUBLE PRECISION NOT NULL,
    co2_value DOUBLE PRECISION NOT NULL,
    zone_name VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    location GEOMETRY(POINT, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_measurements_zone_name ON co2_data.measurements(zone_name);
CREATE INDEX IF NOT EXISTS idx_measurements_co2_value ON co2_data.measurements(co2_value);
CREATE INDEX IF NOT EXISTS idx_measurements_created_at ON co2_data.measurements(created_at);
CREATE INDEX IF NOT EXISTS idx_measurements_location ON co2_data.measurements USING GIST(location);

-- Crear tabla de zonas
CREATE TABLE IF NOT EXISTS co2_data.zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de estadísticas por zona
CREATE TABLE IF NOT EXISTS co2_data.zone_statistics (
    id SERIAL PRIMARY KEY,
    zone_name VARCHAR(100) NOT NULL,
    total_measurements INTEGER NOT NULL,
    avg_co2_value DOUBLE PRECISION NOT NULL,
    min_co2_value DOUBLE PRECISION NOT NULL,
    max_co2_value DOUBLE PRECISION NOT NULL,
    std_co2_value DOUBLE PRECISION,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_name) REFERENCES co2_data.zones(name)
);

-- Función para actualizar estadísticas automáticamente
CREATE OR REPLACE FUNCTION update_zone_statistics()
RETURNS TRIGGER AS $$
BEGIN
    -- Actualizar estadísticas cuando se inserten/actualicen mediciones
    INSERT INTO co2_data.zone_statistics (
        zone_name,
        total_measurements,
        avg_co2_value,
        min_co2_value,
        max_co2_value,
        std_co2_value
    )
    SELECT 
        zone_name,
        COUNT(*) as total_measurements,
        AVG(co2_value) as avg_co2_value,
        MIN(co2_value) as min_co2_value,
        MAX(co2_value) as max_co2_value,
        STDDEV(co2_value) as std_co2_value
    FROM co2_data.measurements
    WHERE zone_name = NEW.zone_name
    GROUP BY zone_name
    ON CONFLICT (zone_name) DO UPDATE SET
        total_measurements = EXCLUDED.total_measurements,
        avg_co2_value = EXCLUDED.avg_co2_value,
        min_co2_value = EXCLUDED.min_co2_value,
        max_co2_value = EXCLUDED.max_co2_value,
        std_co2_value = EXCLUDED.std_co2_value,
        calculated_at = CURRENT_TIMESTAMP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger para actualizar estadísticas automáticamente
DROP TRIGGER IF EXISTS trigger_update_zone_statistics ON co2_data.measurements;
CREATE TRIGGER trigger_update_zone_statistics
    AFTER INSERT OR UPDATE ON co2_data.measurements
    FOR EACH ROW
    EXECUTE FUNCTION update_zone_statistics();

-- Función para crear punto geográfico automáticamente
CREATE OR REPLACE FUNCTION create_geo_point()
RETURNS TRIGGER AS $$
BEGIN
    -- Crear punto geográfico desde lat/lon
    NEW.location = ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger para crear punto geográfico automáticamente
DROP TRIGGER IF EXISTS trigger_create_geo_point ON co2_data.measurements;
CREATE TRIGGER trigger_create_geo_point
    BEFORE INSERT OR UPDATE ON co2_data.measurements
    FOR EACH ROW
    EXECUTE FUNCTION create_geo_point();

-- Crear vista para consultas comunes
CREATE OR REPLACE VIEW co2_data.measurements_with_stats AS
SELECT 
    m.*,
    zs.total_measurements,
    zs.avg_co2_value,
    zs.min_co2_value,
    zs.max_co2_value,
    zs.std_co2_value
FROM co2_data.measurements m
LEFT JOIN co2_data.zone_statistics zs ON m.zone_name = zs.zone_name;

-- Insertar datos de zonas desde los archivos CSV
INSERT INTO co2_data.zones (name, description) VALUES
('Acoculco', 'Zona de Acoculco - Mediciones de CO2'),
('Alcaparrosa', 'Zona de Alcaparrosa - Mediciones de CO2'),
('Azufres', 'Zona de Azufres - Mediciones de CO2'),
('Chichinautzin', 'Zona de Chichinautzin - Mediciones de CO2'),
('Escalera', 'Zona de Escalera - Mediciones de CO2'),
('Michoa', 'Zona de Michoa - Mediciones de CO2'),
('Puruandiro', 'Zona de Puruandiro - Mediciones de CO2')
ON CONFLICT (name) DO NOTHING;

-- Comentarios en las tablas
COMMENT ON TABLE co2_data.measurements IS 'Tabla principal de mediciones de CO2 con coordenadas geográficas';
COMMENT ON TABLE co2_data.zones IS 'Catálogo de zonas de medición';
COMMENT ON TABLE co2_data.zone_statistics IS 'Estadísticas calculadas por zona';
COMMENT ON VIEW co2_data.measurements_with_stats IS 'Vista que combina mediciones con estadísticas de zona';

-- Mostrar información de las tablas creadas
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE schemaname IN ('co2_data', 'geo_data', 'processed_data')
ORDER BY schemaname, tablename;
