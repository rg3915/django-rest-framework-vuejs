# django-rest-framework-vuejs

Neste projeto eu uso [Django Rest Framework][1] e [VueJS][2] com todos os recursos que o [vue-cli](https://cli.vuejs.org/) pode oferecer.

![django-vue04.png](img/django-vue04.png)


Em Dev rodar **dois** servidores, back e front.

### Backend

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.
* Crie um super usuário

```
git clone https://github.com/rg3915/django-rest-framework-vuejs.git
cd django-rest-framework-vuejs
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

Para rodar o Django, dentro da pasta backend, digite:

```
python manage.py runserver
```

Isso vai rodar o servidor de back na porta **8000**.


### Frontend

Para rodar o VueJS, abra uma **nova aba no terminal**, e faça:

```
cd ../frontend
npm install  # primeiro precisa instalar o vue e suas dependências.
npm run serve
```

Isso vai rodar o servidor de front na porta **8080**.


## Comandos pra criar o projeto do zero

### Criando o projeto Django

```
mkdir backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install Django==2.2.12 djangorestframework django-extensions dj-database-url python-decouple django-cors-headers
django-admin startproject myproject .
cd myproject
python ../manage.py startapp core
cd ..
python manage.py migrate
# Crie um super usuário
python manage.py createsuperuser --username="admin" --email=""
```

#### Criando uma pasta chamada contrib com um env_gen.py

O comando a seguir pega `env_gen.py` do gist e clona na pasta `/tmp`.

[nvm gist][4]

```
git clone https://gist.github.com/22626de522f5c045bc63acdb8fe67b24.git /tmp/contrib; if [ ! -d contrib ]; then mkdir contrib; fi; cp /tmp/contrib/env_gen.py contrib/
# rode este comando para gerar o .env (variáveis de ambiente).
python contrib/env_gen.py
```

Em `settings.py` insira em `INSTALLED_APPS`...

```
INSTALLED_APPS = [
    ...
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'myproject.core',
]
```

Edite este trecho do `settings.py`:

```
import os
from decouple import config, Csv
from dj_database_url import parse as dburl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())
```

Configurando o [django-cors-headers][3]:

```
MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ORIGIN_ALLOW_ALL = True
```

E este trecho, onde vamos usar o sqlite:

```
default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}
```

No final do arquivo também edite:

```
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'
```

E

```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

Se você mudar a pasta default dos estáticos, então faça:

```
# opcional
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    'myproject/core/templates/static/',
]
```

Depois entre na pasta `myproject` e vamos editar `urls.py`:

```
cat << EOF > urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('myproject.core.urls')),
    path('admin/', admin.site.urls),
]
EOF
```

Depois entre na pasta `core`:

```
cd core/
```

e vamos editar `views.py`:

```
cat << EOF > views.py
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''
    Este viewset fornece automaticamente ações em 'list' e 'detail'.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
EOF
```

Ainda na pasta `core` vamos criar um `urls.py`:

```
cat << EOF > urls.py
from django.urls import include, path
from rest_framework import routers
from myproject.core import views as v


app_name = 'core'


router = routers.DefaultRouter()
router.register('user', v.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
EOF
```

... e `serializers.py`:

```
cat << EOF > serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )
EOF
```

#### Gravando alguns dados no banco

Vamos criar alguns usuários no Django, para isso vá para a pasta onde está o `manage.py` e digite:

```
# pasta backend
python manage.py shell_plus
```

Depois digite:

```
names = ['fulano', 'beltrano', 'cicrano']
[User.objects.create(username=name) for name in names]
```

Agora vamos para o front.

## Frontend

Volte para a pasta principal do projeto:

Eu estou usando o Node 12, que instalei via [nvm][4].

```
# pasta principal do projeto
cd ..
nvm use 12
vue create frontend
cd frontend
npm install axios
vue add vuetify
```

#### Servindo o front

Para rodar o VueJS, abra uma **nova aba no terminal**, e faça:

```
cd ../frontend
npm run serve
```

Isso vai rodar o servidor de front na porta **8080**.

#### Rodando o servidor Django

```
cd ../backend
python manage.py runserver
```

Isso vai rodar o servidor de back na porta **8000**.

## Finalizando o front

Entre na pasta `frontend`.

Repare que instalamos o [vuetifyjs][5], uma poderosa ferramenta de template para VueJS baseado em Material Design.

Vamos editar `App.vue`:

Acrescente `<Users/>` logo abaixo de `<HelloWorld/>`:

```
  <v-content>
    <HelloWorld/>
    <Users/>
  </v-content>
```

E acrescente:

