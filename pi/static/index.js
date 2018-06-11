function getEvents() {

    let settings = {
        "async": true,
        "crossDomain": true,
        "url": "/api/events",
        "method": "GET",
    }

    $.ajax(settings)
        .always(function () {

        })
        .done(function (data, textStatus, jqXHR) {
            console.log("got data")
            $(".target").html(JSON.stringify(data))
            setTimeout(getEvents, 1000)
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log("error, could not fetch")
        })
}

$(document).ready(function () {
    setTimeout(getEvents, 1000)
})
