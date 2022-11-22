// Show note action buttons on hover
$(".note").hover(function () {
    $(this).find(".title-buttons").show(100);
}, function () {
    $(this).find(".title-buttons").hide(100);
});