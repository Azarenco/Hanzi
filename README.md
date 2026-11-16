# Hànzì de Pablo 🀄

App de flashcards de chino mandarín para estudiar el vocabulario de **El Nuevo Libro de Chino Práctico** (libro 1) y del **HSK 3.0**. Tiene modos por lección, por nivel HSK y «a capón», filtro por tipo de palabra, modo ✍️ Escribir con orden de trazos y repaso espaciado.

## Qué hay aquí

| Archivo | Para qué sirve |
|---|---|
| `Vocabulario Chino.xlsx` | **La fuente de todo**: palabras, lecciones, niveles y tipos. La columna «ID (no tocar)» guarda el progreso. |
| `construir_app.py` | Convierte el Excel en la app. |
| `plantilla.html` | El diseño y el funcionamiento de la app. |
| `app/` | La app ya construida (`index.html`, trazos, librería de escritura e iconos). |
| `.github/workflows/publicar.yml` | Reconstruye y publica la app sola cada vez que subes cambios. |
| `INSTRUCCIONES_PARA_CLAUDE.md` | Lo que tiene que leer cualquier Claude para seguir actualizándola. |

## Añadir una lección

1. Pásale a Claude las fotos de la lección y te devolverá el `Vocabulario Chino.xlsx` actualizado.
2. En GitHub: **Add file → Upload files**, arrastra el Excel nuevo (sustituye al anterior) y pulsa **Commit changes**.
3. En un par de minutos la app ya está al día (puedes verlo en la pestaña **Actions**). Cierra y abre la app en el móvil.

Sin Claude también se puede: añade filas al Excel (deja el ID vacío y en «Lección» pon `Libro 1 · Lección N`) y súbelo.

⚠️ No cambies el carácter ni el significado de una palabra que ya estás estudiando: eso cambia su ID y la tarjeta pierde el progreso. Corregir el pinyin, el nivel o el tipo no le afecta.

## Tu progreso

Se guarda en el navegador del móvil. Haz una copia de vez en cuando en **💾 Copia de seguridad de tu progreso → Copiar mi progreso** y guárdala en una nota o en tu Drive. Para recuperarla, pégala en el mismo sitio y pulsa **Importar** dos veces.
