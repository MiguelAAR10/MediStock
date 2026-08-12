# TCAD
## Protocolo de Alto Nivel para Desarrollo, Ejecucion y Documentacion de Agentes

## 1. Proposito

**TCAD** es un protocolo de trabajo de alto nivel para dirigir la ejecucion de un agente en cualquier tipo de proyecto.

Su objetivo no es solo resolver tareas, sino hacerlo con claridad estrategica, entendimiento del objetivo, respeto por el contexto, analisis previo, desarrollo modular, trazabilidad y minima friccion.

TCAD se aplica a software, backend, frontend, automatizaciones, IA/agentes, documentacion, procesos y mantenimiento.

---

## 2. Vision del Framework

TCAD significa:

- **T - Traduccion**
- **C - Contexto**
- **A - Analisis**
- **D - Desarrollo / Documentacion**

Flujo:

1. Entender lo que se quiere.
2. Entender donde se tocara.
3. Definir estrategia.
4. Ejecutar, validar y documentar.

---

## 3. Principios Fundamentales

1. Claridad antes que velocidad.
2. No asumir cuando falta precision.
3. El contexto manda.
4. Modularidad sobre intervencion agresiva.
5. Compatibilidad sobre complejidad innecesaria.
6. Trazabilidad obligatoria.
7. Comunicacion apta para no tecnicos.
8. Verificacion antes de cerrar.

---

## 4. Cuando invocar TCAD

Invocar TCAD en: nuevas solicitudes, mejoras, correcciones, refactorizaciones, integraciones, tareas de datos/IA/agentes, automatizaciones, arquitectura y documentacion.

---

## 5. Estructura Operativa

### Capa 1: Comprension
### Capa 2: Aterrizaje en sistema real
### Capa 3: Toma de decisiones
### Capa 4: Ejecucion trazable

Riesgos que reduce:

- Traduccion: objetivo equivocado.
- Contexto: ruptura del sistema.
- Analisis: mala estrategia.
- Desarrollo/Documentacion: cambios invisibles o incompletos.

---

## 6. Fase T - Traduccion

### Objetivo
Convertir solicitud ambigua en objetivo accionable.

### Debe responder

- Que se pide realmente.
- Cual es el problema de fondo.
- Cual es el resultado observable.
- Cual es el criterio de exito.

### Salida minima

- Objetivo claro.
- Alcance preliminar.
- Lectura tecnica y no tecnica.
- Ambiguedades detectadas.

### Formato recomendado

```md
## T - Traduccion

**Solicitud original:** ...
**Objetivo real interpretado:** ...
**Resultado esperado:** ...
**Lectura tecnica:** ...
**Lectura no tecnica:** ...
**Ambiguedades / supuestos:** ...
```

---

## 7. Fase C - Contexto

### Objetivo
Entender el entorno real para intervenir sin romper coherencia.

### Debe cubrir

- Contexto funcional.
- Contexto tecnico.
- Contexto visual.
- Contexto operativo.
- Contexto humano.

### Formato recomendado

```md
## C - Contexto

**Sistema / modulo impactado:** ...
**Estado actual:** ...
**Patrones existentes a respetar:** ...
**Dependencias relacionadas:** ...
**Restricciones:** ...
**Riesgos de romper algo:** ...
**Criterio de integracion:** ...
```

---

## 8. Fase A - Analisis

### Objetivo
Elegir la estrategia mas robusta, segura y mantenible.

### Evaluar

- Opciones posibles.
- Impacto tecnico/visual.
- Riesgo, reversibilidad, mantenibilidad.
- Compatibilidad con arquitectura actual.

### Formato recomendado

```md
## A - Analisis

**Problema a resolver:** ...
**Opciones evaluadas:** ...
**Estrategia elegida:** ...
**Por que esta estrategia es la mejor:** ...
**Riesgos:** ...
**Mitigaciones:** ...
**Plan de implementacion:** ...
**Validaciones necesarias:** ...
```

---

## 9. Fase D - Desarrollo / Documentacion

### Objetivo
Implementar, validar y dejar evidencia verificable.

### Debe incluir

- Cambios aplicados.
- Pruebas/validaciones.
- Bitacora con timestamp.
- Impacto esperado.
- Riesgos residuales.

### Formato recomendado

