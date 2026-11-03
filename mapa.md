## 1. Resumen
 
- **Quién es:** Shopify, plataforma de comercio electrónico con sede en Ottawa (Canadá), empresa pública del sector software y más de 10.001 empleados (Correos, Netcraft).
- **Dominio:** `shopify.com`, registrado en 2005 en MarkMonitor, con los seis bloqueos EPP, DNSSEC activo y titular oculto (Registro, Netcraft).
- **Superficie:** `subfinder` saca 1.290 subdominios; DNSDumpster cuenta 1.395 registros A. Por nombre, unos 900 son tiendas de comerciantes (Subdominios, DNSDumpster).
- **Infraestructura:** IP `23.227.38.33` dentro del bloque propio SHOPIFY-NET, detrás de Cloudflare; correo en Google Workspace; DMARC en `p=reject` (Netcraft, DNSDumpster).
- **Lo más interesante:** unos 150 entornos de pruebas y varios nombres de infraestructura interna en DNS. Sin directorios abiertos y con `security.txt` apuntando a HackerOne (Subdominios, Dorks, Ficheros).
---
 
## 2. Dominios y subdominios
 
| Subdominio / familia | IP | En alcance | Para qué parece servir |
|---|---|---|---|
| `shopify.com`, `www`, `shopify.shopify.com` | 23.227.38.33 (ptr `checkout.shopify.com`) | Sí | Web principal |
| `admin`, `accounts`, `account`, `partners` | — | Sí (explícitos) | Panel de comerciantes, login, portal de socios |
| `developer(s)`, `dev`, `devs`, `api`, `app(s)`, `appstore`, `mcp`, `polaris*` | — | Sí | Desarrolladores, API, tienda de apps, servidor MCP, sistema de diseño |
| `shoppay`, `pay`, `paylinks.commerce`, `money`, `lending`, `invoices`, `checkout` | — | Sí | Pagos, préstamos y facturas |
| `hardware*`, `device-enrollment*`, `*.checkout.hardware` (ie, eu, uk, au, sg, ca, nz), `pointofsale`, `ipad-pos` | — | Sí | Punto de venta físico |
| `help*`, `support*`, `internal.help`, `classic-help` | — | Sí | Ayuda y soporte (varios de pruebas) |
| `collabs*` | — | Sí | Plataforma de colaboraciones |
| **`shell*`, `sidekick-staging-N`** | — | Sí | Entornos de pruebas/previsualización |
| **Otros `*-staging`, `canary-*`, `upcoming*`, `test`, `mock`, `testseed`** | — | Sí | Preproducción y pruebas |
| `data`, `analytics`, `datastories`, `datagolf`, `gtm*` | — | Sí | Datos y analítica |
| **`egress-ips`, `failover`, `mc-proxy`, `storefront-agent-server`, `agent-server-next`, `cms`, `cms.everest`, `vault`, `smtp`, `status`** | — | Sí | Piezas internas |
| Registros `_dmarc`, `_mta-sts`, `_msdcs`, `_cisco-uds`, `_cuplogin`, `_collab-edge`, `_etcd-server-ssl` | — | Sí | No son webs: son registros DNS de correo, directorio, telefonía y un clúster etcd |
| `o1`–`o44.mailer`, `mta*.email`, `click`/`view`/`site.email`, `email.careers` | — | **No** (`*.email.shopify.com`); revisar el resto | Envío masivo de correo |
| `ssl` y `b`…`s.ssl` | — | Sí | Frontales antiguos (hipótesis) |
| `23-227-38-N` (22-37, 39-41, 60-62, 76) y `23.227.38.65` | 23.227.38.N | Sí | Hosts con la IP en el nombre |
| `press`, `newsroom`, `blog`, `events`, `careers`, `candidate`, `talent`, `internships`, `bugbounty`, `bounty`, `hack` | — | Sí | Contenido, empleo y programa de bugs |
| `academy`, `cdn`, `community`, `investors`, `livechat` | — | **No** | Formación, CDN, comunidad, inversores y chat |
| Tiendas de comerciantes (`acmi`, `coastmoto`… y `*.my.shopify.com`) | — | **No** (terceros) | Comercios de clientes |
 
Otros datos de DNS:
- **Nameservers:** `gold.foundationdns.com` (172.64.40.2), `.net` (162.159.60.32) y `.org` (108.162.198.62), todos en Cloudflare (AS13335) (DNSDumpster). El whois da otras IPs para los mismos nombres (Registro).
- **Dominios «similares»** (`shopi10.com`, `shopi88.org`…): son nombres parecidos sin relación visible con Shopify (Registro).
- **Ruido:** entradas como `2fcdn` o `252fcdn` parecen restos de `%2F` y no las trataría como hosts reales (Subdominios).
---
 
## 3. Infraestructura y servicios
 
