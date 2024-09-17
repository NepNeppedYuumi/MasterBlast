/**
 * Contains the select column header handler for the BLAST results page.
 * This handler is triggered when the "Select" header is clicked.
 */

/**
 * Checks if all elements of class select-all are checked.
 * If so, they are turned to unchecked.
 * Otherwise, all elements are checked
 */
function selectAll() {
  var allChecked = $('.select-all:checked').length === $('.select-all').length;
  if (allChecked) {
    $('.select-all').prop('checked', false);
  } else {
    $('.select-all').prop('checked', true);
  }
}