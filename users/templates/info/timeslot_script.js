$(document).ready(function() {
    $("#timeSlotsForm").submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        var selectedValues = [];
        $("[name='timeSlot']:checked").each(function() {
            selectedValues.push($(this).val());
        });
        var timeSlotsJSON = JSON.stringify(selectedValues);

        // For testing purposes, display the JSON in the console
        console.log(timeSlotsJSON);
        // You can submit the JSON data to the server or perform other actions here
    });
});
