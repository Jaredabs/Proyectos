install.packages("DBI")
install.packages("odbc")
install.packages("dplyr")
install.packages("dbplyr")
install.packages("ggplot2")

library(DBI)
library(odbc)
library(dplyr)
library(dbplyr)
library(ggplot2)

con <- dbConnect(odbc(), 
                 Driver = "ODBC Driver 17 for Sql Server",
                 Server = "LAPTOP-FGV55536",
                 Database = "DBNegocios",
                 Trusted_Connection= "yes"
)
dbListTables(con)




query_by <- "Select * from V_datos"


modelo_negocio_BI <- dbGetQuery(con, query_by)
View(modelo_negocio_BI)
#--------------------------------------------------------------------------------------------------V_datos
#Numero de negocios por zona y los tipos que hay en cada zona(Restaurantes o Tiendas de Ropa)
Comerciosxzona <- modelo_negocio_BI %>% 
  group_by(Nombre_de_la_Zona, Afluencia_de_peatones) %>%
  summarise(
    Total_Comercios = n(), 
    Giros_Disponibles = n_distinct(Tipo_de_Negocio) 
  ) %>% 
  arrange(desc(Total_Comercios)) 
View(Comerciosxzona)



ggplot(Comerciosxzona, aes( x = reorder(Nombre_de_la_Zona, Total_Comercios), 
                            y = Total_Comercios, fill = Nombre_de_la_Zona)) +
  geom_col(show.legend = FALSE) + 
  coord_flip() +                  
  theme_minimal() +              
  labs(
    title = "Numero de Negocios por Zona",
    subtitle = "establecimientos físicos en Zapotlanejo",
    x = "Zonas de Zapotlanejo",
    y = "Total de Comercios Físicos"
  )



#Locales por tipo de negocio y Cuales tienen Web
Negocios_web <- modelo_negocio_BI %>%
  group_by(Tipo_de_Negocio) %>% # Agrupar por el tipo o clave de giro comercial
  summarise(
    Cantidad_Locales = n(), # Suma el total de piezas (establecimientos) instalados de ese giro
    Locales_Con_Web = sum(!is.na(Url_de_Pagina) & Url_de_Pagina != "NULL") # Cuenta cuántos de ellos ya tienen infraestructura web
  ) %>%
  arrange(desc(Cantidad_Locales)) # Ordena de mayor a menor presencia en el municipio

#View(Negocios_web)






ggplot(Negocios_web, aes( x = reorder(Tipo_de_Negocio, Cantidad_Locales), 
                          y = Cantidad_Locales, fill = Tipo_de_Negocio)) +
  geom_col(show.legend = FALSE) + 
  coord_flip() + 
  theme_minimal() + 
  labs(
    title = "Presencia Comercial por Tipo de Negocio",
    x = "Tipo de Negocio",
    y = "Cantidad Total de Locales"
  )

#---------------------------------------------------------------------------------V_Perfiles_Redes

query_by <- "Select * from V_Perfiles_Redes"


modelo_negocio_BI <- dbGetQuery(con, query_by)
View(modelo_negocio_BI)

#Estadistica que muestra cual red social es mas usada por los negocios en zapotlanejo
Red_Preferida <- modelo_negocio_BI %>%
  group_by(RED_SOCIAL) %>%
  summarise(
    Cantidad_Por_RedSocial = n()
    
  )%>%
  arrange(desc(Cantidad_Por_RedSocial)) # Ordena de mayor a menor

#View(Red_Preferida)






ggplot(Red_Preferida, aes(x = reorder(RED_SOCIAL, Cantidad_Por_RedSocial), 
                          y = Cantidad_Por_RedSocial, fill = RED_SOCIAL)) +
  geom_col(show.legend = FALSE) +               
  theme_minimal() +               
  labs(
    title = "Red Social Preferida por los Negocios",
    x = "Red Social",
    y = "Cantidad de Cuentas"
  )
#---------------------------------------------------------------------------------V_Relacion_Seguidores_Zona
query_by <- "Select * from V_Relacion_Seguidores_Zona"


modelo_negocio_BI <- dbGetQuery(con, query_by)
#View(modelo_negocio_BI)
#Estadistica para ver el promedio de seguidores por zona
Zona_mas_seguidores <- modelo_negocio_BI %>%
  group_by(Zona) %>%
  summarise(
    Seguidores_Por_zona = mean(Total_Seguidores) # mean promedio
  ) %>%
  arrange(desc(Seguidores_Por_zona))
View(Zona_mas_seguidores)




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

#Estadistica para ver Seguidores dependiendo afluencia de gente
Impacto_Afluencia <- modelo_negocio_BI %>%
  group_by(Afluencia_Peatonal) %>%
  summarise(
    Cantidad_Locales = n(),                                    
    Promedio_Seguidores = mean(Total_Seguidores, na.rm = TRUE), 
    Maximo_Seguidores = max(Total_Seguidores, na.rm = TRUE),   # EL que tiene mas seguidores
    Minimo_Seguidores = min(Total_Seguidores, na.rm = TRUE)    # El de menos
  ) %>%
  arrange(desc(Promedio_Seguidores))

View(Impacto_Afluencia)







ggplot(Impacto_Afluencia, aes(x = reorder(Afluencia_Peatonal, Promedio_Seguidores), 
                              y = Promedio_Seguidores, fill = Afluencia_Peatonal)) +
  geom_col(show.legend = FALSE) + # Dibuja las barras y oculta la leyenda para optimizar espacio
  coord_flip() +                  # Hace las barras horizontales para facilitar la lectura
  theme_minimal() +               # Aplica un fondo limpio y moderno
  labs(
    title = "Impacto de la Afluencia Peatonal en el Alcance Digital",
    x = "Nivel de Afluencia Peatonal",
    y = "Promedio de Seguidores"
  )
