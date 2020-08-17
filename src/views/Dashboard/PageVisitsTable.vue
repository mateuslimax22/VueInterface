<template>
  <div class="card">
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0">Pacientes</h3>
        </div>
        <div class="col text-right">
           <input class="form-control" type="text" id="searchQuery" placeholder="Search" />
          
        </div>
      </div>
    </div>

  
    <div class="table-responsive">
            <table v-if="clientes.length" class="table">
                <thead>
                    <tr>
                        <th>Temperatura</th>  
                    </tr>
                </thead>
                <tbody id="table">
                    <tr v-for="cliente in clientes" :key="cliente.subjectid">
                        <td class="subjectid">{{cliente.subjectid}}</td>
                        <td>{{cliente.sex}}</td>
                        <td>{{cliente.dob}}</td>
                        <td>{{cliente.hospitalexpireflg}}</td>
                        <td><base-button type="primary" icon="ni ni-circle-08" v-on:click="greet" >Perfil</base-button></td>
                    </tr>
                </tbody>
            </table>
            <span class="prev">Previous</span><span class="next">Next</span>

             
            
        </div>

  </div>
</template>
<script>
import $ from 'jquery';
import Cliente from '/home/ehealthsys/Documents/jhy/src/services/clientes'



  export default {
    name: 'page-visits-table2',

    data(){
    return{
      clientes:[],
      maxRows:10
    }
  },

    methods: {
    greet: function () {
      this.$router.push({name: 'Perfil'});
    }
  },

    mounted(){
      Cliente.listar().then(resposta => {
        console.log(resposta.data)
        this.clientes = resposta.data
      }),
            
     $("#searchQuery").keyup(function() {
      var data = this.value;
      var rows = $("#table").find("tr");
      if (data == '') {
        rows.show();
      } else {
        rows.hide();
        rows.filter(function () {
          return $(this).find('.subjectid').text().indexOf(data) !== -1
          
        }).show()     
      }
    })  

    },  
  
  }

</script>
<style>
.customers {
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

.customers td, .customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

.customers tr:nth-child(even){background-color: #f2f2f2;}

.customers tr:hover {background-color: #ddd;}

.customers th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #778899;
  color: white;
}
</style>
