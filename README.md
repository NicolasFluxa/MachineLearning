## 📌 Claves de Relación (IDs)

* **bookingid**: Identificador único numérico de la reserva.
* **passengerid**: Identificador único del pasajero dentro de una reserva.
* **recordlocator (PNR)**: Código alfanumérico del registro de reserva.
* **passenger_key**: Concatenación del tipo de documento (Pasaporte/CI) + RUT o número de pasaporte. Un pasajero puede tener múltiples reservas.

---

## 💰 Revenue

* **total_revenue**: Ingresos totales generados por la reserva.
* **fare_revenue**: Ingresos correspondientes a la tarifa base.
* **ancillary_revenue**: Ingresos por servicios complementarios (equipaje, asientos, etc.).
* **discounted_fare_revenue_dc**: Ingresos por tarifa con descuento vía código de descuento.
* **discounted_fare_revenue_pc**: Ingresos por tarifa con descuento porcentual.
* **promocode**: Código promocional aplicado a la reserva (si existe).
* **has_promo_class**: Indicador (1/0) de si la reserva incluye una clase/tarifa promocional.

---

## 🧍 Pasajero (Flyer)

* **pax_type**: Tipo de pasajero (ADT = Adulto, CHD = Niño, INF = Bebé).
* **pax_gender**: Sexo del pasajero (1 = Hombre, 2 = Mujer).
* **language**: Idioma preferido del pasajero (si está disponible).

---

## 📦 Booking – Información Comercial (Booking 1)

* **pos**: Punto de venta de la reserva.
* **channelID**: Canal de venta

  * 1 = Contact Center
  * 2 = Website
  * 3 = API
  * 5 = GDS
* **channeltype**: Tipo de canal (Directo / Indirecto – Agencias).
* **channel_detail**: Detalle específico del canal de venta.
* **status**: Estado de la reserva (2, 3 = válidos).

---

## 🕒 Booking – Fechas y Tiempos

* **booking_date / booking_dt_utc**: Fecha y hora de emisión de la reserva (UTC).
* **time_zone**: Zona horaria asociada a la reserva.
* **booking_weeknumber**: Semana del año en que se realizó la reserva.
* **booking_weekday / booking_dow**: Día de la semana de compra (0–6 o 1–7).
* **booking_hour**: Hora del día en que se realizó la reserva.

---

## ✈️ Viaje – Fechas Clave

* **tripstart_date**: Fecha de salida del primer vuelo.
* **tripend_date**: Fecha de regreso (si aplica).
* **tripstart_weekday**: Día de la semana del inicio del viaje (0–6).
* **tripstart_month**: Mes de inicio del viaje (1–12).

---

## ⏱️ Métricas de Tiempo (Calculadas)

* **days_to_departure / d2g (Days to Gate)**: Días entre la compra y la salida.
* **los (Length of Stay)**: Duración del viaje en días (null para OneWay).
* **advance_ratio**: Desconocida.

---

## 📊 Bins y Categorizaciones

### Anticipación de Compra

* **advance_bin**:

  * Alta: > 15 días
  * Media: 4–14 días
  * Baja: < 4 días
  * Negativos: null

### Duración del Viaje

* **trip_length_bin**:

  * Largo: ≥ 6 días
  * Medio: > 2 y < 6 días
  * Corto: ≤ 2 días

---

## 👨‍👩‍👧‍👦 Pasajeros en la Reserva (Booking 2)

* **paxs / passengers**: Total de pasajeros en la reserva.
* **adults**: Número de adultos.
* **children / childs**: Número de niños (con asiento).
* **infants**: Número de bebés (en brazos).
* **has_chd_inf / has_child / has_infant**: Indicadores (1/0).
* **is_group**: Indicador (1/0) de reserva grupal.

---

## 🌍 Características del Viaje

