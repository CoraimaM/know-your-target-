

# 📘 Informe de Reconocimiento Pasivo

## 🎯 Alcance y Limitaciones
Según las directrices de la auditoría, solo se investigan dominios dentro del alcance autorizado. 
- ✅ **`shopify.com`**: Dentro del alcance. Investigado completamente.
- 🚫 **`mercadolibre.com`** y **`blog.snapchat.com`**: Retornaron `BLOQUEADO` en todas las herramientas. Se confirman fuera del alcance autorizado y se descarten por protocolo.

---

## 1. 📋 Registro del Dominio (WHOIS)
| Campo | Valor | Herramienta |
|-------|-------|-------------|
| Dominio | `SHOPIFY.COM` | `whois_dominio` |
| Fecha de alta | `2005-03-11` | `whois_dominio` |
| Fecha de caducidad | `2027-03-11` | `whois_dominio` |
| Último cambio | `2025-09-02` | `whois_dominio` |
| Registrador | ID `292` (MarkMonitor, Inc.) | `whois_dominio` |
| Estado | `clientTransferProhibited`, `serverDeleteProhibited`, etc. | `whois_dominio` |
| Nameservers (registro) | `gold.foundationdns.com`, `gold.foundationdns.net`, `gold.foundationdns.org` | `whois_dominio` |

---

## 2. 🌐 Registros DNS
| Tipo | Valor(es) | Herramienta |
|------|-----------|-------------|
| **A** | `23.227.38.33` | `dns_registros` |
| **MX** | `1 aspmx.l.google.com.`<br>`5 alt1.aspmx.l.google.com.`<br>`5 alt2.aspmx.l.google.com.`<br>`10 alt3.aspmx.l.google.com.`<br>`10 alt4.aspmx.l.google.com.` | `dns_registros` |
| **NS** | `gold.foundationdns.org.`<br>`gold.foundationdns.net.`<br>`gold.foundationdns.com.` | `dns_registros` |

*Nota: Los MX apuntan a Google Workspace, confirmando el uso de infraestructura de correo gestionada por Google. Los NS coinciden exactamente con los declarados en WHOIS.*

---

## 3. 🌳 Subdominios Descubiertos
- **Fuente**: Transparencia de certificados (`crt.sh`)
- **Total en alcance**: `290` subdominios (38 filtrados por estar fuera de scope)
- **Herramienta**: `subdominios_crtsh`

### Ejemplos representativos por categoría:
- **Core/Infraestructura**: `api.shopify.com`, `core.shopify.com`, `data.shopify.com`, `m.shopify.com`, `app.shopify.com`
- **Plataforma/E-Commerce**: `checkout.shopify.com`, `commerceawards.shopify.com`, `hatchful.shopify.com`, `plus.shopify.com` (parcial)
- **Desarrollo/DevOps**: `dev.shopify.com`, `developer.shopify.com`, `engineering.shopify.com`, `console1.toronto.shopify.com`
- **Soporte/Comunicación**: `help.shopify.com`, `blog.shopify.com`, `careers.shopify.com`, `changelog.shopify.com`
- **SSL/Red interna**: `a.ssl.shopify.com`, `b.ssl.shopify.com`, `kafka-staging01.ec2.shopify.com`

---

## 4. 🔍 Huella Tecnológica y Observaciones
- **Netcraft**: `ERROR: Netcraft devolvió una página sin datos (probablemente se genera con JavaScript o bloquea clientes automáticos)`. Se recomienda consulta manual en: `https://sitereport.netcraft.com/?url=shopify.com` (`huella_netcraft`)
- **Correo electrónico**: La infraestructura MX confirma integración con Google (`aspmx.l.google.com`).
- **Infraestructura DNS**: Delegación a `foundationdns.com`, servicio empresarial de DNS gestionado (común en grandes empresas con requisitos de alta disponibilidad y seguridad).

---
✅ *Fin del informe. Todas las llamadas respetaron el límite de 20 y el principio de pasividad. Los dominios fuera de alcance se descartaron conforme a protocolo `BLOQUEADO`.*