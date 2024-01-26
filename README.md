# API.grea_23
API experimental para pasarela de datos

<ul>Actuamente esta API puede consultar:
  <li><a>La descripción de los Municipios.</a>
  <li><a>Municipios con un estado y programa específico.</a></li>
  <li><a>Municipios ...</a></li>
</ul>

# Producción
Para poder poner en producción este código se necesita:

- Llevar el código API.grea_23 a la máquina de destino.
- Acceder a dicho directorio para crear una imagen con el Dockerfile.
- Lanzar:
   ```console
  docker build -t myimage .
   ```
- Arrancar con:
  ```console
   docker run -d --name mycontainer -p 80:80 myimage
  ```
