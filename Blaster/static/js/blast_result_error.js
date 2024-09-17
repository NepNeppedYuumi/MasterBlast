/**
 * Contains the form submission handler for "#comparison-form".
 * This handler can only be triggered when all HTML elements are loaded.
 */

$(document).ready(function () {
  /**
   * Event handler for submitting "#comparison-form". It checks the number of
   * selected hits and adds an error message to the DOM if less than 2 hits are selected.
   *
   * @param {Event} event - The event object associated with form submission.
   */

  $("#comparison-form").on("submit", function (event) {
    // Get amount of selected hits
    var amount = $('input[name="selected_hits"]:checked').length;

    // Show error message with less than 2 hits selected
    if (amount < 2) {
      event.preventDefault();
      if ($("#error-message").length == 0) {
        $("#comparison-form").prepend(
          '<div id="error-message" class="error-message" role="alert">Please select at least 2 hits for comparison</div>'
        );
      }
    }
  });
});
