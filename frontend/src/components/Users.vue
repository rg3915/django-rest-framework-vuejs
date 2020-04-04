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
        { 'id': 1, 'username': 'Huguinho', 'url': 'huguinho.png' },
        { 'id': 2, 'username': 'Zezinho', 'url': 'zezinho.png' },
        { 'id': 3, 'username': 'Luizinho', 'url': 'luizinho.png' },
        { 'id': 4, 'username': 'Tio Patinhas' },
        { 'id': 5, 'username': 'Pato Donald' },
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
