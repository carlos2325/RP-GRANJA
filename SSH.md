# Conexión SSH – Granja IoT

Referencia para conectarte por SSH a la Raspberry Pi del proyecto.

---

## Conectar desde tu PC/Mac

```bash
ssh pi@192.168.1.135
```

**Si `ssh granja` dice "Could not resolve hostname granja":**  
En tu Mac, copia la carpeta del proyecto (o solo el script) y ejecuta una vez:
```bash
sh /ruta/a/granja-iot/setup-ssh-config.sh
```
O con otra IP: `sh setup-ssh-config.sh 192.168.1.50`. Así se crea/actualiza `~/.ssh/config` con el host `granja`.

- **Usuario:** `pi`
- **IP usada en el proyecto:** `192.168.1.135` (cámbiala si tu Pi tiene otra IP)

---

## Si la IP de la Raspberry cambió

En la Raspberry (pantalla + teclado o consola local):

```bash
hostname -I
```

El primer número es la IP (ej: `192.168.1.50`). Luego conecta:

```bash
ssh pi@192.168.1.50
```

Desde otra máquina en la misma red, si tienes avahi:

```bash
ssh pi@raspberrypi.local
```

---

## Copiar el proyecto a la Raspberry

Desde tu PC (carpeta del proyecto en tu máquina):

```bash
scp -r /ruta/a/granja-iot/* pi@192.168.1.135:~/granja-iot/
```

O solo archivos concretos:

```bash
scp config.py app.py pi@192.168.1.135:~/granja-iot/
```

---

## Copiar desde la Raspberry a tu PC

```bash
scp -r pi@192.168.1.135:~/granja-iot/* ./granja-iot-backup/
```

---

## Evitar escribir la contraseña cada vez (clave SSH)

En tu **PC/Mac** (donde tienes Cursor):

**1. Crear clave SSH (solo una vez):**
```bash
ssh-keygen -t ed25519 -C "granja-iot" -f ~/.ssh/granja_iot -N ""
```

**2. Copiar la clave pública a la Raspberry (solo una vez):**
```bash
ssh-copy-id -i ~/.ssh/granja_iot.pub pi@192.168.1.135
```

**3. Añadir el host en tu config SSH**

```
Host granja
    HostName 192.168.1.135
    User pi
    IdentityFile ~/.ssh/granja_iot
    IdentitiesOnly yes
```

Sustituye `192.168.1.135` por la IP de tu Raspberry si es distinta.

**4. Probar en terminal:** `ssh granja`

**Si al abrir Cursor/SSH te pide otra vez la “clave” (frase de paso de tu clave):**  
Es la contraseña de tu archivo `granja_iot`, no la de la Raspberry.

- Opción A:
```bash
ssh-add ~/.ssh/granja_iot
```

- Opción B: en `~/.ssh/config`, dentro del bloque `Host granja`, añade:
```
AddKeysToAgent yes
```
