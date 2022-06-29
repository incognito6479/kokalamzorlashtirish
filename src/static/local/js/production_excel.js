$("#download_button").click(function (e) {
    e.preventDefault();
    var url_down = "/production/stat/republic/download?month=" + $('#id_month').val() + "&year=" + $('#id_year').val()
    fetch(url_down)
        .then(resp => resp.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            time = new Date()
            a.download = $('#id_year').val()+"-"+$('#id_month').val() +"-"+ time.getHours()+":"+time.getMinutes()+ '.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);

        })
        .catch(() => console.log("Error happend"));


})