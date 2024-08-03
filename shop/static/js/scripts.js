// Custom JavaScript for the e-commerce site

document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom JavaScript loaded.');

    // Example: Alert when a button with class 'btn-alert' is clicked
    document.querySelectorAll('.btn-alert').forEach(button => {
        button.addEventListener('click', function() {
            alert('Button clicked!');
        });
    });
});
