# Backlog / bloqueos — Prospector CRO

## 1. Destrabar Grupo F (corrida real completa)

- **Estado:** pausado, esperando dos cambios que solo vos podés hacer (no son de código).
- **Bloqueo 1 — Ahrefs, plan insuficiente:** `site-explorer-metrics` (tráfico) y `site-audit-issues` (problemas técnicos) devuelven "Insufficient plan" con la cuenta conectada. Solo funciona el Domain Rating gratis (`public-domain-rating-free`).
  **Acción:** revisar en tu cuenta de Ahrefs qué plan hace falta para Site Explorer + Site Audit vía API, y si conviene subir de plan.
- **Bloqueo 2 — Red del entorno bloquea el scraping propio:** el entorno cloud usado en esta sesión tiene **Network access = Trusted** (solo dominios de paquetes/APIs conocidos). Los sitios de las empresas devuelven 403 desde el proxy.
  **Acción:** en `claude.ai/code`, editar el entorno usado por esta sesión/rutina y cambiar **Network access** a **Full**. No alcanza con "Custom + dominios puntuales" porque los sitios a scrapear se descubren en el momento, no se conocen de antemano.
- **Cuando ambos estén resueltos:** avisame y retomamos F2/F3 (revisar la tabla y JSON reales, confirmar los criterios de aceptación del spec) antes de generar los borradores de Gmail.

## 2. Corrida de prueba ya hecha (referencia)

Lote `20260714-212421-abb2af` — mercado ecommerce, país Argentina, 11-50 empleados. 3 empresas reales de Apollo (EcomExperts, Sell, Ukelele), Domain Rating real de Ahrefs. JSON guardados en `data/` (no versionado, es local a esta sesión). Sirvió para encontrar y corregir el bug de `null` vs `False` en el scoring (ver `specs/v1/tasks.md`, sección F).
