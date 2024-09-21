document.addEventListener("DOMContentLoaded", () => {
  const BTN_SUBMIT = document.getElementById("btnSubmitAlpha"),
    ID_ALPHA = document.getElementById("id_alfa"),
    CONT_RES = document.getElementById("respuesta"),
    BTNEXPORT = document.getElementById("exportCSV")

  BTN_SUBMIT.addEventListener("click", (e) => {
    e.preventDefault()

    let dato = ID_ALPHA.value

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

    fetch('/calcular_alpha/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken, // Añadir el token CSRF en los headers
      },
      body: JSON.stringify({
        alpha_dato: dato
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
        CONT_RES.innerHTML = "α <sub>real</sub> = 100% - α <sub>dato</sub> = 100% - " + dato + "% = " + data['alpha_real'] * 100 + "% = " + data['alpha_real']
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

  BTNEXPORT.addEventListener("click", (e) => {
    e.preventDefault()
    console.log(Nr);
    downloadCSV([Nr], "rectangulares.csv")
  })

  function downloadCSV(array, filename) {
    // Convertir el array a CSV
    const csvContent = array.map(e => e.join(",")).join("\n");

    // Crear un blob con el contenido CSV
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    // Crear un enlace y simular un clic para descargar el archivo
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
})