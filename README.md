# Collectoholic — app para iPhone y iPad (con GitHub Actions)

Igual que la versión de Android, la app muestra https://collectoholic.neocities.org/. Lo que publiques en Neocities aparece en la app sin recompilarla.

## Coste
Para firmar la app y subirla a TestFlight o a la App Store necesitas el **Apple Developer Program: 99 € al año**. Sin esa cuenta, no hay forma de instalar la app en un iPhone que no sea el tuyo.

## 1. Subir el proyecto a GitHub
Crea un repositorio y sube todos los archivos, incluida la carpeta `.github`. El flujo se ejecuta en un Mac virtual de GitHub, así que no necesitas un Mac.

## 2. Crear la cuenta y los certificados (en developer.apple.com)
1. Inscríbete en el Apple Developer Program.
2. En **Certificates, Identifiers & Profiles**, crea un **App ID** con el identificador `org.collectoholic.museo`.
3. Crea un certificado **Apple Distribution**. Para generar la petición (CSR) sin Mac, puedes usar OpenSSL, que viene con Git Bash en Windows:

       openssl req -new -newkey rsa:2048 -nodes -keyout clave.key -out peticion.csr

   Sube `peticion.csr` en Apple, descarga el certificado (`.cer`) y conviértelo a `.p12` con la clave:

       openssl x509 -inform DER -in distribution.cer -out distribution.pem
       openssl pkcs12 -export -inkey clave.key -in distribution.pem -out certificado.p12

   Pon una contraseña al `.p12` y anótala.
4. Crea un **perfil de aprovisionamiento** de tipo **App Store** para ese App ID y ese certificado. Descárgalo como `.mobileprovision`.
5. Anota tu **Team ID** (en Membership).

## 3. Crear los secretos en GitHub
Settings → Secrets and variables → Actions:

- `APPLE_TEAM_ID`: tu Team ID.
- `APPLE_CERT_P12_BASE64`: el `.p12` en base64. En Windows (PowerShell): `[Convert]::ToBase64String([IO.File]::ReadAllBytes("certificado.p12"))`
- `APPLE_CERT_PASSWORD`: la contraseña del `.p12`.
- `APPLE_PROVISIONING_PROFILE_BASE64`: el `.mobileprovision` en base64 (mismo método).
- `KEYCHAIN_PASSWORD`: cualquier contraseña, solo la usa el Mac virtual.

Opcional, para subir solo a TestFlight:

- `APP_STORE_KEY_ID`, `APP_STORE_ISSUER_ID`: de App Store Connect → Integrations → App Store Connect API.
- `APP_STORE_KEY_P8_BASE64`: la clave `.p8` en base64.

## 4. Compilar
Se ejecuta sola al subir cambios a `main`, o desde Actions → Build iOS → Run workflow. Al terminar, descarga el artefacto `collectoholic-ipa`. Si configuraste la clave de App Store Connect, el IPA también se sube a TestFlight.

Si el paso de compilación falla, abre el registro del paso que ha fallado. Este flujo no lo he podido probar, así que es probable que haya que ajustar algún detalle en la primera ejecución.

## 5. Antes de enviarla a revisión de Apple
- Apple puede rechazar apps que solo muestran una web (directriz 4.2). Ten preparada una descripción de lo que hace la app más allá de la web.
- Necesitas una URL de política de privacidad: la app guarda correos, sugerencias y museos en Supabase.
- Rellena la ficha de App Store Connect (capturas, descripción, icono de 1024×1024) y la información para revisores.

## Actualizaciones
Cada compilación usa el número de la ejecución de GitHub como número de versión de compilación. Mantén siempre el mismo certificado y el mismo App ID.
