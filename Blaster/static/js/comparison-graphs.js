/**
 * Contains the form submission handler for "#switch-graphs".
 * This handler can only be triggered when all HTML elements are loaded.
 */

/**
 * Event handler for changing the selected option in "#switch-graphs".
 * It retrieves the selected option's value, hides all divs in "#comparison-graph"
 * and shows the selected one.
 * This allows for dynamic display of the different graphs based on user selection.
 */
$(document).ready(function () {
  $("#switch-graphs").change(function () {
    var selectedOption = $(this).val(); // Get value of selected option
    $("#comparison-graph > div").hide(); // Hide all divs in "#comparison-graph"
    $("#" + selectedOption).show(); // Show div that matches selected option
  });
});