* **trip_type**: Código numérico del tipo de viaje.
* **trip_rt**: Descripción del tipo de viaje (RoundTrip / OneWay).
* **is_roundtrip**: Indicador (1/0) de ida y vuelta.
* **trip_country**: País del viaje.
* **trip_market**: Mercado del viaje (Doméstico / Regional).
* **country_origin**: País de origen.
* **country_dest**: País de destino.
* **is_international**: Indicador (1/0) de viaje internacional.
* **is_cross_border**: Indicador (1/0) de cruce de fronteras.

---

## 📅 Lógica de Calendario (Bleisure)

* **includes_weekend**: El viaje incluye sábado o domingo.
* **only_weekdays**: El viaje ocurre solo en días hábiles.
* **tripstart_is_weekend**: La ida es en fin de semana.
* **tripend_is_weekend**: La vuelta es en fin de semana.

---

## 🎯 Objetivos / Labels

* **motivo_de_viaje**: Etiqueta real del motivo del viaje (Business / Leisure).
* **motivo_predicho**: Clasificación generada por el modelo.

---

Si quieres, en el siguiente paso puedo:

* Convertir esto en **JSON / YAML / Markdown técnico**
* Proponer un **modelo estrella (facts & dimensions)**
* O ayudarte a definir **features finales para ML** (bleisure / churn / revenue)

---

# Referencia Maestra de Parámetros XGBoost

Este documento detalla los hiperparámetros esenciales para la configuración, regularización y optimización de modelos XGBoost.

---

### 1. Control de Estructura y Aprendizaje

**`learning_rate` (eta)**:  
Controla la magnitud de la actualización de los pesos en cada paso (shrinkage). Después de cada paso de boosting, se obtienen los pesos de las nuevas características y el `learning_rate` reduce estos pesos para hacer el proceso de boosting más conservador.  
* **Significancia:** Un valor bajo hace que el modelo sea más robusto al sobreajuste (overfitting), pero el entrenamiento será más lento y requerirá más árboles (`n_estimators`). Un valor alto aprende rápido pero puede atascarse en óptimos locales o divergir.
* **Rango:** `[0, 1]`. Típico: `0.01 - 0.3`.

**`n_estimators`**:  
El número de iteraciones de boosting (número de árboles a construir).  
* **Significancia:** Si es muy bajo, el modelo no aprenderá lo suficiente (underfitting). Si es excesivamente alto, aumenta el riesgo de overfitting (aunque XGBoost es bastante resistente a esto si el `learning_rate` es bajo). Generalmente, si reduces el `learning_rate`, debes aumentar `n_estimators`.
* **Rango:** `Entero > 0`. Típico: `100 - 5000`.

**`max_depth`**:  
Profundidad máxima de cada árbol.  
* **Significancia:** Controla la complejidad del modelo. Árboles profundos pueden capturar relaciones muy específicas y patrones de alto orden, pero memorizan el ruido (overfitting). Árboles poco profundos (stumps) son buenos para capturar tendencias lineales simples.
* **Rango:** `Entero > 0`. Típico: `3 - 10`.

**`min_child_weight`**:  
Define la suma mínima de peso de instancias (Hessian) necesaria en un nodo hijo (hoja).  
* **Significancia:** Es fundamental para controlar el overfitting. Si el paso de partición del árbol resulta en un nodo hoja con una suma de pesos menor que este valor, el proceso de construcción se detendrá. En términos simples: evita que el modelo cree reglas para grupos de datos muy pequeños o insignificantes. Cuanto mayor sea el valor, más conservador es el modelo.
* **Rango:** `[0, ∞]`. Típico: `1 - 10`.

**`gamma` (min_split_loss)**:  
Reducción mínima de la función de pérdida requerida para realizar una partición adicional en un nodo hoja.  
* **Significancia:** Actúa como un parámetro de pseudo-regularización. A diferencia de otros algoritmos que podan el árbol después de construirlo, XGBoost usa `gamma` para no crecer el árbol si la ganancia no es sustancial. Valores altos hacen el algoritmo muy conservador.
* **Rango:** `[0, ∞]`. Típico: `0 - 5`.

