$(document).ready(function(){
	  var endpoint = 'api/data/graphic'
	  var defaultData = []
	  var labels = [];
	  var data_viagem = [];
	  var receita_total =[];
	  var receita_mes = [];
	  var mes = []
	  var valor = [];
	  var tipo = [];
	  var valores_manutencao = [];
	  var receita
	  var manutencao
	  var despesa
	  var pass_total = []
	  var pass_inteira = []
	  var pass_meia = []
	  
	  $.ajax({
		method:"GET",
		url: endpoint,
		success: function(data){
			labels = data.labels
			data_viagem = data.viagem_data
			receita_total = data.receita_total
			receita_mes = data.receita_mes
			defaultData = data.default_itens
			mes = data.meses
			valor = data.valor
			tipo = data.tipo
			valores_manutencao = data.valores_manutencao
			manutencao = data.manutencao
			receita = data.receita
			despesa = data.despesa
			pass_total = data.pass_total
			pass_inteira = data.pass_inteira
			pass_meia = data.pass_meia
			
			setChart()
			console.log(data)
			console.log(data.customers)
			
		
		},
		error: function(error_data){  
			console.log("error")
			console.log(error_data)
		}
	  })	
	  
	  function setChart(){
		  var ctx = document.getElementById("myChart");
		    var myChart = new Chart(ctx, {
		        type: 'line',
		        data: {
		          labels: data_viagem,
		          datasets: [{
		              label: 'receita', 
		              data: receita_total, 
		              backgroundColor: '#007bff',
		              borderColor: '#007bff',
		              borderWidth: 1
		              
		          },
		          { label:'despesas',
		            data: receita_total,
		            backgroundColor:'rgba(255,225,0,0.5)',
		            type:'line'},
		          
		          { label:'passagens',
			        data: valor,
			        backgroundColor:'rgba(0,225,0,0.5)',
	                type:'line'},]
		    
		        },
		        options: {
			          scales: {
			        	  yAxes: [{
			        	        ticks: {
			        	          min: 0,
			        	          max: 30000,
			        	          maxTicksLimit: 30
			        	        },
			        	        gridLines: {
			        	          color: "rgba(0, 0, 0, .125)",
			        	        }
			        	      }],
			          }
			      }
		    });
		    
		    // -- Line Passagens
		    var ctx = document.getElementById("myLinePass");
		    var myChart = new Chart(ctx, {
		        type: 'line',
		        data: {
		          labels: data_viagem,
		          datasets: [{
		              label: 'passagens', 
		              data: pass_total, 
		              backgroundColor: 'rgba(255, 255, 0, 0.5)',
		              borderColor: 'rgba(255, 255, 0, 0.5)',
		              borderWidth: 1   
		          },
		          { label:'inteira',
			            data: pass_inteira,
			            backgroundColor:'rgba(255,225,0,0.5)',
			            type:'line'},
			          
			          { label:'meia',
				        data: pass_meia,
				        backgroundColor:'rgba(0,225,0,0.5)',
		                type:'line'},
		                ]
		        },
		        options: {
			          scales: {
			        	  yAxes: [{
			        	        ticks: {
			        	          min: 0,
			        	          max: 300,
			        	          maxTicksLimit: 30
			        	        },
			        	        gridLines: {
			        	          color: "rgba(0, 0, 0, .125)",
			        	        }
			        	      }],
			          }
			      }
		    });
		    
		    // -- Bar Chart Example
		    var ctx = document.getElementById("myBarChart");
		    var myLineChart = new Chart(ctx, {
		      type: 'bar',
		      data: {
		        labels: ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET","OUT", "NOV", "DEZ"],
		        datasets: [{
		          label: "Valores",
		          backgroundColor: "rgba(2,117,216,1)",
		          borderColor: "rgba(2,117,216,1)",
		          data: valor,
		        }],
		      },
		      options: {
		        scales: {
		          xAxes: [{
		            time: {
		              unit: 'month'
		            },
		            gridLines: {
		              display: false
		            },
		            ticks: {
		              maxTicksLimit: 12
		            }
		          }],
		          yAxes: [{
		            ticks: {
		              min: 0,
		              max: 30000,
		              maxTicksLimit: 5
		            },
		            gridLines: {
		              display: true
		            }
		          }],
		        },
		        legend: {
		          display: true
		        }
		      }
		    });
		   
		    
		    // -- Pie Receitas
		    var ctx = document.getElementById("myPieChart");
		    var myPieChart = new Chart(ctx, {
		      type: 'pie',
		      data: {
		        labels: ["Receita", "Manutenção", "Despesa"],
		        datasets: [{
		          data: [receita, manutencao, despesa],
		          backgroundColor: ['#007bff', '#dc3545', '#ffc107'],
		        }],
		      },
		    });
		    
		    // -- Pie Manutencao
		    var ctx = document.getElementById("myPieDespesas");
		    var myPieChart = new Chart(ctx, {
		      type: 'pie',
		      data: {
		        labels: tipo,
		        datasets: [{
		          data: valores_manutencao,
		          backgroundColor: ['rgba(0,0,0,1)', '#dc3545', '#ffc107', '#28a745','rgba(2,117,216,1)', 'rgba(20,100,200,1)' ],
		        }],
		      },
		    })
		    
	  }
		  
		  /*var ctx = document.getElementById("myChart").getContext('2d');
	      var myChart = new Chart(ctx, {
	      type: 'bar',
	      data: {
	          labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
	          datasets: [{
	              label: '# of Votes',
	              data: defaultData,
	              backgroundColor: [
	                  'rgba(255, 99, 132, 0.2)',
	                  'rgba(54, 162, 235, 0.2)',
	                  'rgba(255, 206, 86, 0.2)',
	                  'rgba(75, 192, 192, 0.2)',
	                  'rgba(153, 102, 255, 0.2)',
	                  'rgba(255, 159, 64, 0.2)'
	              ],
	              borderColor: [
	                  'rgba(255,99,132,1)',
	                  'rgba(54, 162, 235, 1)',
	                  'rgba(255, 206, 86, 1)',
	                  'rgba(75, 192, 192, 1)',
	                  'rgba(153, 102, 255, 1)',
	                  'rgba(255, 159, 64, 1)'
	              ],
	              borderWidth: 1
	          }]
	      },
	      options: {
	          scales: {
	              yAxes: [{
	                  ticks: {
	                      beginAtZero:true
	                  }
	              }]
	          }
	      }
	  });*/
  })
  