**Hosting y red** (Netcraft)
- Empresa de hosting: Shopify (Canadá). Propietario del bloque: Shopify, Inc., rango `23.227.32.0-23.227.63.255` (SHOPIFY-NET).
- IPv4 `23.227.38.33`, sin IPv6. AS13335 (Cloudflare) y servidor `cloudflare`.
- Posición en el ranking de Netcraft: 716. Primera vez visto: septiembre de 2007.
**Tecnologías** (Netcraft)
- Cloudflare como CDN y acelerador HTTP; HTML5, UTF-8, gzip y librerías alojadas en Google.
- Cabeceras de seguridad: HSTS (con preload), `X-Content-Type-Options` y `X-XSS-Protection`.
- Dos rastreadores: Google Tag Manager y un widget de Shopify servido desde `cdn.shopify.com`.
**TLS** (Netcraft)
- Certificado `shopify.com` y `*.shopify.com`, validación de dominio, emitido por Google Trust Services (WE1), vigente del 8/10/2026 al 6/1/2027.
- TLS 1.3, ECDSA, HTTP/2 y Perfect Forward Secrecy. Sin SSLv3 y sin Heartbeat.
**Correo** (DNSDumpster, Netcraft)
- MX en Google Workspace (`aspmx.l.google.com` y `alt1`–`alt4`).
- SPF con `_spf.google.com`, `mail.zendesk.com` y `sendgrid.net`, terminado en `~all` (softfail).
- DMARC `p=reject; pct=100; fo=1`, con informes a `dmarc-aggregate@shopify.com` y `dmarc-reports@shopify.com`.
**Servicios de terceros** (DNSDumpster, registros TXT de verificación)
- Aparecen verificaciones de Atlassian, Stripe, Twilio, Klaviyo (varias), MongoDB, Zapier, DocuSign, Apple, Adobe, Microsoft, OpenAI (tres), Linear, TeamViewer, Drift, Facebook y Amazon SES, entre otros.
- Son una pista de la pila de SaaS que usa la empresa, pero todos son de terceros y quedan fuera de alcance.
**Shodan**
- Búsqueda de `shopify.com`: unos 4.587 resultados. Mayoría en EE. UU. (1.648), Alemania (630) y Reino Unido (356).
- Puertos: 443 (3.275), 80 (1.079), 8080 (94), 6081 (35) y 3000 (23).
- Organizaciones: Amazon (970 y 649), Hetzner (410), DigitalOcean (219) y Cloudflare (143).
- Productos: nginx (2.022), Apache (903), CloudFront (303). Sistemas: Ubuntu (496) y unos pocos Windows y FreeBSD antiguos.
- Los resultados que se ven (Four Roses Bourbon, Shaped Pens…) son tiendas de terceros con certificados propios. Esto es el rastro de comerciantes y no la infraestructura de Shopify, así que no lo tomaría como superficie propia.
**Ficheros y dorks**
- `robots.txt` bloquea `/authentication/` y `/* /account`.
- `security.txt`: `security@shopify.com`, clave de cifrado, política en HackerOne y página de agradecimientos (Ficheros).
- `intitle:"index of" shopify.com` no encuentra directorios abiertos; solo un hilo de un comerciante en la comunidad (Dorks).
---
 
## 4. Correos y personas
 
**Patrón de correo** (Correos)
- Hunter da 4.547 resultados: 4.259 personas, 257 decisores y 288 genéricos. Todos salen con la parte local oculta (`********@shopify.com`), así que **el patrón no se puede deducir de la captura**.
- Buzones confirmados: `security@shopify.com` (Ficheros), `dmarc-aggregate@shopify.com` y `dmarc-reports@shopify.com` (Netcraft).
**Organización y personas** (Correos)
- 53 ejecutivos. Los primeros que salen: Tobias L. (CEO), Harley F. (President), Jane L. (Partner) y Lauren N. (VP of Enterprise Revenue).
- Sede en Ottawa (Ontario), sector software, más de 10.001 empleados, empresa pública.
- Hay reclutamiento propio por subdominios (`candidate`, `talent`, `internships`) (Subdominios).
- Hay subdominios con pinta de nombre propio (`maxine.sarmiento`, `rishabh.tu`, `devarshy`, `kerwin`), sin confirmar si son empleados o comerciantes (Subdominios).
- El whois no da ninguna persona (Registro).
---
 
## 5. Puntos de interés
 
**1. Entornos de pruebas (~150 hosts)**
- `shell*`, `sidekick-staging-N`, `upcoming*`, `*-staging` y `canary-*` (Subdominios).
- Es el bloque más grande y donde es más probable que haya controles distintos a producción. Todo cuelga de `*.shopify.com`, que está en alcance.
- Primero comprobar cuáles resuelven y cuáles piden login. De paso, cruzar con los 1.395 registros A de DNSDumpster para ver los ~100 que `subfinder` no sacó.
**2. Panel, identidad y socios: `admin`, `accounts`, `partners`**
- Están incluidos de forma explícita en el programa (Subdominios).
- `robots.txt` esconde `/authentication/` y `/account`, así que ahí hay flujos de autenticación que Shopify considera sensibles (Ficheros).
- Probar solo con tiendas creadas por nosotros, con el correo de HackerOne.
**3. Infraestructura interna y servicios de agentes**
- `egress-ips`, `failover`, `mc-proxy`, `storefront-agent-server`, `agent-server-next`, `mcp`, `internal.help`, `cms.everest` y `_etcd-server-ssl` (Subdominios).
- Nombres que no deberían interesar desde fuera y aparecen en DNS. Los de agentes y MCP son tecnología reciente, probablemente menos probada.
- Primero resolverlos y ver cuáles responden; es probable que casi todos estén cerrados.
