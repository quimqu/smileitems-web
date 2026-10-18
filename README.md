# smileitems.com

Web de marca de **Smile Items** (detalls de cumpleanys i farciment de piñates
que venem a Amazon.es). Estàtica, en castellà, a Cloudflare Pages. No ven res:
tots els botons porten a la botiga d'Amazon o a la fitxa de cada producte.

- Botiga: https://www.amazon.es/stores/page/CEB684D1-29E5-4254-8359-192E5743696E
- Titular de la web: Double Q Works, S.L.U. (a Amazon, el venedor encara és la
  persona física).
- Correu: `customerservice@smileitems.com` → arriba a `quimqu@gmail.com`
  (Cloudflare Email Routing) i s'hi respon des de Gmail «en nom de» (SMTP de
  Resend).

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

La primera vegada cal crear el projecte abans:
`npx wrangler pages project create smileitems --production-branch main`.

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

### 4. Enviar: Resend

1. Resend → *Domains* → *Add domain* → `smileitems.com`, regió **eu-west-1**.
2. Afegir els registres que dona a Cloudflare DNS, tots en **DNS only** (núvol
   gris). Seran aquests tres (copiar els valors exactes de Resend):
   - `TXT resend._domainkey` → la clau DKIM
   - `MX send` → `feedback-smtp.eu-west-1.amazonses.com`, prioritat 10
   - `TXT send` → `v=spf1 include:amazonses.com ~all`

   Van al subdomini `send`, o sigui que **no xoquen** amb els MX d'Email Routing
   de l'arrel. Resend també pot afegir-los sol si li connectes Cloudflare.
3. *Verify*.
4. Afegir DMARC a Cloudflare: `TXT _dmarc` → `v=DMARC1; p=none;`
   (més endavant, quan tot vagi bé, `p=quarantine`).
5. Resend → *API Keys* → *Create* → nom `gmail-smtp`, permís **Sending access**,
   domini **smileitems.com**. Copiar-la: només es veu un cop.

### 5. Gmail «en nom de»

Gmail (quimqu@gmail.com) → ⚙ → *Ver todos los ajustes* → *Cuentas e
importación* → *Enviar como* → *Añadir otra dirección de correo electrónico*:

- Nombre: `Smile Items` · Correo: `customerservice@smileitems.com` · deixar
  marcat *Tratar como un alias*.
- Servidor SMTP `smtp.resend.com` · port **465** · usuari `resend` ·
  contrasenya = l'API key del pas 4.5 · *Conexión segura con SSL*.
- Gmail envia un codi a customerservice@ → arriba al mateix Gmail per Email
  Routing → enganxar-lo.
- Al mateix apartat, marcar *Responder desde la misma dirección a la que se
  envió el mensaje*: així, les respostes a clients surten soles des de
  customerservice@.

### Comprovar-ho

- Des d'un altre compte (no des del mateix Gmail, que deduplica), escriure a
  customerservice@smileitems.com → ha d'arribar a quimqu@gmail.com.
- Respondre'l → al destinatari, *Mostrar original* ha de dir
  `SPF: PASS`, `DKIM: PASS (smileitems.com)`, `DMARC: PASS`.

## Pendents

- **CIF i dades del Registre Mercantil** de Double Q Works a `aviso-legal/`
  (la LSSI les exigeix; hi ha un comentari `PENDENT` al lloc).
- Repositori a GitHub (`quimqu/smileitems-web`, privat) i `git push`.
- Donar d'alta la propietat a Search Console i enviar el sitemap.

## Gotcha de xarxa

Des de Movistar hi ha rangs d'IP de Cloudflare bloquejats (ordres judicials pel
futbol). Si la web no carrega des de casa però sí des del mòbil amb dades, és
això, no el desplegament.
