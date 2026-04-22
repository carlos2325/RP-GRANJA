# Conexión SSH a este equipo (Raspberry Pi – granja-iot)

Usa esta carpeta para conectar **desde otro equipo** a este Raspberry Pi por SSH (incluido Cursor Remote SSH).

---

## Parámetros de conexión

| Parámetro | Valor |
|-----------|--------|
| **Host / IP** | `192.168.1.135` |
| **Hostname** | `raspberrypi` |
| **Usuario** | `pi` |
| **Puerto** | `22` |
| **Ruta del proyecto** | `/home/pi/granja-iot` |

---

## Conectar desde el otro equipo

### Opción A: Por contraseña (rápido para probar)

```bash
ssh pi@192.168.1.135
```

### Opción B: Por clave SSH (recomendado para Cursor)

```bash
ssh-keygen -t ed25519 -C "cursor-granja-iot" -f ~/.ssh/id_ed25519_granja
ssh-copy-id -i ~/.ssh/id_ed25519_granja.pub pi@192.168.1.135
```

Configura en `~/.ssh/config` (en el otro equipo):

```
Host granja-iot
    HostName 192.168.1.135
    User pi
    Port 22
    IdentityFile ~/.ssh/id_ed25519_granja
```

Luego:

```bash
ssh granja-iot
```

---

## Usar en Cursor (Remote SSH)

1. `Cmd+Shift+P` → **Remote-SSH: Connect to Host**
2. Elige `granja-iot` o `pi@192.168.1.135`
3. Abre carpeta: `/home/pi/granja-iot`
