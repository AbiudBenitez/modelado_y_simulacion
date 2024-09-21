document.addEventListener("DOMContentLoaded", () => {
  const BTN_RADIO1 = document.getElementById("btnradio1"),
    BTN_RADIO2 = document.getElementById("btnradio2"),
    MANUAL = document.getElementById("numeros_cont"),
    ARCHIVO = document.getElementById("numeros"),
    BTN_ENVIAR = document.getElementById("btn-enviar"),
    INPUT_NUM = document.getElementById("num_rec"),
    MANUAL_NUMBERS = document.getElementById("manual-numbers"),
    FORM = document.getElementById("promedios_data"),
    BTNRADIO1 = document.getElementById("btnradio1"),
    FILENUMBERS = document.getElementById("file_numbers"),
    NRVAL = document.getElementById("nrVal"),
    NVAL = document.getElementById("nval"),
    MEDIAVAL = document.getElementById("mediaVal"),
    FORMULA = document.getElementById("formulaVals"),
    DIVRESPONSE = document.getElementById("response"),
    BTNSUBMITALPHA = document.getElementById("btnSubmitAlpha"),
    BTNSUBMITALPHADN = document.getElementById("btnSubmitAlphaDn"),
    RENDER = new FileReader(),
    TBODYKS = document.getElementById("tbodyks"),
    TABLEKS = document.getElementById("tableks")

  const DIVKS = document.getElementById("responseks")

    let Zo = ''
    let Dn = ''
    let n = ''
    let promedios

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');

    if(BTN_RADIO1.checked === true) {
      MANUAL.classList.toggle("d-none")
    } else {
      ARCHIVO.classList.toggle("d-none")
    }

    BTN_RADIO2.addEventListener("change", () => {
      MANUAL.classList.add("d-none")
      ARCHIVO.classList.remove("d-none")
    })

    BTN_RADIO1.addEventListener("change", () => {
      MANUAL.classList.remove("d-none")
      ARCHIVO.classList.add("d-none")
    })

    FILENUMBERS.addEventListener("change", (event) => {
      const FILE = event.target.files[0];
      RENDER.onload = (e) => {
        const csvData = e.target.result

        Papa.parse(csvData, {
          header: false,
          skipEmptyLines: true,
          complete: function(results) {
            console.log(results.data[0]);
            promedios = results.data[0].map(i=>Number(i));
            calcProm(promedios)
            calcKS(promedios)
          }
        })
      }
      console.log(promedios);
      RENDER.readAsText(FILE)
    })

    BTN_ENVIAR.addEventListener("click", (e) => {
      e.preventDefault()
      if(!INPUT_NUM.value) {
        alert("Valida que los campos esten completos")
      } else {
        MANUAL_NUMBERS.classList.remove("d-none")
        let cantidad = INPUT_NUM.value
        MANUAL_NUMBERS.innerHTML = ''
        for (let i = 0; i < cantidad; i++) {
          MANUAL_NUMBERS.innerHTML += '<section class="col-3 mb-3"></section>'
          MANUAL_NUMBERS.lastChild.innerHTML = '<label for="numero_'+ parseInt(i+1) +'" class="form-label" id="label_'+ parseInt(i+1) +'">Numero '+ parseInt(i+1) +'</label>'
          MANUAL_NUMBERS.lastChild.innerHTML += '<input type="text" required class="form-control" name="numero_'+ parseInt(i+1) +'" id="numero_'+ parseInt(i+1) +'">'
        }
        MANUAL_NUMBERS.innerHTML += '<section class="col-12"><button class="btn btn-info col-12">Calcular</button></section>'
      }
    })

    FORM.addEventListener("submit", (e) => {
      e.preventDefault()
      DIVRESPONSE.classList.remove("d-none")
      if(BTNRADIO1.checked) {
        let inputs = MANUAL_NUMBERS.querySelectorAll('input')
        // let csrftoken = e.target.querySelector("input").value
        let promedio = []
        inputs.forEach(input => {
          promedio.push(parseFloat(input.value))
        });
        console.log(promedio);
        calcProm(promedio)
        calcKS(promedio)
      }
    })

    BTNSUBMITALPHA.addEventListener("click", (e) => {
      e.preventDefault()
      const ID_ALPHA = document.getElementById("id_alfa"), 
      CONT_RES = document.getElementById("respuesta")
      fetch('/calcular_alpha/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'), // Añadir el token CSRF en los headers
        },
        body: JSON.stringify({
          alpha_dato: ID_ALPHA.value
        }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error en la solicitud');
          }
          return response.json();
        })
        .then(data => {
          CONT_RES.style.display = "block"
          CONT_RES.innerHTML = "α <sub>real</sub> = 100% - α <sub>dato</sub> = 100% - " + ID_ALPHA.value + "% = " + data['alpha_real'] * 100 + "% = " + data['alpha_real']
          CONT_RES.innerHTML += "<br>Z <sub>α real / 2</sub> = Z <sub>" + data['alpha_real'] + "/2 </sub>= Z<sub> " + data['Zar'] + "</sub>"
          CONT_RES.innerHTML += "<br>Z = " + data['Z']
          if(Zo < data['Z']) {
            CONT_RES.innerHTML += "<br><span class='lead text-success'>Los numeros rectangulares son ACEPTADOS</span>"
          } else {
            CONT_RES.innerHTML += "<br><span class='lead text-danger'>Los numeros rectangulares son RECHAZADOS</span>"
  
          }
          console.log('Respuesta del servidor:', data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    })

    BTNSUBMITALPHADN.addEventListener("click", (e) => {
      e.preventDefault()
      const ID_ALPHA_DN = document.getElementById("id_alfaDn"), 
      CONT_RES_DN = document.getElementById("respuestaDn")
      fetch('/calcular_alpha_dn/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'), // Añadir el token CSRF en los headers
        },
        body: JSON.stringify({
          alpha_dato: ID_ALPHA_DN.value,
          n: n,
          promedios: promedios
        }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error en la solicitud');
          }
          return response.json();
        })
        .then(data => {
          CONT_RES_DN.style.display = "block"
          CONT_RES_DN.innerHTML = "<p class='text-warning'>Revisa el valor original de la tabla, ya que esta funcion no es optima para muestras menores de 100</p>"
          CONT_RES_DN.innerHTML += "d <sub>α,N</sub> = d <sub>" + data['alpha_real'] + "," + data['n'] + "</sub> = " + data['Dan']
          if(Dn < data['Dan']) {
            CONT_RES_DN.innerHTML += "<br><span class='lead text-info'>"+ Dn +" < "+ data['Dan'] +"</span>"
            CONT_RES_DN.innerHTML += "<br><span class='lead text-success'>Los numeros rectangulares son ACEPTADOS</span>"
          } else {
            CONT_RES_DN.innerHTML += "<br><span class='lead text-info'>"+ Dn +" > "+ data['Dan'] +"</span>"
            CONT_RES_DN.innerHTML += "<br><span class='lead text-danger'>Los numeros rectangulares son RECHAZADOS</span>"
  
          }
          console.log('Respuesta del servidor:', data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    })

    function calcProm(datos) {
      DIVRESPONSE.classList.remove("d-none")
      fetch('/promedio_value/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken, // Añadir el token CSRF en los headers
        },
        body: JSON.stringify({
          lista: datos
        }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error en la solicitud');
          }
          return response.json();
        })
        .then(data => {
          console.log('Respuesta del servidor:', data);
          NRVAL.innerHTML = ""
          data['lista'].forEach((element, i) => {
            if(i === 0) {
              NRVAL.innerHTML += element
            } else {
              NRVAL.innerHTML += " + " + element
            }
          });
          NVAL.innerHTML = data['n']
          MEDIAVAL.innerHTML = data['promedio']
          FORMULA.innerHTML = "Zo = | (("+ data['promedio'] +" - 1/2) * √"+ data['n'] +") / √(1/12) | = " + data['Zo']
          Zo = data['Zo']
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }

    function calcKS(datos) {
      DIVKS.classList.remove("d-none")
      fetch('/ks_value/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken, // Añadir el token CSRF en los headers
        },
        body: JSON.stringify({
          lista: datos
        }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error en la solicitud');
          }
          return response.json();
        })
        .then(data => {
          console.log('Respuesta del servidor:', data);
          for(let i = 0; i < data['n']; i++) {
            TBODYKS.innerHTML += '<tr></tr>'
            TBODYKS.lastChild.innerHTML += '<td>'+ parseInt(i+1) +'</td>'
            TBODYKS.lastChild.innerHTML += '<td>'+ data['listaOrd'][i] +'</td>'
            TBODYKS.lastChild.innerHTML += '<td>'+ parseInt(i+1) +' / '+ data['n'] +' = '+ data['Fxi'][i] +'</td>'
            TBODYKS.lastChild.innerHTML += '<td>'+  data['Fxi'][i] +' - '+ data['listaOrd'][i] +' = '+ data['Dn'][i] +'</td>'
          }
          TABLEKS.innerHTML += "<p class='text-center col-12'>D<sub>n</sub> = "+ data['Dnm'] +"</p>"
          Dn = data['Dnm']
          n = data['n']
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
})