---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
self-explain: true
noteId: 1786916857185
---
Explicá cómo random variables se pueden tratar como vectores con inner product = covarianza, qué es la "norma" en ese espacio, y por qué la correlación es literal el coseno del ángulo entre 2 variables.

---

Se define <X,Y> := Cov[x,y] (para variables de media cero) — cumple las propiedades de un inner product real (simétrico, positive definite, lineal). La "norma" de una variable es ||X|| = sqrt(Cov[x,x]) = sqrt(V[x]) = sigma(x) — la standard deviation ES la norma en este espacio abstracto.

El ángulo entre 2 variables: cos(theta) = <X,Y> / (||X|| ||Y||) = Cov[x,y] / sqrt(V[x]V[y]) — esa fórmula ES exactamente la correlación. Por eso: correlación = coseno del ángulo entre las variables vistas como vectores. Ortogonalidad (cos=0) equivale a Cov[x,y]=0, es decir no correlacionadas — y si no correlacionadas, V[x+y]=V[x]+V[y] es literal el teorema de Pitágoras (c^2=a^2+b^2) con las std devs como catetos/hipotenusa.

Ref: `02-Topics/Probability-Fundamentals.md — 17. Inner products de random variables`
