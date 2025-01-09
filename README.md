# ms-profile

## Descripción del Proyecto

**ms-profile** es un servicio que gestiona la información de perfiles de usuarios, permitiendo almacenar y procesar información relacionada con su experiencia laboral, habilidades, y otros datos relevantes. Este servicio se integra con otros microservicios como **ms-scraper** y **ms-job** para ofrecer funcionalidades avanzadas, como la generación automática de perfiles a partir de archivos de CV.

## Funcionalidades Principales

- **Procesamiento de CVs**:
  - Permite cargar CVs en formato PDF.
  - Extrae automáticamente datos relevantes del CV, como experiencia laboral, educación y habilidades.

- **Gestión de Perfiles**:
  - CRUD de perfiles, con soporte para actualización y eliminación de datos.
  - Almacenamiento eficiente de perfiles procesados.

- **Integración con ms-scraper y ms-job**:
  - Vinculación de perfiles con ofertas de trabajo generadas por otros servicios.

- **API RESTful**:
  - Endpoints para interactuar con los perfiles de los usuarios.

- **Validación de Datos**:
  - Uso de Pydantic para garantizar que los datos procesados cumplan con los requisitos del sistema.

## Arquitectura

- **Procesamiento de Datos**:
  - Extracción de información de CVs utilizando herramientas de procesamiento de texto.

- **Base de Datos**:
  - Uso de PostgreSQL para el almacenamiento de perfiles.
  - Modelos definidos utilizando SQLAlchemy.

- **Integración con Kafka**:
  - Publicación de eventos relacionados con la creación y actualización de perfiles.

## Configuración

### Variables de Entorno

El proyecto requiere las siguientes variables de entorno, configuradas en un archivo `.env`:

- `DB_HOST`: Host de la base de datos.
- `DB_PORT`: Puerto de la base de datos.
- `DB_NAME`: Nombre de la base de datos.
- `DB_USER`: Usuario de la base de datos.
- `DB_PASSWORD`: Contraseña de la base de datos.
- `PROFILE_PROCESSING_API_URL`: URL del servicio para procesar CVs.
- `KAFKA_BOOTSTRAP_SERVERS`: Dirección del servidor Kafka.

### Instalación

1. Clona este repositorio:
   ```bash
   git clone <repositorio>
   cd ms-profile
