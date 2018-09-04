function queryBalance() {
    $.get("/balance", function(data, status) {
        console.log(data);
        $("#xcoin-balance").html(data);
    });
}

function send() {
    var address = $("#address").val();
    var amount = $("#amount").val();

    $.post("/send", {
        "address": address,
        "amount": amount
    }, function(data, status) {
        console.log(data);
    });
} 