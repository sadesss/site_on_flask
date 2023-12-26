// $(document).ready(function() {
//     var panelOne = $('.form-panel.two').height(),
//         panelTwo = $('.form-panel.two')[0].scrollHeight;

//     $('#loginForm').submit(function(e) {
//         e.preventDefault();  // Prevent the default form submission
//         // Your existing login logic here

//         // For testing, you can add a console.log statement
//         console.log('Form submitted');
//     });

//     $('.form-panel.two').not('.form-panel.two.active').on('click', function(e) {
//         e.preventDefault();

//         $('.form-toggle').addClass('visible');
//         $('.form-panel.one').addClass('hidden');
//         $('.form-panel.two').addClass('active');
//         $('.form').animate({
//             'height': panelTwo
//         }, 200);
//     });

//     $('.form-toggle').on('click', function(e) {
//         e.preventDefault();
//         $(this).removeClass('visible');
//         $('.form-panel.one').removeClass('hidden');
//         $('.form-panel.two').removeClass('active');
//         $('.form').animate({
//             'height': panelOne
//         }, 200);
//     });
// });
