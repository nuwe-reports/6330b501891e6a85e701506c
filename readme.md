# Talent Squad - Backend II - Nuwe

## Sobre el desafio

Reto NUWE creación API.[Talent Squad - Backend II](https://nuwe.io/dev/challenges/talent-squad-backend-ii)
#### Descripción NUWE
El reto que tenemos para ti consiste en crear una API de búsqueda de empleo que todos puedan utilizar. Y cuando se dice todos quiere decir todos, ya que incluso un marciano puede estar buscando su siguiente oportunidad laboral ;).

La información necesaria para las ofertas son:

* Título del trabajo
* Nombre de la empresa
* Pequeña descripción del trabajo
* Habilidades necesarias (e.j.: HTML, JavaScript, React, Node.js, etc.)
* El mercado en el que opera la empresa (e.j.: software, salud, ecommerce, etc.)
* Tipo de trabajo (e.j.: full time, contract, internship, etc.)
* Localización de la empresa, aunque el trabajo sea en romoto ;)
* Cualquier otra información que te pueda parecer relevante

Objetivos (user stories)
* Hacer una REST/GraphQL API en Node.js o cualquier otro Web Framework que * prefieras.
* Hacer un CRUD Endpoint para Create, Update, Delete or List ofertas de * trabajo.
* Crear un List Endpoint donde puedas buscar por título del trabajo, nombre * de la empresa, habilidades, mercado, tipo, localización y todos los * campos de información que has puesto en las descripciones.
* Hacer un endpoint de Subscribe/Unsubscribe donde el usuario pueda * registrarse con el email para recibir ofertas de trabajo.
* Hacer testing (con Postman/Insomnia o Automated)

## Solución
Se ha utilizado [fastAPI](https://fastapi.tiangolo.com/) para crear una API, sqlalchemy para almacenar los datos en una BD y pytest para hacer tests automáticos.

#### Job Posts
Crear: POST /API/v1/jobposts/create
Update: PUT /API/v1/jobposts/update/{id}
Delete: DELETE /API/v1/jobposts/delete/{id}
List: GET /API/v1/jobposts/list

Para buscar job posts: GET /API/v1/jobposts/search?name=nombre_a_buscar
Se puede buscar por otros campos cambiando name por otro campo
Se puede buscar por más de un campo concatenadolos con & (name=nombre_a_buscar&skills=skill_a_buscar)

#### Users
Crear Usuario: POST /API/v1/users/register
Suscribir: /API/v1/users/subscribe/{email}
Desuscribir: /API/v1/users/unsubscribe/{email}

Se puede ver más detalle de los endpoints en [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/). Para consultarlo el servidor debe estar activo.

## Cómo probar el código
Para poner en marcha el servidor se debe tener instaldo conda i se puede preparar el entorno con el siguiente comando:

```bash
conda env create -f env.yaml
conda activate nuwe-talent-squad-backend-2
uvicorn main:app --reload
```

Para probar los test se puede hacer con el siguiente comando
```bash
pytest -v
```
El resultado de los tests se puede ver en la captura siguiente
![Tests](img/tests.png)

El repositorio ya viene con una base de datos prerellenada con 3 ofertas que se han generacon con  ```src/insert_jobposts.py```