#---------------------------------------------------------------------------------V_Relacion_WifiAlPublico_NumeroOpiniones
query_by <- "Select * from V_Relacion_WifiAlPublico_NumeroOpiniones"


modelo_negocio_BI <- dbGetQuery(con, query_by)
View(modelo_negocio_BI)
#Cantidad de negocios con y sin wifi
 negocios_Wifi<- modelo_negocio_BI %>%
  mutate(Hay_Wifi_Alpublico = ifelse(Hay_Wifi_Alpublico == TRUE | Hay_Wifi_Alpublico == 1, "Sí", "No")) %>% #Cambiar boleanos a si y no
  group_by(Hay_Wifi_Alpublico) %>%
  summarise(
    Cantidad = n(),                                    
   
  ) %>%
  arrange(desc(Cantidad))

View(negocios_Wifi)






ggplot(negocios_Wifi, aes(x = reorder(Hay_Wifi_Alpublico, Cantidad), 
                          y = Cantidad, fill = Hay_Wifi_Alpublico)) +
  geom_col(show.legend = FALSE) + 
  coord_flip() +                  
  theme_minimal() +            
  labs(
    title = "Disponibilidad de Wifi Público en los Negocios",
    x = "¿Ofrece Wifi al Público?",
    y = "Cantidad de Negocios"
  )

#Tener wifi en los locales, aumenta el numero de opiniones en maps?
Impacto_Wifi_Opiniones <- modelo_negocio_BI %>%
  
  mutate(Hay_Wifi_Alpublico = ifelse(Hay_Wifi_Alpublico == TRUE | Hay_Wifi_Alpublico == 1, "Sí", "No")) %>%
  group_by(Hay_Wifi_Alpublico) %>%
  
  summarise(
    Cantidad_Locales = n(),                                   
    Promedio_Opiniones = mean(Total_Opiniones, na.rm = TRUE),#meida
    Maximo_Opiniones = max(Total_Opiniones, na.rm = TRUE),    
    Minimo_Opiniones = min(Total_Opiniones, na.rm = TRUE)     
  ) %>%
  arrange(desc(Promedio_Opiniones))
View(Impacto_Wifi_Opiniones)





ggplot(Impacto_Wifi_Opiniones, aes(x = reorder(Hay_Wifi_Alpublico, Promedio_Opiniones), 
                                   y = Promedio_Opiniones, fill = Hay_Wifi_Alpublico)) +
  geom_col(show.legend = FALSE) + # Dibuja las barras y oculta la leyenda para optimizar espacio
  coord_flip() +                  # Hace las barras horizontales para facilitar la lectura
  theme_minimal() +               # Aplica un fondo limpio y moderno
  labs(
    title = "Impacto de la WIFI en el numero de opiniones",
    x = "¿Ofrece Wifi al Público?",
    y = "Promedio de Opiniones / Reseñas"
  )

#---------------------------------------------------------------------------------V_Relacion_ZonaTuristica_AlSentimiento
query_by <- "Select * from V_Relacion_ZonaTuristica_AlSentimiento"
modelo_negocio_BI <- dbGetQuery(con, query_by)
View(modelo_negocio_BI)


#Sentimiento de las personas por zona 
Zona_relacion_Sentimiento <- modelo_negocio_BI %>%
  
  
  group_by(Zona_Turistica, Sentimiento_Dominante) %>%
  summarise(
    Cantidad_Locales = n() 
  ) %>%
  arrange(Zona_Turistica, desc(Cantidad_Locales))

View(Zona_relacion_Sentimiento)
  



ggplot(Zona_relacion_Sentimiento, aes(x = reorder(Zona_Turistica, Cantidad_Locales), 
                                      y = Cantidad_Locales, fill = Sentimiento_Dominante)) +
  geom_col() +      
  coord_flip() +   
  theme_minimal() + 
  labs(
    title = "Sentimiento del Cliente Dependiendo la Zona",
    x = "¿Es Zona Turística?",
    y = "Cantidad de Establecimientos",
    fill = "Sentimiento Dominante"
  )
#---------------------------------------------------------------------------------V_Relacion_ZonaTuristica_NumeroOpiniones
query_by <- "Select * from V_Relacion_ZonaTuristica_NumeroOpiniones"
modelo_negocio_BI <- dbGetQuery(con, query_by)
View(modelo_negocio_BI)


#Si la zona es turistica o no afecta en el numero de opiniones en internet?
Impacto_Zona_Opiniones <- modelo_negocio_BI %>%
  group_by(Zona_Turistica) %>%
  
  summarise(
    Cantidad_Locales = n(),                                  
    Promedio_Opiniones = mean(Total_Opiniones, na.rm = TRUE),
    Maximo_Opiniones = max(Total_Opiniones, na.rm = TRUE),    
    Minimo_Opiniones = min(Total_Opiniones, na.rm = TRUE)     
  ) %>%
  
  arrange(desc(Promedio_Opiniones))

View(Impacto_Zona_Opiniones)





ggplot(Impacto_Zona_Opiniones, aes(x = reorder(Zona_Turistica, Promedio_Opiniones), 
                                   y = Promedio_Opiniones, fill = Zona_Turistica)) +
  geom_col(show.legend = FALSE) + 
  coord_flip() +                 
  theme_minimal() +             
  labs(
    title = "Impacto del Entorno Turístico en el Numero de Opiniones",
    x = "¿Es Zona Turística?",
    y = "Promedio de Opiniones en Internet"
  )

