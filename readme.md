DOCKER:

1. Tener instalado docker: https://www.docker.com/products/docker-desktop/
2. paso: Construirlo -> 
    ```docker build -t town_arrival```
3. paso: Ejecutarlo -> 
    ```docker run -p 8000:8000 town_arrival```

Cada vez que estamos desarrollando y añadimos cosas nuevas hay que construir de nuevo el proyecto y volver a ejecutarlo.

Aunque te salga la linea: Starting development server at http://0.0.0.0:8000/ no hay que meterse en ese link, hay que usar el siguiente:


URL: http://127.0.0.1:8000/