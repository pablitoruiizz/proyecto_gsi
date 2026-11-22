# Ver el WordPress local desde el móvil (por si se pide en la defensa)

Solo hace falta si alguien pide enseñar el portal en un móvil real. En la entrega no se pide.

## Qué pasa

WP Fastest Cache guarda las páginas con la dirección de quien las visita primero. Si el PC abrió el sitio por `localhost`, esas páginas llevan enlaces a `localhost` y, en el móvil, la web sale sin estilos ni imágenes. (El mu-plugin `cadus-entorno-tailscale.php` ya corrige la dirección del sitio, pero no la de las páginas ya guardadas.)

## Antes de enseñarlo (1 minuto, en el PC)

1. WampServer en marcha (Apache y MySQL en verde).
2. Vaciar la caché (PowerShell, desde cualquier carpeta):

```powershell
Remove-Item "C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\www\proyecto_gsi\cms-wordpress\wp-content\cache\all\*" -Recurse -Force
```

```powershell
Remove-Item "C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\www\proyecto_gsi\cms-wordpress\wp-content\cache\wpfc-minified\*" -Recurse -Force
```

3. Abrir la web **primero desde el móvil**, antes que desde el PC por `localhost`. Si se abre antes en el PC, hay que repetir el paso 2.

## Direcciones

- Misma wifi: `http://<IP del PC>/proyecto_gsi/cms-wordpress/` (ver la IP con `ipconfig`; la red debe estar como *Privada* en Windows).
- Tailscale (también con datos móviles): `http://<IP de Tailscale del PC>/proyecto_gsi/cms-wordpress/` (ver la IP con `tailscale ip -4`; el móvil debe tener Tailscale con la misma cuenta).

## Arreglo permanente (solo en el PC de la demostración)

En el escritorio de WordPress: WP Fastest Cache > Ajustes, desmarcar «Cache System», guardar y pulsar «Delete Cache». Las páginas tardan unos 3 s más, pero cargan bien por cualquier dirección. Ese plugin reescribe `.htaccess`: no se sube al repositorio.
