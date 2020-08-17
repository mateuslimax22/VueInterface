<template>
  <div class="card">
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <div id="chart_div" style="width: 100%; height: 500px;"></div>
        </div>
      </div>
    </div>
  </div>

</template>
<script >

import Cliente from '../../services/clientes'
import Paciente from '../../views/Perfil'

  export default {
    name: 'grafico-bp',

    data(){
    return{
      clientes:[],
      maxRows:10
    }
  },

    mounted(){
      Cliente.listar().then(resposta => {
        console.log(resposta.data)
        this.clientes = resposta.data
      }),
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);    
        function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Tempo', 'BPM'],
          ['1',      100],//Colocar os dados de Tempo e Batimentos
          ['2',      90],
          ['3',       100],
          ['4',      80],
          ['5',       90],
          ['6',      100],
          ['7',       60],
          ['9',      100],
        ]);

        var options = {
          legend: 'BPM', series:{
            0: {color: '#DD4477'}//Se quiser alterar a cor do gráfico, basta alterar o parametro entre '', Azul = #3366CCv Vermelho = #DC3912 Amarelo = #FF9900 Verde = #109618
          },
          title: 'BPM',
          hAxis: {title: 'Tempo',  titleTextStyle: {color: '#333'}},
          vAxis: {minValue: 0}
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }

    },  
  
  }

</script>
<style>
</style>