```md
## D - Desarrollo / Documentacion

**Timestamp:** YYYY-MM-DD HH:MM:SS
**Cambio realizado:** ...
**Archivos / areas impactadas:** ...
**Implementacion aplicada:** ...
**Validacion realizada:** ...
**Resultado:** ...
**Impacto:** ...
**Pendientes / riesgos residuales:** ...
```

---

## 10. Flujo Completo para Agentes

1. Recibir solicitud.
2. Traducir.
3. Levantar contexto.
4. Analizar.
5. Ejecutar.
6. Verificar.
7. Documentar.
8. Cerrar con claridad.

---

## 11. Modo Universal de Aplicacion

Aplicable en:

- software,
- disenio,
- procesos/automatizacion,
- IA/agentes,
- estrategia/documentacion.

---

## 12. Protocolos de Decision

1. Minima invasion.
2. Coherencia sistemica.
3. Legibilidad futura.
4. Justificacion tecnica.
5. Reversibilidad.
6. Validacion proporcional al riesgo.

---

## 13. Niveles de Riesgo

- **Bajo:** cambios localizados.
- **Medio:** cambios funcionales aislados.
- **Alto:** arquitectura, seguridad, datos sensibles, pagos, migraciones.

Politica: a mayor riesgo, mayor contexto, analisis, validacion y documentacion.

---

## 14. Artefactos Minimos

- Interpretacion del objetivo.
- Mapa de contexto.
- Estrategia de implementacion.
- Cambios realizados.
- Validaciones.
- Bitacora con timestamp.
- Pendientes/riesgos residuales.

---

## 15. Bitacora TCAD (Plantilla)

```md
## Bitacora TCAD

**Timestamp:** YYYY-MM-DD HH:MM:SS
**Tipo de tarea:** feature | fix | refactor | analisis | documentacion | diseno | automatizacion | agente
**Solicitud original:** ...
**Objetivo interpretado:** ...

### T - Traduccion
...

### C - Contexto
...

### A - Analisis
...

### D - Desarrollo / Documentacion
...

**Validacion realizada:** ...
**Resultado final:** ...
**Riesgos residuales:** ...
**Siguiente paso recomendado:** ...
```

Timestamp obligatorio: `YYYY-MM-DD HH:MM:SS`.

---

## 16. Checklist Operativo

- Traduccion correcta de la necesidad.
- Objetivo real entendido.
- Contexto revisado.
- Restricciones identificadas.
- Estrategia razonada.
- Ejecucion modular.
- Resultado verificado.
- Documentacion con timestamp.
- Impacto explicado en lenguaje claro.

---

## 17. Anti-Patrones a Evitar

- Codificar antes de entender.
- Cambiar una parte sin ver el sistema.
- Resolver tecnicamente sin resolver objetivo real.
- Sobredisenar soluciones simples.
- Romper patrones visuales/arquitectura.
- Cerrar sin trazabilidad ni validacion.

---

## 18. Version Ejecutiva

- **T:** traducir necesidad a objetivo claro.
- **C:** entender contexto completo.
- **A:** definir estrategia segura y mantenible.
- **D:** ejecutar, validar y documentar.

---

## 19. Prompt Maestro

```md
Aplica el framework TCAD para esta tarea.

T - Traduce la solicitud a un objetivo claro, tecnico y no tecnico.
C - Analiza el contexto completo antes de proponer cambios.
A - Define la estrategia mas segura, modular y mantenible.
D - Ejecuta, valida y documenta con bitacora y timestamp.

No asumas.
No rompas contexto existente.
No implementes antes de entender.
Explica decisiones con claridad.
Deja trazabilidad.
```

---

## 20. Declaracion de Uso Permanente

Desde este proyecto, **TCAD** se adopta como protocolo operativo permanente de ejecucion del agente.

Debe aplicarse como:

- marco de pensamiento,
- estructura de comunicacion,
- control de calidad,
- protocolo de ejecucion,
- protocolo de documentacion,
- criterio de integracion.

---

## 21. Sintesis Final

TCAD es disciplina operativa para que un agente entienda mejor, decida mejor, ejecute mejor, rompa menos y documente mejor.

Principio central:

> Antes de hacer, entender.  
> Antes de tocar, contextualizar.  
> Antes de ejecutar, analizar.  
> Despues de resolver, documentar.
