# smileitems.com

Web de marca de **Smile Items** (detalls de cumpleanys i farciment de piñates
que venem a Amazon.es). Estàtica, en castellà, a Cloudflare Pages. No ven res:
tots els botons porten a la botiga d'Amazon o a la fitxa de cada producte.

- Botiga: https://www.amazon.es/stores/page/CEB684D1-29E5-4254-8359-192E5743696E
- Titular de la web: Double Q Works, S.L.U. (a Amazon, el venedor encara és la
  persona física).
- Correu: `customerservice@smileitems.com` → arriba a `quimqu@gmail.com`
  (Cloudflare Email Routing) i s'hi respon des de Gmail «en nom de» (SMTP de
  Brevo). Resend no: el pla gratuït només admet un domini i ja el fa servir
  silncy.

## Estructura

```
public/            el que es publica (index, aviso-legal/, privacidad/, 404)
  img/             generades per tools/images.py, no editar a mà
raw/               originals: fotos de les fitxes d'Amazon i bàners de la botiga
tools/images.py    raw/ → public/img (webp, logo transparent, og.jpg, icones)
wrangler.toml      projecte de Pages "smileitems"
```

Productes que surten a la web (els vius el 18/10/2026):

| ASIN | Producte |
|---|---|
| B0DPBG4WH9 / B0FBMMCT9Z | Muñecos Smiley ×20 / ×40 (una sola targeta, dos botons) |
| B0DPBKC7YY | Squishy caca ×20 |
| B0DSV1KVB3 | Mini cubos ×24 |
| B0FBS527XB | Laberintos 3D ×20 |
| B0GWY9XHPN | Libros pintar con agua ×12 |
| B0DTJ1CJ4W | Adhesivos WC ×8 |

L'helicòpter (B0DLY2LBJT) i el Montessori (B0F9FG19T8) ja no existeixen a
Amazon. **Si es dona de baixa o d'alta un producte, cal tocar `index.html`.**
No hi posem preus a propòsit: canvien i Amazon és la font de veritat.

## Provar-la en local

```bash
py -3 -m http.server 8798 --directory public
```

(o `preview_start smileitems-web`, que és al `C:\dev\.claude\launch.json`).

## Publicar

Des d'Ubuntu (WSL), on wrangler ja té sessió iniciada amb quimqu@gmail.com:

```bash
cd /mnt/c/dev/smileitems-web && npx wrangler pages deploy public --project-name smileitems --branch main --commit-dirty=true
```

El projecte es va crear el 18/10/2026 amb
`npx wrangler pages project create smileitems --production-branch main --force`.
El `--force` cal perquè wrangler 4.151 ara intenta convertir els projectes nous
de Pages en Workers. Un cop creat, els `pages deploy` ja van directes a Pages
i no s'hi ha de posar `--force`.

---

## Posada en marxa (una sola vegada)

El domini és a **Namecheap** amb els seus DNS (`dns1/dns2.registrar-servers.com`)
i el 18/10/2026 no tenia cap registre: ni web ni correu (qualsevol mail a
customerservice@ rebotava).

### 1. Portar el domini a Cloudflare (DNS)

1. Cloudflare → *Add a domain* → `smileitems.com` → pla Free.
2. Namecheap → Domain List → smileitems.com → *Nameservers* → **Custom DNS** →
   els dos que doni Cloudflare. Esperar que la zona surti *Active* (minuts o
   poques hores).
3. A la zona, deixar **desactivats** *Block AI bots* i *Managed robots.txt*
   (a silncy s'han reactivat sols algun cop).

### 2. Web a Pages

1. Publicar (ordre de dalt).
2. Pages → smileitems → *Custom domains* → afegir `smileitems.com` i
   `www.smileitems.com` (com que la zona és a Cloudflare, crea els CNAME sola).
3. Zona → *Rules* → *Redirect Rules* → plantilla «Redirect from WWW to root»
   (301), perquè només hi hagi una URL canònica.

### 3. Rebre: Cloudflare Email Routing

1. Zona → *Email* → *Email Routing* → *Get started*. Afegeix sol els MX
   (`route1/2/3.mx.cloudflare.net`) i el TXT SPF de l'arrel.
2. *Destination addresses* → `quimqu@gmail.com` (cal clicar l'enllaç que arriba).
3. *Routing rules* → `customerservice@smileitems.com` → *Send to* →
   `quimqu@gmail.com`.

### 4. Enviar: Brevo (compte de Double Q Works, pla gratuït: 300 correus/dia)

1. Brevo → ⚙ → *Senders, Domains & Dedicated IPs* → *Domains* → `smileitems.com`
   → mètode **Automatic** (Domain Connect amb Cloudflare). Fet el 18/10/2026; va
   afegir:
   - `TXT @` → `brevo-code:...` (verificació)
   - `CNAME brevo1._domainkey` / `brevo2._domainkey` → `b1/b2.smileitems-com.dkim.brevo.com`
     (DKIM; Brevo en té una d'activa i l'altra de recanvi)
   - `TXT _dmarc` → `v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com`

   Els MX i l'SPF d'Email Routing queden igual: Cloudflare els té bloquejats.
2. Brevo demana verificar el telèfon abans del primer enviament.
3. ⚙ → *SMTP & API* → *SMTP* → *Generate a new SMTP key* (nom `gmail`).
   El *Login* és una adreça `...@smtp-brevo.com`, no el correu del compte.
4. Si el correu transaccional té el seguiment d'obertures/clics activat,
   desactivar-lo (reescriu els enllaços de les respostes).

### 5. Gmail «en nom de»

Gmail (quimqu@gmail.com) → ⚙ → *Ver todos los ajustes* → *Cuentas e
importación* → *Enviar como* → *Añadir otra dirección de correo electrónico*:

- Nombre: `Smile Items` · Correo: `customerservice@smileitems.com` · deixar
  marcat *Tratar como un alias*.
- Servidor SMTP `smtp-relay.brevo.com` · port **587** · usuari = el *Login* de
  Brevo · contrasenya = la clau SMTP · *Conexión segura con TLS*.
- Gmail envia un codi a customerservice@ → arriba al mateix Gmail per Email
  Routing → enganxar-lo.
- Al mateix apartat, marcar *Responder desde la misma dirección a la que se
  envió el mensaje*: així, les respostes a clients surten soles des de
  customerservice@.

### Comprovar-ho

- Des d'un altre compte (no des del mateix Gmail, que deduplica), escriure a
  customerservice@smileitems.com → ha d'arribar a quimqu@gmail.com.
- Respondre'l → al destinatari, *Mostrar original* ha de dir
  `DKIM: PASS (smileitems.com)` i `DMARC: PASS` (l'SPF passa amb el domini de
  Brevo; no cal que estigui alineat perquè ja ho està el DKIM).

## Pendents

- **CIF i dades del Registre Mercantil** de Double Q Works a `aviso-legal/`
  (la LSSI les exigeix; hi ha un comentari `PENDENT` al lloc).
- Repositori a GitHub (`quimqu/smileitems-web`, privat) i `git push`.
- Donar d'alta la propietat a Search Console i enviar el sitemap.

## Gotcha de xarxa

Des de Movistar hi ha rangs d'IP de Cloudflare bloquejats (ordres judicials pel
futbol). Si la web no carrega des de casa però sí des del mòbil amb dades, és
això, no el desplegament.
