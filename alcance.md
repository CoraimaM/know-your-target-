Enlace al programa: https://www.shopify.com/es-es

- fecha de consulta: 03/11/2026

- Qué entra y qué no entra en el alcance
	Lo primero que me llamó la atención es que Shopify separa sus activos en dos grupos: los **Core**, que son los más importantes y donde se puede reportar hasta severidad crítica, y los **Non-core**, que se puntúan más bajo. En el CSV salen 30 activos en total: 19 pagan recompensa y 11 no.

- Lo que se puede reportar, pero no paga
	Las apps de terceros y las tiendas de terceros. En el caso de las apps, primero tienes que avisar al desarrollador y solo acudes a Shopify si no te contesta como toca.
	Cualquier vulnerabilidad real en un activo que no esté en la lista puede aceptarse, pero sin recompensa.
	
 - Lo que está fuera (ni siquiera se puede reportar)
	 `investors.shopify.com`, `academy.shopify.com`, `*.email.shopify.com`, `community.shopify.com` y `community.shopify.dev`, porque los llevan terceros.
	 `cdn.shopify.com`, porque subir archivos ahí es una función normal y no cuenta como vulnerabilidad.
	 `livechat.shopify.com`, el portal de proveedores (supplier-portal) y el apartado genérico "Other".
	-Los "Core Ineligible Findings", que el programa excluye de forma expresa.

- ¿Permite herramientas automáticas?

	Esto no lo dice en ningún sitio de la información que tengo, ni a favor ni en contra, así que no podemos afirmar que se permitan ni que se prohíban. Lo más sensato es dejar claro que no se especifica y que, si hay dudas, se escribe a `bugbounty@shopify.com`. Eso sí, exigen una **prueba de concepto que funcione** para demostrar el impacto; si no la tienes, el informe se cierra como N/A, así que lanzar un escáner a ciegas no sirve de mucho.

- ¿Hay límite de peticiones?
	Tampoco aparece ningún límite en la información disponible. Lo que sí hay son normas de conducta: tus pruebas no pueden romper ni tocar datos que no sean tuyos, ni tumbar el servicio.

- ¿Se puede contactar con empleados?
	Con los empleados en general no pone ninguna prohibición, pero con el **Soporte de Shopify** sí que hay una norma clara: no se puede contactar con ellos (por chat, correo ni teléfono) ni para probar, ni para preguntar por la recompensa, ni para pedir novedades o validar un informe antes de enviarlo. Si lo haces, pierdes la recompensa y te pueden echar del programa. Para dudas sobre reglas o alcance, el canal bueno es `bugbounty@shopify.com`. Además, los empleados de Shopify no pueden participar y tienen que usar el programa interno.

- ¿Piden identificarse?
	Sí, y varias cosas:
	- La cuenta de Shopify hay que crearla con el correo alias `@wearehackerone.com` que te da HackerOne.
	- Solo puedes probar en tiendas que hayas creado tú con ese correo. Probar con comerciantes reales está prohibido y te pueden descalificar.
	- Piden una puntuación Signal de 1.0 o más en el último año; si estás por debajo, se usan informes de prueba.
	- No pueden participar personas ni países que estén en listas de sanciones.

- Otras reglas que vale la pena mencionar
	- No se puede publicar nada antes de que esté resuelto, salvo que den permiso.
	- Hay que reportar cada vulnerabilidad en cuanto la validas.
	- Si varios informes comparten la misma causa raíz, los siguientes se cierran como duplicados.
	- Si encuentras credenciales filtradas, solo puedes autenticarte y desautenticarte al momento, sin usar ninguna función, y no las puedes compartir fuera del informe.
	- Todo lo que envíes queda bajo licencia MIT, y los impuestos del pago van por tu cuenta.
