/**
 * Contains the file export handler for the BLAST hit page.
 * This handler is triggered when the "Export" button is clicked.
 */

/**
 * Retrieves the format type and its related data from the document.
 * Creates a blob to export and download a file of the chosen type.
 */
function exportFile() {
    event.preventDefault();

    // Retrieve chosen export format and get metadata
    const format = document.getElementById("export-format").value;
    const data = $('#' + format).data();
    const content = data.name;
    const filename = data.other;

    // Create blob to export and download it
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    return false;
}