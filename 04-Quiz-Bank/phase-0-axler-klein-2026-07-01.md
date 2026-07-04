---
tags: [phase-0, linear-algebra, subspaces, bases, dimension, linear-maps, functions, probability, vectors, axler, coding-the-matrix]
date_added: 2026-07-01
last_tested: 2026-07-03
---

Q: ¿Cuáles son las 3 condiciones pa que un subconjunto U de V sea subespacio? (Axler 1.34)
A: (1) 0 ∈ U, (2) cerrado bajo suma (u,w∈U ⟹ u+w∈U), (3) cerrado bajo escalar (a∈F, u∈U ⟹ au∈U).

---

Q: ¿Es {(x,y,z)∈R³ : x+y+z=5} subespacio? ¿Por qué?
A: No. El vector cero no cumple la ecuación (0+0+0=0≠5) — falla la condición de identidad aditiva. Ecuación no-homogénea rompe subespacialidad.

---

Q: Dos vectores v,w son linealmente independientes. ¿Qué significa exactamente? (Axler 2.16d)
A: Ninguno de los dos es múltiplo escalar del otro — no apuntan en la misma dirección/línea.

---

Q: (1,2,-4) y (7,-5,6) son independientes en R³ pero NO son base de R³. ¿Por qué no?
A: Con solo 2 vectores, el span máximo es un plano (2D) — no alcanza a cubrir las 3 dimensiones de R³, sin importar cuán independientes sean.

---

Q: ¿Qué 2 condiciones tiene que cumplir una lista pa ser "base" de un espacio vectorial? (Axler 2.26)
A: (1) Ser linealmente independiente Y (2) hacer span del espacio completo. Las dos son obligatorias.

---

Q: ¿Por qué "dimensión" es un concepto válido y no ambiguo? (Axler 2.34)
A: Porque se prueba primero que CUALQUIER base del mismo espacio tiene el mismo largo — recién con eso garantizado se define dim V = largo de cualquier base.

---

Q: Si U es subespacio de V y dim U = dim V, ¿qué se puede concluir? (Axler 2.39)
A: U = V exactamente. Un subespacio propio siempre tiene dimensión estrictamente menor — no existe "casi todo el espacio".

---

Q: T(x,y,z) = (2x-4y+3z+b, 6x+cxyz). ¿Bajo qué condición es T lineal?
A: b=0 y c=0. b≠0 rompe T(0)=0 (traslación); c≠0 rompe homogeneidad (término cúbico no escala linealmente).

---

Q: ¿Qué es una función, en términos de dict/hashmap?
A: Un conjunto de pares (a,b) donde ningún par comparte la misma primera entrada — igual que un dict sin keys duplicadas. Dominio = conjunto de keys válidas.

---

Q: ¿Qué significa que f y g sean inversos funcionales? (Definición 0.3.13)
A: f∘g es la identidad en el dominio de g, Y g∘f es la identidad en el dominio de f — las DOS direcciones tienen que cumplirse.

---

Q: ¿Por qué una función que manda dos inputs distintos al mismo output NO es invertible?
A: Porque el inverso no podría "deshacer" sin ambigüedad — al ver ese output compartido, no sabría cuál de los dos inputs originales devolver.

---

Q: Si aplicás una función INVERTIBLE a un input con distribución uniforme, ¿qué distribución tiene el output? ¿Por qué?
A: También uniforme. Cada output tiene exactamente un input que lo produce (invertible = biyectiva), así que la probabilidad se traslada 1-a-1 sin sumar ni redistribuir.

---

Q: Un vector de n entradas — ¿cómo se interpreta como función? (Klein 2.2)
A: Es una función con dominio {0,1,...,n-1} (los índices) y codominio F (los valores) — cada índice mapea a su entrada correspondiente.

---

Q: Da 3 ejemplos de cosas que se pueden representar como vectores, además de "flechas geométricas".
A: Cualquiera de: binary string (key criptográfica), attributes (fila de dataset/features), imagen (píxel→intensidad), distribución de probabilidad, estado de un sistema evolucionando.

---

Q: ¿Por qué la suma de vectores es automáticamente asociativa y conmutativa, sin necesidad de probarlo aparte?
A: Porque se define entrada-por-entrada, y la suma en el campo subyacente (R, C, GF(2)) ya es asociativa y conmutativa — la propiedad se hereda directo.

---

Q: 2[1,2,3] + [10,20,30] — ¿cuál es la precedencia de operadores acá, y cuál es el resultado?
A: Escalar-vector multiplicación tiene precedencia sobre suma (igual que multiplicación sobre suma en aritmética normal). Resultado: [2,4,6]+[10,20,30] = [12,24,36].

---

Q: ¿Qué es una "combinación convexa" de dos vectores u, v? (Klein 2.6.3)
A: Una expresión αu+βv donde α,β≥0 y α+β=1 — parametriza cualquier punto del segmento entre u y v, ponderando cuánto pesa cada extremo.

---

Q: En el ejemplo de las caras promediadas (Example 2.6.10), ¿qué representa (1/2)u + (1/2)v?
A: El promedio pixel-a-pixel de las dos imágenes — una tercera "cara" a mitad de camino entre las dos, mezclando rasgos de ambas.

---

Q: Nombra 2 lugares en ML/dev donde reaparece la combinación convexa.
A: Cualquiera de: mixup (data augmentation, λx1+(1-λ)x2), lerp (interpolación lineal en gráficos), softmax/attention weights (pesos no-negativos que suman 1).
