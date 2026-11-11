# Comunica+

**Plataforma de Comunicación Aumentativa y Alternativa (AAC)** para ayudar a niños, niñas y adolescentes a comunicarse y a aprender a hablar tocando imágenes que representan palabras.

Aplicación web instalable (PWA) que funciona sin conexión una vez instalada y guarda todos los datos en el propio dispositivo.

**Versión actual:** `v2026.10.31-1`

---

## ¿Qué hace?

- **Tablero de comunicación:** cada imagen tocada se agrega a la frase y se pronuncia en voz alta. Con varias imágenes se arman frases completas.
- **Perfiles múltiples:** uno por cada niño o niña, con su vocabulario, su voz y su progreso.
- **Voz real grabada:** se puede grabar al niño diciendo cada palabra; la app reproduce esa grabación en lugar de la voz sintética.
- **Ayuda rápida:** pantalla de botones grandes para lo urgente (ayuda, dolor, baño, agua, comida, miedo, cansancio, frío, calor).
- **Mascota:** compañera animada en el estilo *Infantil*, que llama al niño por su nombre y festeja los aciertos.
- **Niveles de estímulo:** modos *Calmado*, *Normal* y *Alto* para ajustar efectos, vibración y movimiento.
- **Ocho juegos de "Aprender a hablar":** escuchar y elegir, leer y elegir, repetir en voz alta, armar la frase, rompecabezas, globos, memotest e historias.
- **Acceso por switch:** escaneo automático de botones para quienes no pueden tocar con precisión, con selección por pantalla, botón grande o teclado.
- **Logros y reporte:** logros desbloqueables y un reporte imprimible o exportable a PDF para terapia y escuela.
- **Copia de seguridad:** exportación y restauración completa del perfil, incluida una copia solo de voces.

## Privacidad

Los perfiles, el progreso y las grabaciones de voz **no se suben a ningún servidor**: quedan únicamente en el dispositivo donde se usa la aplicación. Solo salen de allí si se exporta una copia de seguridad y se comparte manualmente.

## Instalación

1. Abrir el enlace de la aplicación (GitHub Pages, `...github.io/...`) en Chrome desde el celular o la tablet.
2. Abrir el menú de tres puntos (⋮).
3. Elegir **"Instalar aplicación"** o **"Añadir a la pantalla de inicio"**.

La primera apertura requiere internet para cargar todos los recursos. Después funciona sin conexión para el uso diario.

## Estructura del repositorio

| Archivo | Descripción |
| --- | --- |
| `index.html` | Aplicación completa: interfaz, lógica, juegos, perfiles y almacenamiento (IndexedDB). |
| `manifest.json` | Manifiesto PWA: nombre, colores, orientación e íconos. |
| `sw.js` | Service worker con estrategia *red primero* y respaldo en caché para uso offline. |
| `icon-192.png`, `icon-512.png`, `icon-512-maskable.png` | Íconos de la aplicación. |
| `Guia-de-Comunica.md` | Guía de uso para familias y cuidadores. |
| `Guia de uso Comunica.docx` | Misma guía en formato Word. |

## Detalles técnicos

- **Sin dependencias ni build:** un único `index.html` con HTML, CSS y JavaScript embebidos. Se sirve directamente como sitio estático.
- **Almacenamiento:** IndexedDB en el navegador del dispositivo.
- **Síntesis de voz:** Web Speech API (`speechSynthesis`).
- **Reconocimiento de voz:** Web Speech API (`SpeechRecognition`), cuando el navegador lo permite.
- **Actualizaciones:** el service worker usa *red primero* para el mismo origen, de modo que una versión nueva publicada se descarga al volver a abrir la app con internet. Si no hay conexión, sirve la última copia en caché.

## Publicación

El repositorio se publica como sitio estático en GitHub Pages. Para publicar una actualización basta con subir los archivos modificados; los dispositivos la reciben al reabrir la aplicación con conexión (puede ser necesario cerrarla por completo y volver a abrirla).

## Documentación para usuarios

La [Guía de Comunica+](Guia-de-Comunica.md) explica paso a paso, sin tecnicismos, cómo instalar la aplicación, crear perfiles, usar el tablero, grabar voces, configurar los juegos y el acceso por switch, y hacer copias de seguridad.

## Limitaciones conocidas

- El acceso por switch todavía no se probó con un pulsador físico real; conviene probarlo antes con el teclado o tocando la pantalla.
- El reporte muestra el total acumulado hasta la fecha, no la evolución semana a semana.
- Los datos no se sincronizan entre dispositivos: para cambiar de celular hay que exportar y restaurar una copia de seguridad.