```
...
import Users from './components/Users';

  components: {
    HelloWorld,
    Users
  },
```

Agora vamos criar o componente `Users.vue`:

```
cat << EOF > src/components/Users.vue
<template>

  <v-col class="mb-5" cols="12">
    <v-item-group multiple>
      <v-container>
        <v-row>
          <v-col
            v-for="user in users" :key="user.id"
            cols="12"
            md="4"
          >
            <v-item>
              <v-card
                class="mx-auto"
                max-width="344"
                outlined
              >
                <v-list-item three-line>
                  <v-list-item-content>
                    <v-list-item-title class="headline mb-1">{{ user.username }}</v-list-item-title>
                  </v-list-item-content>

                  <v-img
                    v-if=user.url
                    :src="require('../assets/'+user.url)"
                    class="my-3"
                    contain
                    height="80"
                  />
                </v-list-item>

                <v-card-actions>
                  <v-btn text>Button</v-btn>
                  <v-btn text>Button</v-btn>
                </v-card-actions>
              </v-card>
            </v-item>
          </v-col>
        </v-row>
      </v-container>
    </v-item-group>
  </v-col>

</template>

<script>
  import axios from 'axios'

  const endpoint = 'http://localhost:8000/api/'

  export default {
    name: 'Users',

    data: () => ({
      users: [
        { 'id': 5, 'username': 'Huguinho', 'url': 'huguinho.png' },
        { 'id': 6, 'username': 'Zezinho', 'url': 'zezinho.png' },
        { 'id': 7, 'username': 'Luizinho', 'url': 'luizinho.png' },
        { 'id': 8, 'username': 'Tio Patinhas' },
        { 'id': 9, 'username': 'Pato Donald' },
      ]
    }),
    created() {
      axios.get(endpoint + 'user/')
        .then(response => {
          response.data.map(item => {
            return this.users.push(item)
          })
        })
    }
  }
</script>
EOF
```

#### Imagens

Copie as imagens para o lugar correto.

wget -O src/assets/huguinho.png https://raw.githubusercontent.com/rg3915/django-rest-framework-vuejs/master/img/huguinho.png
wget -O src/assets/zezinho.png https://raw.githubusercontent.com/rg3915/django-rest-framework-vuejs/master/img/zezinho.png
wget -O src/assets/luizinho.png https://raw.githubusercontent.com/rg3915/django-rest-framework-vuejs/master/img/luizinho.png


Prontinho!!!


### Links:

[Django Rest Framework Quickstart][6]

[Django Rest Framework documentação][1]

[django-cors-headers][3]

[VueJS][2]

[Vuetify][5]

[Minicurso: Frontend em 2018 - um guia pra quem tá perdido com Tony Lâmpada][12]

[Minicurso: Vue.JS - O basicão com Tony Lâmpada][13]

[Construindo um front-end moderno com Vue.js - WorkWeb 2018 com Alefe Souza][7]

[ComDevShow 2018 - #3 Construindo um front-end moderno com Vue.js com Alefe Souza][8]

[[Gravação] Live streaming: Vue.js, Vuex e Mirage JS][9]

[[parte 1/2] Vue, Vuex, Computed Properties e Getters][10]

[Vue.js do jeito ninja][11]

[Grupy-SP e VueJS-SP Crossover Out 2019][14]

[1]: https://www.django-rest-framework.org/
[2]: https://vuejs.org/
[3]: https://pypi.org/project/django-cors-headers/
[4]: https://gist.github.com/rg3915/6fad3d19f2b511ec5da40cef5a168ca5
[5]: https://vuetifyjs.com/en/
[6]: http://pythonclub.com.br/django-rest-framework-quickstart.html
[7]: https://www.youtube.com/watch?v=UaaYVaEHo9w
[8]: https://www.youtube.com/watch?v=3Po5Cw6cw98
[9]: https://www.youtube.com/watch?v=17Ro7A3AqxU
[10]: https://www.youtube.com/watch?v=d9GKdl3hxas
[11]: https://www.youtube.com/watch?v=07-TvnH7XNo&list=PLcoYAcR89n-qq1vGRbaUiV6Q9puy0qigW
[12]: https://www.youtube.com/watch?v=ZjgT8S65_pk&list=PLgMNBa0XaIgdFwU1I5Y89fAHdWMxY1ji6
[13]: https://www.youtube.com/watch?v=zLCXSLTJNfw&list=PLgMNBa0XaIgdMt8edUbQmFnqL4g9ZgAxT
[14]: https://www.youtube.com/playlist?list=PLs0UShRCaojIoUESSummFnigDE-ZiOKhB