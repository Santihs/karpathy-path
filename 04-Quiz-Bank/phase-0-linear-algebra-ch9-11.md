---
tags: [phase-0, linear-algebra, dot-product, duality, cross-product]
date_added: 2026-06-29
last_tested: null
---

Q: ¿Qué tipo de resultado produce el producto punto? ¿Y el producto cruz?
A: Producto punto → escalar (un número). Producto cruz → vector (perpendicular a los dos de entrada). Esta diferencia es fundamental.

---

Q: ¿Qué significa geométricamente que v·w = 0?
A: Los vectores son perpendiculares (ortogonales) — no comparten ninguna dirección. Ángulo entre ellos = 90°.

---

Q: Dado v = [2, 0] y w = [1, 1], ¿cuánto de w va en la dirección de v?
A: comp = (v·w) / |v| = (2×1 + 0×1) / 2 = 1. La "sombra" de w sobre v tiene longitud 1.

---

Q: ¿Por qué en attention de transformers se usan productos punto?
A: Cada producto punto Q·Kᵀ mide cuánto "apunta" una query en la dirección de una key — es similitud direccional. Alto producto punto = alta relevancia.

---

Q: Explica dualidad en una oración.
A: Cualquier transformación lineal nD→1D puede escribirse como producto punto con un vector en nD — proyectar y transformar son la misma operación.

---

Q: Si û = [0.8, 0.6] y lo uso como transformación 2D→1D, ¿dónde aterrizan î y ĵ?
A: î aterriza en 0.8 (coordenada x de û), ĵ aterriza en 0.6 (coordenada y de û). Las coordenadas de û son exactamente los landing points.

---

Q: ¿Para qué dimensiones está definido el producto cruz?
A: Solo en 3D (y matemáticamente en 7D, pero ignorar). El producto punto funciona en cualquier dimensión.

---

Q: ¿Qué representa geométricamente |v × w|?
A: El área del paralelogramo formado por v y w. Igual que |v||w|sin(θ).

---

Q: Conexión entre producto cruz y dualidad: ¿cómo se deriva v × w usando dualidad?
A: Define f(p) = det([p, v, w]) — función lineal 3D→1D. Por dualidad, existe un vector dual q tal que f(p) = q·p. Ese vector q es exactamente v×w. El producto cruz es el dual de la función volumen.

---

Q: Una red neuronal tiene embeddings de 512 dimensiones. ¿Cómo uses dot product para medir similitud entre dos embeddings?
A: Normaliza ambos (hazlos unitarios), luego dot product = cos(θ). Resultado cercano a 1 = similares. Cercano a 0 = independientes. Cercano a -1 = opuestos. Cosine similarity = (v·w) / (|v| × |w|).
