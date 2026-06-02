# 📊 Sistema de Inteligencia de Negocios para el Municipio de Zapotlanejo

## Objetivo del Proyecto

Desarrollar una solución integral de Inteligencia de Negocios y Big Data para evaluar la madurez digital del sector textil y gastronómico en Zapotlanejo, Jalisco. Este sistema está diseñado para transformar datos de presencia web y redes sociales en métricas accionables, para en un futuro optimizar la toma de decisiones estratégicas y comerciales en Zapotlanejo.

**Objetivos Específicos:**

- **Diagnóstico Comercial:** Proporcionar un panorama técnico y claro sobre la infraestructura digital actual de los negocios en el municipio.
- **Inteligencia de Negocios:** Construir tableros interactivos que faciliten el análisis ágil y preciso de los indicadores clave de rendimiento (KPIs).
- **Análisis de Patrones:** Identificar conductas de mercado cruzando la evidencia de impacto digital en la red con las dinámicas físicas y geográficas de la zona.
- **Toma de Decisiones:** Facilitar la implementación de iniciativas tecnológicas basadas en evidencia para mejorar la competitividad y digitalización de los locales.

---

## 🏗️ 1. Arquitectura de Sistemas y Flujo de Datos

El proyecto se diseñó estructurando un diagrama BPMN para asegurar la integridad de la información desde su levantamiento físico hasta la visualización directiva.

![Arquitectura General](URL_DE_TU_IMAGEN_AQUI)

---

## 🗄️ 2. Modelado de Base de Datos (SQL Server)

Para centralizar y procesar el censo de negocios, se implementó un modelo relacional normalizado tipo **Copo de Nieve (3FN)**. Esto garantiza la integridad referencial y optimiza el rendimiento de las consultas para las herramientas analíticas.

<!-- BRO: Arrastra aquí la captura de tu diagrama relacional de SQL Server -->

![Modelo Copo de Nieve](URL_DE_TU_IMAGEN_AQUI)

**Ejemplo de creación de vistas para análisis (SQL):**

```sql

    VISTA DE RELACION DE SEGUIDORES A AFLUENCIA DE LA ZONA
    CREATE VIEW V_Relacion_Seguidores_Zona AS
        SELECT

        E.Nombre            AS Nombre_Negocio,
        F.Seguidores            AS Total_Seguidores,
        G.Nombre_Zona           AS Zona,
        G.Afluencia_Peatonal    AS Afluencia_Peatonal,
        G.Es_zona_turistica     AS Es_Zona_Turística

    FROM [Presencia Posicionamiento Digital] AS F
    INNER JOIN [Sucursal] AS S
        ON F.ID_Sucursal = S.ID_Sucursal
    INNER JOIN [Geografia] AS G
        ON S.ID_Geografia = G.ID_Geografia
    INNER JOIN [Establecimiento] AS E
        ON S.ID_Establecimiento = E.ID;

```

## 🔬 3. Análisis Exploratorio de Datos (RStudio)

Se procesaron los datos extraídos utilizando **RStudio** y la librería `ggplot` para ejecutar análisis estadísticos descriptivos, encontrando el promedio de seguidores por zona

**Ejemplo de Análisis Estadístico (Script en R):**

```r

    modelo_negocio_BI <- dbGetQuery(con, query_by)
    #View(modelo_negocio_BI)
    #Estadistica para ver el promedio de seguidores por zona
    Zona_mas_seguidores <- modelo_negocio_BI %>%
    group_by(Zona) %>%
    summarise(
        Seguidores_Por_zona = mean(Total_Seguidores) # mean promedio
    ) %>%
    arrange(desc(Seguidores_Por_zona))

    #GRAFICA PROMEDIO DE SEGUIDORES POR ZONA
    ggplot(Zona_mas_seguidores, aes(x = reorder(Zona, Seguidores_Por_zona),
                                y = Seguidores_Por_zona, fill = Zona)) +
    geom_col(show.legend = FALSE) +
    coord_flip() +
    theme_minimal() +
    labs(
        title = "Promedio de Seguidores por Zona",
        subtitle = "Análisis del alcance digital por Zona",
        x = "Colonias",
        y = "Promedio de Seguidores en Redes"
    )
```

![Grafica de RStudio (Promedio seguidores por Zona)](URL_DE_TU_IMAGEN_AQUI)

## 📈 4. Inteligencia de Negocios y Visualización (Power BI)

La parte final se hizo en Power BI, aplicando funciones lógicas en DAX para categorizar la madurez digital e integrar mapas de geolocalización, entre otras cosas. Todas estas funciones derivadas de la informacion almacenada en nuestra base de datos fueron asignadas a Dashboards inteligentes e interactivos, con la finalidad de dar datos concretos de la situacion digital en el municipio de Zapotlanejo.

**Ejemplo de Lógica de Negocio (Función DAX):**

```dax
    Nivel_Presencia_RS =
    SWITCH(
        TRUE(),
        'Presencia Posicionamiento Digital'[Seguidores] >= 1000, "Presencia Fuerte",
        'Presencia Posicionamiento Digital'[Seguidores] >= 300, "Presencia Media",
        'Presencia Posicionamiento Digital'[Seguidores] >= 0, "Presencia Baja",
        "Sin Datos"
    )
```

## Dashboards Interactivos

**Dashboard 1 (General)**

![Dashboard 1 (General)](URL_DE_TU_IMAGEN_AQUI)

**Dashboard 2 (WEB)**

![Dashboard 2 (WEB)](URL_DE_TU_IMAGEN_AQUI)

**Dashboard 3 (Redes Sociales)**

![Dashboard 3 (Redes Sociales)](URL_DE_TU_IMAGEN_AQUI)

**Dashboard 4 (Analisis Peatonal y Turistico)**

![Dashboard 4 (Analisis Peatonal y Turistico)](URL_DE_TU_IMAGEN_AQUI)
