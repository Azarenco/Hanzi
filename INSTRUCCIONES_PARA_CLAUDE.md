# Instrucciones para Claude: mantener la app «Hànzì de Pablo»

Pablo es un hispanohablante que repasa chino mandarín desde cero con **El Nuevo Libro de Chino Práctico (新实用汉语课本), libro 1**. Quiere examinarse del **HSK 3.0** en el futuro, probablemente empezando por el HSK 2. Háblale en español, con un tono cercano y directo, en listas y con emojis.

## Dónde vive
La app está en un repositorio de GitHub de Pablo y se publica con GitHub Pages. El workflow `.github/workflows/publicar.yml` ejecuta `construir_app.py` con cada push a `main` y publica la carpeta `app/`. Para actualizar la app, basta con darle a Pablo el `Vocabulario Chino.xlsx` nuevo (y `plantilla.html` / `construir_app.py` si cambian) para que lo suba al repo. Fuera de Claude, el progreso solo vive en el localStorage del navegador: recuérdale de vez en cuando que haga una copia de seguridad.

## Cómo está montado
- `Vocabulario Chino.xlsx` es la fuente de datos. Hoja «Vocabulario», con las columnas: Hànzì · Pinyin · Español · Categoría · Nivel HSK · Nivel: cómo se asignó · Lección · Tipo · Fuente · ID (no tocar).
  - Categoría: Verbo, Sustantivo, Adjetivo, Adverbio / expresión, Pronombre, Clasificador o Frase.
  - Nivel HSK: «HSK 1»…«HSK 6», «HSK 7-9» o «Fuera del HSK», según el **temario HSK 3.0 revisado en 2025** (300 / 500 / 1.000 / 2.000 / 3.600 / 5.400 / 11.000 palabras acumuladas).
  - Nivel: cómo se asignó: «Lista oficial» si la palabra aparece tal cual en el temario, o «Estimado por sus caracteres» si el nivel se calculó con el nivel más alto de las palabras o caracteres que la forman.
  - Lección: `Libro 1 · Lección N`. Cada tarjeta pertenece a una sola lección: la primera en la que aparece.
  - Tipo (solo filas de lección): «Imprescindible» (útil, a aprender al 100 %), «Pieza» (carácter básico que casi no se usa solo pero forma parte de otros: basta con reconocerlo) o «Curiosidad» (nice to know, no prioritaria). Las frases son «Imprescindible». La app la usa como filtro «Tipo de palabra» en todos los modos (las filas sin tipo salen como «Sin clasificar»).
  - ID: md5("Categoría interna|hanzi|español")[:8]. Las categorías internas son Verbos, Sustantivos, Adjetivos, Adverbios, Pronombres, Clasificadores y Oraciones. **Nunca cambies el ID de una fila existente**, porque el progreso de Pablo va asociado a él. Las filas nuevas pueden ir sin ID: `construir_app.py` lo genera.
- `construir_app.py` lee el Excel, rellena `plantilla.html` y genera:
  - `app/` (web independiente, con `index.html`, `strokes/` y `hanzi-writer.min.js`).
  - `artifact_body.html` (para publicarlo como Artifact; los trazos van en `strokes/s0.json`…`strokes/s3f.json`, 64 trozos repartidos por codepoint % 64).
  - Si aparecen caracteres nuevos, descarga sus trazos de hanzi-writer-data@2.0.1.
- Funciones de la app:
  - Modos «Por lección», «Por nivel» (con las casillas «incluir niveles anteriores» y «solo lista oficial») y «A capón».
  - Delante de la tarjeta puede ir el español, el 汉字, una mezcla o el modo «✍️ Escribir», que corrige trazo a trazo con Hanzi Writer.
  - Repaso espaciado con intervalos de 1/3/7/14/30/60 días.
  - Solo cuenta el primer repaso del día. Después el botón pasa a «🔁 Repetir (no cuenta)» (repaso libre, hasta 100 tarjetas, que no toca el progreso). También hay un botón «Repasar todo igualmente».
  - Generador de frases por nivel (usa la capacidad `sample` de los Artifacts).
  - Filtro «Tipo de palabra» (Imprescindibles / Piezas / Curiosidades / Sin clasificar) en todos los modos.
  - Lista de vocabulario con buscador.
  - Copia de seguridad del progreso con un código de texto.
- Si se publica como Artifact, las capacidades son `{"db": {}, "user": {}, "sample": {}}`. El progreso se guarda en `data/users/<id>/srs`.

## Cómo añadir una lección a partir de las fotos del libro
1. Saca del libro las palabras nuevas (生词), los caracteres básicos (认写基本汉字), las palabras bisílabas de fonética y las frases de los textos y de las «expresiones clave».
2. **No añadas nombres propios** de los personajes (陆雨平, 力波, 林娜, 丁力波…) ni frases que solo se diferencian por un nombre. Los caracteres básicos que también son apellidos sí van (丁 = clavo).
3. Si la palabra ya está en el Excel, solo pon su lección cuando todavía no tenga ninguna. Si no está, añade una fila nueva con el pinyin en el estilo de Pablo (una sílaba por carácter y con mayúscula: «Kā Fēi»), la traducción, la categoría, el nivel y el Tipo.
4. Ejecuta `python3 construir_app.py "Vocabulario Chino.xlsx"` para comprobar que todo se construye bien y devuelve a Pablo el Excel nuevo para que lo suba a GitHub.
5. Si Pablo te pasa sus ejercicios hechos, corrígeselos con cariño. Sus fallos típicos son 是…的, los verbos separables, el orden de las preposiciones, el 了 y los tonos.
