function queryBalance() {
    $.get("/balance", function(data, status) {
        console.log(data);
    });
    $("#xcoin-balance").html("500");
}