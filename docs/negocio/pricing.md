# Plan de pricing — Stellae.ai

> Modelo de precios por tipo de cliente. Se vende **valor de negocio** (palancas de revenue),
> no "el mejor forecast". Cifras en € derivadas de la disposición a pagar real del mercado
> español (ver §6). Complementa a `universo-clientes.md`.

---

## 1. Arquitectura de producto (3 piezas)

El producto no es "una plataforma": son tres piezas que se combinan según el cliente.

| Pieza | Qué es | Naturaleza |
|---|---|---|
| **A · Plataforma** | Acceso al mapa de flujos y a la previsión de afluencia de su zona (SaaS). | Recurrente (suscripción) |
| **B · Informe trimestral "5 acciones"** | Documento cada quarter con **5 acciones concretas** de revenue para ese negocio, leídas de sus flujos. **Es el corazón de la consultoría.** | Recurrente (4/año) |
| **C · Engagement puntual** | Proyecto: cruce de **la BBDD del propio cliente** con los flujos → palancas de revenue; o estudio ad-hoc (p. ej. Año Santo 2027). | No recurrente (one-off) |

**Regla de oro:** A es el **gancho** (barato o gratis), B es el **negocio recurrente** (lo que
de verdad se vende), C es el **ticket alto** que aparece cuando el cliente ya confía.

---

## 2. Anclajes de mercado (de dónde salen los números)

- **Software de gestión pyme (PMS/channel manager):** **45–79 €/mes**; existen planes gratuitos
  (Amenitiz, Avirato). → Nuestra plataforma debe entrar **por debajo o al lado** de ese gasto,
  como complemento, no como coste nuevo grande. [S1]
- **Consultoría/marketing pyme España:** **60–150 €/h** puntual · **500–3.000 €/proyecto** ·
  **400–2.000 €/mes** retainer; agencias 1.500–4.000 €/mes de media. → Techo claro de lo que
  una pyme paga por "que alguien le diga qué hacer". [S2]
- **Sector público / grandes cuentas:** presupuestos de **decenas a cientos de millones**
  (Xunta 125,9 M€; SEGITTUR 130 M€; TT.OO. que facturan paquetes de miles de €). → El ticket
  institucional/enterprise no lo limita el presupuesto sino la confianza y la licitación. [S3]

---

## 3. Tarifas por tipo de cliente

> Precios de lista orientativos (excl. IVA). "Bundle anual" = A + 4×B con descuento.

### Pymes (S1 alojamiento · S2 restauración · S3 servicios · S4 retail)

| Plan | A · Plataforma | B · Informe trimestral | Bundle anual (A+4B) | Público objetivo |
|---|---|---|---|---|
| **Gancho (Free)** | Mapa básico de su zona, gratis | — | 0 € | Captación / long tail (S4) |
| **Basic** | **29 €/mes** | 150 €/informe | **~990 €/año** | Micro-negocio, 1 local |
| **Pro** | **59 €/mes** | incluido (4/año) | **~1.290 €/año** | Alojamiento/restauración estándar |
| **Multi-local** | **149 €/mes** | incluido + 1 revisión | **~2.900 €/año** | Mini-cadena, 2–5 locales |
| **Engagement C** | — | — | **500–1.500 €** one-off | Cruce de su BBDD (upsell) |

**ACV pyme típico: 900–1.500 €/año.** Coherente: cabe junto a los 45–79 €/mes del PMS y muy
por debajo del retainer de marketing (400–2.000 €/mes).

### Grandes cuentas (S5 · TT.OO., cadenas, Paradores, plataformas)

| Pieza | Precio | Nota |
|---|---|---|
| **A · Plataforma enterprise** | **500–1.500 €/mes** (o licencia anual 6k–18k €) | Multi-ruta, multi-establecimiento, API |
| **B · Informe trimestral premium** | **1.500–3.000 €/informe** | Con recomendaciones de cupos y pricing de paquete |
| **C · Engagement** | **5.000–20.000 €** | Cruce de su BBDD, apertura de nueva ruta, plan de temporada |

**ACV grande cuenta: 15.000–40.000 €/año.**

### Institucional / público (S6 · Xunta, DMOs, ayuntamientos, SEGITTUR)

