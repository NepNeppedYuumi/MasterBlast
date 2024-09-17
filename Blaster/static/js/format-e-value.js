/**
 * Contains the E-value formatting handler for the BLAST results,
 * BLAST hit and comparison pages.
 * This handler is triggered when the document is ready and 
 * necessary to display e-notation anywhere, because e-values stored
 * in the database are very long floats.
 */

/**
 * Retrieves objects with "display-e-value" at the start of their id.
 * Formats their float values to e-notation.
 */
$(document).ready(function(){
    var cells = document.querySelectorAll('[id^=display-e-value-]');
    for (var i in cells) {
        cells[i].textContent = parseFloat(cells[i].textContent).toExponential(2);
    };
});