---

### 2. Estocasticidad (Muestreo Aleatorio)

**`subsample`**:  
Fracción de observaciones (filas) a muestrear aleatoriamente para cada árbol.  
* **Significancia:** Previene el overfitting al hacer que cada árbol vea un subconjunto diferente de los datos. Si se establece en 0.5, XGBoost recolectará aleatoriamente la mitad de los datos para crecer los árboles.
* **Rango:** `(0, 1]`. Típico: `0.5 - 0.9`.

**`colsample_bytree`**:  
Fracción de columnas (features) a muestrear aleatoriamente para cada árbol.  
* **Significancia:** Similar a "Random Forest". Útil cuando tienes muchas características o algunas características dominantes que opacan a las demás. Obliga al modelo a considerar variables menos potentes.
* **Rango:** `(0, 1]`. Típico: `0.5 - 0.9`.

---

### 3. Regularización Avanzada

**`reg_alpha` (alpha)**:  
Término de regularización L1 en los pesos.  
* **Significancia:** Promueve la "esparcidad" (sparsity). Esto significa que fuerza los pesos de las características menos importantes a ser exactamente cero. Es útil para realizar selección de características (feature selection) implícita en datasets con mucho ruido o alta dimensionalidad.
* **Rango:** `[0, ∞]`. Típico: `0 - 10`.

**`reg_lambda` (lambda)**:  
Término de regularización L2 en los pesos.  
* **Significancia:** Suaviza los pesos de las hojas, evitando que un solo nodo tenga una influencia desproporcionada. Ayuda a reducir el overfitting de manera más suave que L1. Es la regularización por defecto de XGBoost.
* **Rango:** `[0, ∞]`. Típico: `1 - 10`.

---

### 4. Manejo de Desbalance y Estabilidad

**`scale_pos_weight`**:  
Controla el balance de pesos entre clases positivas y negativas.  
* **Significancia:** Crítico para datasets desbalanceados. Un valor típico es `sum(negative instances) / sum(positive instances)`. Hace que el modelo penalice mucho más el error al clasificar mal la clase minoritaria (positiva).
* **Rango:** `> 0`.

**`max_delta_step`**:  
Restricción máxima en el paso de actualización de peso (delta) de cada hoja.  
* **Significancia:** Generalmente no es necesario, pero es vital en regresión logística con clases extremadamente desbalanceadas. Si el modelo es inestable o el gradiente explota, establecer esto en un valor finito (ej. 1-10) ayuda a la convergencia.
* **Rango:** `[0, ∞]`. Típico: `0 (sin límite)` o `1 - 10`.

---

### 5. Definición del Problema y Sistema

**`objective`**:  
Especifica la función de pérdida a minimizar.  
* **Significancia:** Define la naturaleza matemática del problema. Debe coincidir con tu variable objetivo (target). Usar la función incorrecta invalidará los resultados.
* **Valores:** `String`. Ejemplos: `binary:logistic` (Clasificación binaria, devuelve probabilidad), `reg:squarederror` (Regresión), `multi:softmax` (Multiclase).

**`eval_metric`**:  
Métrica de evaluación para datos de validación durante el entrenamiento.  
* **Significancia:** Permite monitorear el rendimiento real del modelo iteración tras iteración. Fundamental para usar "Early Stopping". Para datos desbalanceados, `error` es malo, `auc` o `logloss` son preferibles.
* **Valores:** `String` o `Lista`. Ejemplos: `auc`, `logloss`, `rmse`, `mae`, `error`.

**`tree_method`**:  
Algoritmo de construcción del árbol.  
* **Significancia:** Afecta drásticamente la velocidad de entrenamiento y el uso de memoria. Para datasets grandes (>100k filas), los métodos basados en histogramas son la norma.
* **Valores:** `String`. Ejemplos: `auto`, `exact`, `hist` (rápido en CPU), `gpu_hist` (rápido en GPU).

