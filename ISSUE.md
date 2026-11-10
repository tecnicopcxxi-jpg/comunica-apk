## Resumen

Encontré seis problemas de accesibilidad en `index.html` (`v2026.10.31-1`, 5938 líneas, blob `de71d41c`). Todo lo que sigue sale de leer el código y de calcular el ratio de contraste según WCAG 2.x. **No** hice prueba con lector de pantalla real ni con usuarios: el impacto está medido, no observado.

Los agrupo en un solo issue como lista de trabajo porque la app es de Comunicación Aumentativa y Alternativa: varios de estos fallos no degradan la estética, interrumpen el uso.

## Por qué acá la severidad es distinta

Quien usa la app puede tener además baja visión, dificultad motora fina, o comunicarse con lector de pantalla o con un switch. Eso vuelve críticas tres cosas que en otra app serían detalles: el contraste del texto (es la etiqueta de la palabra), el foco visible (es el mecanismo del switch) y el anuncio de la frase armada (es la salida del sistema).

## 1. Contraste insuficiente en 16 de 21 categorías — WCAG 1.4.3 (AA)

Cada categoría define un fondo `--cat-<x>` y una tinta `--cat-<x>-ink` (líneas 26-46), que se aplican al botón del pictograma en las líneas 4927, 4956 y 4972. El texto de la palabra va sobre ese fondo.

Medición con la fórmula de luminancia relativa, texto normal, mínimo AA **4.5:1**:

| Categoría | Fondo | Tinta actual | Ratio | Tinta propuesta | Ratio |
| --- | --- | --- | --- | --- | --- |
| `verb` (Acciones) | `#7BC24A` | blanco | **2.17** | `#111111` | 8.68 |
| `noun` (Necesidades) | `#F2913C` | blanco | **2.36** | `#111111` | 7.99 |
| `higiene` | `#3FB6AE` | blanco | **2.47** | `#111111` | 7.66 |
| `emo` (Emociones) | `#F2836B` | blanco | **2.55** | `#111111` | 7.40 |
| `desc` (Cómo es) | `#4DA6E8` | blanco | **2.65** | `#111111` | 7.14 |
| `comida` (Comidas) | `#E2865B` | blanco | **2.69** | `#111111` | 7.01 |
| `social` | `#E96FA0` | blanco | **2.90** | `#111111` | 6.52 |
| `dinero` | `#48A868` | blanco | **2.97** | `#111111` | 6.36 |
| `colores` | `#A97BDE` | blanco | **3.19** | `#111111` | 5.91 |
| `question` (Preguntas) | `#9C7FE0` | blanco | **3.22** | `#111111` | 5.87 |
| `aseo` | `#6E90C7` | blanco | **3.24** | `#111111` | 5.82 |
| `figuras` | `#7C8CA6` | blanco | **3.41** | `#111111` | 5.54 |
| `home` (Casa) | `#B5754A` | blanco | **3.74** | `#111111` | 5.04 |
| `transporte` | `#2E8B8B` | blanco | **4.05** | `#111111` | 4.66 |
| `salud` | `#C0576E` | blanco | **4.35** | requiere ajuste de fondo | 4.52 |
| `school` (Escuela) | `#5B6EE1` | blanco | **4.41** | requiere ajuste de fondo | 4.53 |

Ya pasan con la tinta actual: `people` 6.79, `vestirse` 5.34, `trabajo` 5.20, `church` 5.10, `dolor` 5.04.

`school` (4.41) y `salud` (4.35) están en una zona muerta: ni blanco ni un oscuro llegan a 4.5. Oscurecer el fondo apenas 1-2% alcanza (`#5A6CDE` da 4.53 con blanco; `#BC556B` da 4.52).

Por qué importa: el texto es la etiqueta de la palabra y el color es la pista de categoría. Cuando el par fondo/tinta se funde, el usuario pierde las dos cosas a la vez, y el color deja de servir para navegar.

Detalle: `body[data-style="adulto"]` redefine los fondos (líneas 241-243) pero solo declara `--cat-vestirse-ink`; el resto hereda blanco del `:root`. En ese estilo fallan `people` 2.69, `noun` 4.42 y `comida` 4.32.

## 2. Zoom bloqueado — WCAG 1.4.4 (AA)

Línea 5:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1">
```

`maximum-scale=1` impide llegar al 200% que pide el criterio y, en iOS Safari, desactiva el pinch-zoom. No hay alternativa: los tamaños del tablero están en `px`. Para alguien con baja visión es un bloqueo duro, y se arregla sacando ese atributo.

## 3. La frase armada no se anuncia — WCAG 4.1.3 (AA)

El contenedor de la frase se crea en la línea 4838 (`class:'sentence-strip'`) y no tiene `aria-live`. En las 5938 líneas hay **0** apariciones de `aria-live`.

El usuario toca un pictograma, la frase se arma en pantalla y el lector de pantalla no dice nada. El núcleo del producto queda mudo para quien no ve la pantalla. A mi criterio es el más grave de la lista.

## 4. Pestañas sin estado accesible — WCAG 4.1.2 (A)

Línea 4957: las pestañas se crean como `<button>` con `class:'tab-btn active'` y nada más. En todo el archivo hay **0** `role=`, `aria-selected` y `aria-pressed`.

El lector anuncia "Acciones, botón" sin indicar que está seleccionada. El estado existe solo en CSS. Si siguen siendo botones, corresponde `aria-pressed`; si se modelan como pestañas, `role="tab"` + `aria-selected`.

## 5. Foco visible eliminado — WCAG 2.4.7 (AA)

`outline:none` en las líneas 115 y 165, y **0** apariciones de `:focus-visible` en el archivo.

En una app que se opera con switch y teclado, el foco visible **es** el mecanismo de selección: el escaneo automático avanza por botones que el usuario no puede ver resaltados. No es un detalle de teclado.

## 6. Nombres accesibles inconsistentes — WCAG 4.1.2 (A) y 1.1.1 (A)

En 5938 líneas hay 5 `aria-label` y 1 `alt`. Los cuatro nombres existentes están todos en inputs de búsqueda (2754, 3074, 3590, 4895) y el botón de limpiar (4897) sí tiene `aria-label`.

El badge de voz (4985) usa `title:'Grabar voz propia'` sin `aria-label`. `title` no es un nombre accesible confiable en móvil. Es la misma app resolviendo el mismo problema de dos formas distintas: falta un criterio escrito, no es azar.

## Cómo reproducir

```bash
grep -n 'maximum-scale' index.html
grep -c 'aria-live' index.html
grep -c ':focus-visible' index.html
grep -n 'outline:none' index.html
grep -n "class:'tab-btn" index.html
grep -n 'voice-badge' index.html
grep -n -- '--cat-' index.html | head -22
```

## Propuesta de trabajo

Dos PRs chicos, en este orden, para que cada uno se pueda revisar solo:

1. `fix/a11y-zoom-contrast`: línea 5 y paleta de categorías. Mantendría los fondos (ya funcionan como código de color aprendido) y elegiría la tinta por categoría según la tabla de arriba, con un solo token oscuro (`#111111`) en lugar de 16 valores a mano.
2. `fix/a11y-focus-aria`: `:focus-visible` global, `aria-live` en la franja de frase, estado en las pestañas y `aria-label` en los botones que hoy solo tienen emoji.

## Fuera de alcance de este issue

`Guia-de-Comunica.md` dice `v2026.10.01-1` mientras `index.html` dice `v2026.10.31-1` (línea 791). Es desfase de documentación, no accesibilidad; lo dejo anotado por si conviene corregirlo aparte.