| Pieza | Precio | Nota |
|---|---|---|
| **A · Licencia territorial** | **6.000–30.000 €/año** | Panel de aforo/rutas para el destino |
| **B · Informe trimestral de destino** | **5.000–15.000 €/informe** | Gestión de masificación, reparto de flujo |
| **C · Estudio Año Santo 2027** | **15.000–60.000 €+** | Proyecto ad-hoc, vía licitación/convenio |

**ACV institucional: 30.000–100.000 €+/año** (ciclo largo, alto valor).

### Verticales adyacentes (S7)

- **Licencia de datos / partnership:** a medida, **desde 3.000 €/año** o revenue-share.
  No prioritario; oportunista.

---

## 4. Matriz de cuadrantes (precio × recurrencia)

Cómo cae cada segmento y qué combinación de piezas se le ofrece.

```
              ▲ PRECIO ALTO
              │
  S6 Instituc.│ estudio Año Santo 2027 (C)      │ S5 TT.OO./cadenas: A enterprise + B premium
  (C one-off) │ cruce BBDD gran cuenta (C)       │ S6 licencia territorial + B destino
  ────────────┼──────────────────────────────────┼─────────────────────────────►
  NO RECURRENTE                                    RECURRENTE
  ────────────┼──────────────────────────────────┼─────────────────────────────►
  S4 Retail:  │ informe único de gancho          │ S1 Alojamiento: A Pro + B (núcleo MRR)
  freemium →  │ cruce BBDD pyme (C, 500–1.500 €)  │ S2 Restauración: A Pro + B
  upsell      │                                   │ S3 Servicios: A Basic/Pro + B
              │                                    ▼ PRECIO BAJO
```

**Los cuatro cuadrantes, en claro:**

| Cuadrante | Quién | Qué le vendemos | Rol en el negocio |
|---|---|---|---|
| **Alto + Recurrente** | S5 grandes cuentas, S6 licencia territorial | A enterprise + B premium (retainer) | **Margen y prestigio** |
| **Alto + No recurrente** | S6 estudios Año Santo, cruce BBDD de gran cuenta | C (proyecto) | **Picos de caja, entrada** |
| **Bajo + Recurrente** | S1, S2, S3 | A Pro + B trimestral (bundle) | **MRR / núcleo del negocio** |
| **Bajo + No recurrente** | S4 retail, micro-servicios | Free → informe único / C pyme | **Captación / long tail** |

---

## 5. Lógica de crecimiento (cómo se sube de cuadrante)

1. **Entrar por el gancho:** mapa gratis de su zona → activa al negocio (bajo/no recurrente).
2. **Convertir a recurrente:** el primer informe trimestral demuestra 5 acciones con € → pasa
   a bundle A+B (bajo/recurrente = el MRR).
3. **Subir a ticket alto:** cuando pide cruzar **su** BBDD de clientes → engagement C, y las
   grandes cuentas entran directamente por aquí.
4. **Ancla institucional:** un contrato S6 (Xacobeo 2027) da credibilidad para vender a todo el
   resto.

---

## 6. Fuentes de los anclajes

- **[S1] PMS/channel manager pyme:** Misterplan (desde 45 €/mes), HotelManager (desde 79 €/mes),
  planes gratis Amenitiz/Avirato. https://misterplan.es/precios-channel-manager-hoteles.html ·
  https://www.hotelmanager.es/precios/
- **[S2] Consultoría/marketing pyme España:** 60–150 €/h · 500–3.000 €/proyecto · 400–2.000 €/mes.
  https://asest.es/story/cuanto-cuesta-una-consultoria-de-marketing/ ·
  https://www.esconzeta.com/es/blog/cuanto-cuesta-agencia-marketing-digital-espana
- **[S3] Presupuesto público/grandes cuentas:** Xunta 125,9 M€ (2026) ·
  https://www.xunta.gal/es/notas-de-prensa/-/nova/018257/... · SEGITTUR PID 130 M€ ·
  https://planderecuperacion.gob.es/noticias/se-pone-en-marcha-plataforma-inteligente-destinos-pid-prtr
- Gasto del peregrino y estacionalidad: ver `universo-clientes.md` §1 y §6.