**`n_jobs`**:  
Número de hilos paralelos usados para correr XGBoost.  
* **Significancia:** Solo afecta la velocidad de cómputo, no el resultado del modelo.
* **Rango:** `Entero`. `-1` usa todos los núcleos disponibles.

**`random_state` (seed)**:  
Semilla para el generador de números aleatorios.  
* **Significancia:** Garantiza la reproducibilidad. Mismos datos + mismo parámetro = mismo resultado exacto.
* **Rango:** `Entero`.

---

# Diccionario de Parámetros y Métricas para LightGBM

Este documento describe las métricas de evaluación y los hiperparámetros comunes utilizados en los modelos LightGBM, basándose en el contexto de tu notebook.

---

## Métricas de Evaluación

Estas son métricas que se calculan después de entrenar el modelo para medir su rendimiento. No son parámetros que se configuran antes del entrenamiento.

### `ROC-AUC`
*   **Qué es**: Una métrica de rendimiento para problemas de clasificación. Significa "Área Bajo la Curva de Característica Operativa del Receptor".
*   **Qué hace**: Mide la capacidad del modelo para distinguir entre las clases positiva y negativa. Un valor de 1.0 indica un clasificador perfecto, mientras que un valor de 0.5 sugiere un rendimiento no mejor que el azar.
*   **Valores**: Un número flotante entre 0.0 y 1.0.

### `Precision (1)`
*   **Qué es**: Una métrica que mide la exactitud de las predicciones positivas.
*   **Qué hace**: Responde a la pregunta: "De todas las veces que el modelo predijo la clase 1 (positiva), ¿qué porcentaje fue correcto?". Se calcula como `Verdaderos Positivos / (Verdaderos Positivos + Falsos Positivos)`.
*   **Valores**: Un número flotante entre 0.0 y 1.0.

### `Recall (1)`
*   **Qué es**: Una métrica que mide la completitud de las predicciones positivas. También se conoce como "Sensibilidad".
*   **Qué hace**: Responde a la pregunta: "De todos los casos que eran realmente de la clase 1, ¿qué porcentaje detectó correctamente el modelo?". Se calcula como `Verdaderos Positivos / (Verdaderos Positivos + Falsos Negativos)`.
*   **Valores**: Un número flotante entre 0.0 y 1.0.

### `F1-Score (1)`
*   **Qué es**: La media armónica de `Precision` y `Recall`.
*   **Qué hace**: Proporciona un balance entre la precisión y el recall. Es útil cuando se necesita un equilibrio entre identificar correctamente los casos positivos y no generar demasiados falsos positivos.
*   **Valores**: Un número flotante entre 0.0 y 1.0.

---

## Hiperparámetros del Modelo LightGBM

Estos son ajustes que se configuran *antes* de entrenar el modelo para controlar su comportamiento y rendimiento.

### `objective`
*   **Qué es**: El objetivo de aprendizaje.
*   **Qué hace**: Define la función de pérdida que el modelo intentará minimizar durante el entrenamiento. Esto le dice al modelo qué tipo de problema está resolviendo.
*   **Parámetros que acepta**:
    *   `'binary'`: Para clasificación binaria (dos clases).
    *   `'multiclass'`: Para clasificación multiclase.
    *   `'regression'`: Para problemas de regresión.

### `metric`
*   **Qué es**: La métrica de evaluación a monitorear.
*   **Qué hace**: Especifica qué métrica se usará para evaluar el rendimiento del modelo en el conjunto de validación durante el entrenamiento. Es crucial para técnicas como el `early stopping`.
*   **Parámetros que acepta**: `'auc'`, `'binary_logloss'`, `'f1'`, `'precision'`, `'recall'`, `'None'` (si no se desea una métrica específica aquí).

### `n_jobs`
*   **Qué es**: El número de hilos de CPU a utilizar.
*   **Qué hace**: Controla el paralelismo del entrenamiento.
*   **Parámetros que acepta**:
    *   Un número entero (ej. `4` para usar 4 hilos).
    *   `-1`: Para usar todos los hilos de CPU disponibles.

