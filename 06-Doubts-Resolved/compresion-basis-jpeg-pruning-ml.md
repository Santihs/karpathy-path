---
tags: [phase-0, linear-algebra, coding-the-matrix, compression, sparsity, ml-connection]
date_resolved: 2026-07-17
---

# La compresión con "coordenadas + poda" de Klein Cap 5 = JPEG y pruning de redes neuronales

Klein plantea 3 estrategias de compresión de imágenes (Cap 5.2) que resultan ser, sin nombrarlas así, la misma idea detrás de dos técnicas reales muy usadas en ML/software.

## Strategy 1 (podar valores directo) ≈ magnitude pruning en redes neuronales

Podar las entradas de menor magnitud de un vector (quedarte con las k más grandes) es exactamente **magnitude-based weight pruning**: se rankean los pesos de una red por valor absoluto y se ponen en cero los de menor magnitud, asumiendo que aportan poco a la salida. Se usa desde los 90s, hoy con variantes iterativas (podar + reentrenar) para no perder precisión.

## Strategy 3 (podar coordenadas en una buena base) ≈ JPEG / DCT

Podar directo los píxeles arruina la imagen (Strategy 1 en Klein daba manchas). JPEG resuelve esto igual que Strategy 3 de Klein: transforma la imagen a una base donde la información queda concentrada en pocos coeficientes grandes (Discrete Cosine Transform, pariente de Fourier), poda los coeficientes chicos, y reconstruye. La DCT concentra la "energía" de la señal en pocos coeficientes por bloque — de ahí que podar ahí (no en píxeles crudos) preserve mucho más la imagen.

**El patrón general:** elegir una base donde la señal es *sparse* (poca info concentrada en pocos números grandes) hace que podar sea casi gratis. Elegir mal la base (como los píxeles crudos) hace que podar destruya todo. Esto conecta directo con Klein Question 5.2.4/5.2.5 — la elección de generadores (basis) es lo que determina si la compresión funciona.

## Fuentes
- [Magnitude-Based Weight Pruning — Emergent Mind](https://www.emergentmind.com/topics/magnitude-based-weight-pruning)
- [The State of Sparsity in Deep Neural Networks (arXiv)](https://arxiv.org/pdf/1902.09574)
- [JPEG DCT Coefficients Overview — Emergent Mind](https://www.emergentmind.com/topics/jpeg-discrete-cosine-transform-dct-coefficients)