### `verbosity`
*   **Qué es**: El nivel de detalle de los mensajes impresos.
*   **Qué hace**: Controla cuánta información muestra LightGBM durante el entrenamiento.
*   **Parámetros que acepta**:
    *   `< 0` (ej. `-1`): Muestra solo errores fatales.
    *   `0`: Muestra errores y advertencias.
    *   `1`: Muestra información adicional.

### `random_state`
*   **Qué es**: La semilla para la generación de números aleatorios.
*   **Qué hace**: Asegura que los resultados del modelo sean reproducibles. Cualquier operación estocástica (como el `subsampling`) producirá los mismos resultados si se usa la misma semilla.
*   **Parámetros que acepta**: Un número entero (ej. `42`).

### `n_estimators`
*   **Qué es**: El número de árboles de decisión a construir.
*   **Qué hace**: Controla la cantidad de rondas de boosting. Un número mayor puede mejorar el rendimiento, pero también aumenta el riesgo de sobreajuste y el tiempo de entrenamiento.
*   **Parámetros que acepta**: Un número entero positivo (ej. `100`, `1000`).

### `learning_rate`
*   **Qué es**: La tasa de aprendizaje.
*   **Qué hace**: Reduce la contribución de cada árbol nuevo. Un valor más bajo requiere más `n_estimators` pero generalmente conduce a un modelo más robusto y preciso.
*   **Parámetros que acepta**: Un número flotante pequeño, típicamente entre `0.01` y `0.3`.

### `num_leaves`
*   **Qué es**: El número máximo de hojas en un árbol.
*   **Qué hace**: Es el principal parámetro para controlar la complejidad de un árbol individual. Un valor más alto permite al modelo aprender relaciones más complejas, pero aumenta el riesgo de sobreajuste.
*   **Parámetros que acepta**: Un número entero, debe ser menor que `2^max_depth`.

### `max_depth`
*   **Qué es**: La profundidad máxima de un árbol.
*   **Qué hace**: Limita la profundidad de cada árbol para evitar el sobreajuste. Un valor de `-1` significa sin límite.
*   **Parámetros que acepta**: Un número entero (ej. `5`, `10`) o `-1`.

### `subsample`
*   **Qué es**: La fracción de datos a usar para entrenar cada árbol.
*   **Qué hace**: LightGBM tomará una muestra aleatoria de las filas (sin reemplazo) antes de construir cada árbol. Esto ayuda a prevenir el sobreajuste.
*   **Parámetros que acepta**: Un número flotante entre `0.0` y `1.0` (ej. `0.8` para usar el 80% de los datos).

### `colsample_bytree`
*   **Qué es**: La fracción de características (columnas) a usar para entrenar cada árbol.
*   **Qué hace**: En cada iteración, se selecciona un subconjunto aleatorio de características. Ayuda a prevenir el sobreajuste y acelera el entrenamiento.
*   **Parámetros que acepta**: Un número flotante entre `0.0` y `1.0` (ej. `0.7` para usar el 70% de las columnas).

### `min_child_samples`
*   **Qué es**: El número mínimo de muestras de datos requeridas en una hoja.
*   **Qué hace**: Evita que el modelo cree divisiones que solo se aplican a muy pocos datos, lo que ayuda a controlar el sobreajuste.
*   **Parámetros que acepta**: Un número entero positivo (ej. `20`).

### `scale_pos_weight`
*   **Qué es**: El peso para la clase positiva.
*   **Qué hace**: Se utiliza en problemas con clases desbalanceadas. Aumenta el peso de la clase minoritaria (positiva) en la función de pérdida, haciendo que el modelo preste más atención a los errores en esa clase.
*   **Parámetros que acepta**: Un número flotante. Un valor común es `(número de muestras negativas) / (número de muestras positivas)`.

